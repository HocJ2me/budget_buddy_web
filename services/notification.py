from config.mailer import send_email
from utils.email_templates import alert_template, forecast_template, goal_plan_template


def send_budget_alert_email(to_email, username, category, spent, limit, alert_type='overbudget'):
    subject = f"[Cảnh báo] Vượt ngân sách {category}" if alert_type == 'overbudget' else f"[Cảnh báo] Chi tiêu bất thường {category}"
    html = alert_template(username, category, spent, limit, alert_type)
    return send_email(to_email, subject, html)


def send_forecast_email(to_email, username, income, expected_expense, predicted_balance):
    subject = "[Báo cáo] Dự báo dòng tiền cuối tháng"
    html = forecast_template(
        username, income, expected_expense, predicted_balance)
    return send_email(to_email, subject, html)


def send_goal_plan_email(to_email, username, goal_name, target, current_saved, monthly_needed, est_months):
    subject = f"[Mục tiêu] Kế hoạch tích lũy {goal_name}"
    html = goal_plan_template(
        username, goal_name, target, current_saved, monthly_needed, est_months)
    return send_email(to_email, subject, html)
