import os
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from services.notification import send_goal_plan_email

app = Flask(__name__)
# Đổi thành key bí mật bất kỳ
app.config['SECRET_KEY'] = 'super-secret-key-123'
db_path = os.path.join(app.instance_path, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.makedirs(app.instance_path, exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Chưa login sẽ tự động nhảy về route này

# --- MODELS ---


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'income' hoặc 'expense'
    note = db.Column(db.String(200), nullable=True)
    date = db.Column(db.String(50), nullable=False)


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    target = db.Column(db.Float, nullable=False)
    current_saved = db.Column(db.Float, default=0.0)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- AUTH ROUTES (Login, Signup, Logout) ---


@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('overview'))
    return render_template('login.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        flash('Tên đăng nhập hoặc mật khẩu không chính xác!', 'error')
        return redirect(url_for('login'))

    login_user(user)
    return redirect(url_for('overview'))


@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
        flash('Mật khẩu nhập lại không khớp!', 'error')
        return redirect(url_for('login'))

    if User.query.filter_by(username=username).first():
        flash('Tên đăng nhập đã tồn tại!', 'error')
        return redirect(url_for('login'))

    if User.query.filter_by(email=email).first():
        flash('Email đã được đăng ký!', 'error')
        return redirect(url_for('login'))

    hashed_pwd = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_pwd)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return redirect(url_for('overview'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# --- MAIN APP ROUTES ---

@app.route('/')
@login_required
def overview():
    # Lấy toàn bộ dữ liệu từ CSDL ra để truyền sang HTML
    transactions_list = Transaction.query.order_by(Transaction.id.desc()).all()
    goals_list = Goal.query.all()
    return render_template('overview.html', user=current_user, transactions=transactions_list, goals=goals_list)


@app.route('/transactions')
@login_required
def transactions():
    return render_template('transactions.html', user=current_user)


@app.route('/budgets')
@login_required
def budgets():
    return render_template('budgets.html', user=current_user)


@app.route('/goals')
@login_required
def goals():
    return render_template('goals.html', user=current_user)


@app.route('/ai-coach')
@login_required
def ai_coach():
    return render_template('ai-coach.html', user=current_user)


# ---------------- TRANSACTIONS API ----------------

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    result = [{
        'id': t.id,
        'amount': t.amount,
        'category': t.category,
        'type': t.type,
        'note': t.note,
        'date': t.date
    } for t in transactions]
    return jsonify(result)


@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    new_tx = Transaction(
        amount=data['amount'],
        category=data['category'],
        type=data['type'],
        note=data.get('note', ''),
        date=data['date']
    )
    db.session.add(new_tx)
    db.session.commit()
    return jsonify({"success": True, "id": new_tx.id})


# ---------------- GOALS API ----------------

@app.route('/api/goals', methods=['GET'])
def get_goals():
    goals = Goal.query.all()
    result = [{
        'id': g.id,
        'name': g.name,
        'target': g.target,
        'current_saved': g.current_saved
    } for g in goals]
    return jsonify(result)


@app.route('/api/goals', methods=['POST'])
def add_goal():
    data = request.json
    new_goal = Goal(
        name=data['name'],
        target=data['target'],
        current_saved=data.get('current_saved', 0.0)
    )
    db.session.add(new_goal)
    db.session.commit()

    # Gửi email thông báo tạo mục tiêu nếu có truyền email
    if current_user.email:
        remaining = max(0, new_goal.target - new_goal.current_saved)
        monthly_needed = 1500000
        est_months = max(1, int(remaining / monthly_needed)
                         ) if remaining > 0 else 0
        send_goal_plan_email(
            current_user.email,
            current_user.username,
            new_goal.name,
            new_goal.target,
            new_goal.current_saved,
            monthly_needed,
            est_months
        )

    return jsonify({"success": True, "id": new_goal.id})


@app.route('/api/goals/<int:goal_id>/deposit', methods=['POST'])
def deposit_goal(goal_id):
    data = request.json
    deposit_amount = float(data.get('amount', 0))

    goal = Goal.query.get_or_404(goal_id)
    goal.current_saved += deposit_amount
    db.session.commit()

    # Tính toán thông số gửi email
    remaining = max(0, goal.target - goal.current_saved)
    monthly_needed = 1500000
    est_months = max(1, int(remaining / monthly_needed)
                     ) if remaining > 0 else 0

    user_email = current_user.email if current_user.is_authenticated else data.get(
        'user_email')
    username = current_user.username if current_user.is_authenticated else data.get(
        'username', 'Bạn')

    if user_email:
        send_goal_plan_email(
            to_email=user_email,
            username=username,
            goal_name=goal.name,
            target=goal.target,
            current_saved=goal.current_saved,
            monthly_needed=monthly_needed,
            est_months=est_months
        )

    return jsonify({
        "success": True,
        "current_saved": goal.current_saved,
        "message": f"Đã nạp {deposit_amount:,.0f} ₫ vào mục tiêu {goal.name}"
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
