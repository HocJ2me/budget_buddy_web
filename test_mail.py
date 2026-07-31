from services.notification import send_budget_alert_email, send_forecast_email, send_goal_plan_email

# Thay địa chỉ email nhận bằng EMAIL THẬT CỦA BẠN để kiểm tra hộp thư
RECEIVER_EMAIL = "your_actual_email@gmail.com"

print("⏳ Đang tiến hành gửi email test...")

# Test 1: Gửi thử mail Cảnh báo ngân sách
success = send_budget_alert_email(
    to_email=RECEIVER_EMAIL,
    username="User Test",
    category="Ăn uống",
    spent=1500000,
    limit=1000000,
    alert_type="overbudget"
)

if success:
    print("✅ Gửi email test thành công! Hãy kiểm tra Hộp thư đến (hoặc thư mục Spam).")
else:
    print("❌ Gửi email thất bại. Hãy kiểm tra lại EMAIL_USER và EMAIL_PASS trong file .env")
