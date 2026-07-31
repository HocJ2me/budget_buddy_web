from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Đổi thành key bí mật bất kỳ
app.config['SECRET_KEY'] = 'super-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Chưa login sẽ tự động nhảy về route này

# --- Model User ---


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- AUTH ROUTES (Login, Signup, Logout) ---


@app.route('/login', methods=['GET'])
def login():
    # Nếu đã đăng nhập từ trước -> Chuyển thẳng về trang Overview /
    if current_user.is_authenticated:
        return redirect(url_for('overview'))
    return render_template('login.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    # Kiểm tra username có tồn tại và password có đúng không
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

    # Lưu user mới vào CSDL
    hashed_pwd = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_pwd)
    db.session.add(new_user)
    db.session.commit()

    # Đăng nhập luôn sau khi đăng ký thành công
    login_user(new_user)
    return redirect(url_for('overview'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# --- MAIN APP ROUTES (Cần đăng nhập mới truy cập được) ---

@app.route('/')
@login_required
def overview():
    return render_template('overview.html', user=current_user)


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tự động tạo bảng User trong SQLite nếu chưa có
    app.run(debug=True)
