def format_vnd(amount):
    return f"{amount:,.0f} ₫".replace(",", ".")


def alert_template(username, category, spent, limit, alert_type='overbudget'):
    is_over = alert_type == 'overbudget'
    title = '⚠️ Cảnh Báo Vượt Ngân Sách' if is_over else '🚨 Chi Tiêu Bất Thường'
    color = '#DC2626' if is_over else '#D97706'
    bg_badge = '#FEF2F2' if is_over else '#FFFBEB'

    desc = f"Danh mục <b>{category}</b> của bạn đã vượt quá hạn mức ngân sách đặt ra." if is_over else f"Hệ thống ghi nhận một khoản chi tiêu lớn bất thường ở danh mục <b>{category}</b>."

    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body style="margin: 0; padding: 0; background-color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
      <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #F8FAFC; padding: 40px 10px;">
        <tr>
          <td align="center">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 500px; background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.04);">
              
              <!-- Brand Header -->
              <tr>
                <td style="padding: 20px 24px 16px; border-bottom: 1px solid #E2E8F0;">
                  <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                      <td width="38">
                        <div style="width: 38px; height: 38px; background: #0D9488; border-radius: 10px; text-align: center; line-height: 38px; font-size: 18px;">💰</div>
                      </td>
                      <td style="padding-left: 12px;">
                        <div style="font-size: 16px; font-weight: 700; color: #1E293B;">Budget Buddy</div>
                        <div style="font-size: 12px; font-weight: 500; color: #64748B;">Smart Finance</div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- Banner Status -->
              <tr>
                <td style="padding: 16px 24px; background-color: {bg_badge}; border-bottom: 1px solid #E2E8F0;">
                  <div style="font-size: 17px; font-weight: 700; color: {color};">
                    {title}
                  </div>
                </td>
              </tr>

              <!-- Main Content -->
              <tr>
                <td style="padding: 24px; color: #334155; font-size: 14px; line-height: 1.6;">
                  <p style="margin: 0 0 12px; font-size: 15px;">Xin chào <b style="color: #0D9488;">{username}</b>,</p>
                  <p style="margin: 0 0 20px; color: #475569;">{desc}</p>
                  
                  <!-- Detail Card -->
                  <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px 20px; margin-bottom: 24px;">
                    <table width="100%" border="0" cellspacing="0" cellpadding="0">
                      <tr>
                        <td style="padding: 6px 0; color: #64748B; font-size: 13px; font-weight: 500;">Đã chi tiêu:</td>
                        <td align="right" style="padding: 6px 0; color: #DC2626; font-size: 15px; font-weight: 700;">{format_vnd(spent)}</td>
                      </tr>
                      {f'''
                      <tr>
                        <td style="padding: 6px 0; color: #64748B; font-size: 13px; font-weight: 500;">Hạn mức đặt ra:</td>
                        <td align="right" style="padding: 6px 0; color: #1E293B; font-size: 14px; font-weight: 600;">{format_vnd(limit)}</td>
                      </tr>
                      ''' if limit else ''}
                    </table>
                  </div>

                  <!-- Action Button -->
                  <div style="text-align: center;">
                    <a href="http://127.0.0.1:5000/budgets" style="display: inline-block; background-color: #0D9488; color: #FFFFFF; text-decoration: none; font-weight: 700; font-size: 14px; padding: 12px 24px; border-radius: 10px;">Kiểm tra ngân sách ngay &rarr;</a>
                  </div>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="padding: 16px 24px; background-color: #F8FAFC; border-top: 1px solid #E2E8F0; text-align: center; color: #64748B; font-size: 12px;">
                  Thông báo tự động từ <b>Budget Buddy</b> &middot; Quản lý chi tiêu thông minh
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>"""


def forecast_template(username, income, expected_expense, predicted_balance):
    is_positive = predicted_balance >= 0
    balance_color = '#0D9488' if is_positive else '#DC2626'

    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body style="margin: 0; padding: 0; background-color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
      <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #F8FAFC; padding: 40px 10px;">
        <tr>
          <td align="center">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 500px; background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.04);">
              
              <!-- Brand Header -->
              <tr>
                <td style="padding: 20px 24px 16px; border-bottom: 1px solid #E2E8F0;">
                  <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                      <td width="38">
                        <div style="width: 38px; height: 38px; background: #0D9488; border-radius: 10px; text-align: center; line-height: 38px; font-size: 18px;">💰</div>
                      </td>
                      <td style="padding-left: 12px;">
                        <div style="font-size: 16px; font-weight: 700; color: #1E293B;">Budget Buddy</div>
                        <div style="font-size: 12px; font-weight: 500; color: #64748B;">Smart Finance</div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- Banner Title -->
              <tr>
                <td style="padding: 20px 24px; background-color: #0D9488; color: #FFFFFF;">
                  <div style="font-size: 12px; font-weight: 500; opacity: 0.9;">Báo Cáo Tài Chính</div>
                  <div style="font-size: 18px; font-weight: 700; margin-top: 2px;">📈 Dự Báo Dòng Tiền Cuối Tháng</div>
                </td>
              </tr>

              <!-- Main Content -->
              <tr>
                <td style="padding: 24px; color: #334155; font-size: 14px; line-height: 1.6;">
                  <p style="margin: 0 0 12px; font-size: 15px;">Xin chào <b style="color: #0D9488;">{username}</b>,</p>
                  <p style="margin: 0 0 20px; color: #475569;">Dựa trên nhịp độ thu chi hiện tại, hệ thống đã tính toán dòng tiền ước tính đến cuối tháng của bạn:</p>
                  
                  <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px 20px; margin-bottom: 20px;">
                    <table width="100%" border="0" cellspacing="0" cellpadding="0">
                      <tr>
                        <td style="padding: 6px 0; color: #64748B; font-size: 13px; font-weight: 500;">Thu nhập ước tính:</td>
                        <td align="right" style="padding: 6px 0; color: #059669; font-size: 14px; font-weight: 700;">+{format_vnd(income)}</td>
                      </tr>
                      <tr>
                        <td style="padding: 6px 0; color: #64748B; font-size: 13px; font-weight: 500;">Chi tiêu dự kiến:</td>
                        <td align="right" style="padding: 6px 0; color: #DC2626; font-size: 14px; font-weight: 700;">-{format_vnd(expected_expense)}</td>
                      </tr>
                      <tr>
                        <td colspan="2" style="padding: 6px 0;"><div style="border-bottom: 1px dashed #CBD5E1;"></div></td>
                      </tr>
                      <tr>
                        <td style="padding: 10px 0 4px; color: #1E293B; font-size: 14px; font-weight: 700;">Số dư dự kiến cuối tháng:</td>
                        <td align="right" style="padding: 10px 0 4px; color: {balance_color}; font-size: 16px; font-weight: 700;">{format_vnd(predicted_balance)}</td>
                      </tr>
                    </table>
                  </div>

                  {'<div style="background-color: #FEF2F2; border-radius: 10px; padding: 12px 14px; color: #DC2626; font-size: 13px; font-weight: 600; margin-bottom: 20px;">⚠️ Cảnh báo: Bạn có nguy cơ thâm hụt tài chính nếu duy trì tốc độ chi tiêu này.</div>' if not is_positive else ''}

                  <div style="text-align: center;">
                    <a href="http://127.0.0.1:5000/" style="display: inline-block; background-color: #1E293B; color: #FFFFFF; text-decoration: none; font-weight: 700; font-size: 14px; padding: 12px 24px; border-radius: 10px;">Xem tổng quan tài chính &rarr;</a>
                  </div>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="padding: 16px 24px; background-color: #F8FAFC; border-top: 1px solid #E2E8F0; text-align: center; color: #64748B; font-size: 12px;">
                  Thông báo tự động từ <b>Budget Buddy</b> &middot; Quản lý chi tiêu thông minh
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>"""


def goal_plan_template(username, goal_name, target, current_saved, monthly_needed, est_months):
    pct = min(100, int((current_saved / target) * 100))

    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body style="margin: 0; padding: 0; background-color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
      <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #F8FAFC; padding: 40px 10px;">
        <tr>
          <td align="center">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 500px; background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.04);">
              
              <!-- Brand Header -->
              <tr>
                <td style="padding: 20px 24px 16px; border-bottom: 1px solid #E2E8F0;">
                  <table width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                      <td width="38">
                        <div style="width: 38px; height: 38px; background: #0D9488; border-radius: 10px; text-align: center; line-height: 38px; font-size: 18px;">💰</div>
                      </td>
                      <td style="padding-left: 12px;">
                        <div style="font-size: 16px; font-weight: 700; color: #1E293B;">Budget Buddy</div>
                        <div style="font-size: 12px; font-weight: 500; color: #64748B;">Smart Finance</div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- Banner Title -->
              <tr>
                <td style="padding: 20px 24px; background-color: #7C3AED; color: #FFFFFF;">
                  <div style="font-size: 12px; font-weight: 500; opacity: 0.9;">Kế Hoạch Tiết Kiệm</div>
                  <div style="font-size: 18px; font-weight: 700; margin-top: 2px;">🎯 Mục tiêu: {goal_name}</div>
                </td>
              </tr>

              <!-- Main Content -->
              <tr>
                <td style="padding: 24px; color: #334155; font-size: 14px; line-height: 1.6;">
                  <p style="margin: 0 0 12px; font-size: 15px;">Xin chào <b style="color: #7C3AED;">{username}</b>,</p>
                  <p style="margin: 0 0 20px; color: #475569;">Dưới đây là cập nhật kế hoạch tích lũy chi tiết cho mục tiêu của bạn:</p>

                  <!-- Progress Container -->
                  <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px 20px; margin-bottom: 20px;">
                    <div style="margin-bottom: 8px; font-size: 13px; font-weight: 700; color: #7C3AED;">
                      Tiến độ đạt {pct}% <span style="color: #64748B; font-weight: 500; float: right;">{format_vnd(current_saved)} / {format_vnd(target)}</span>
                    </div>
                    
                    <!-- Progress Bar -->
                    <div style="height: 8px; background-color: #E2E8F0; border-radius: 99px; overflow: hidden; margin-bottom: 12px;">
                      <div style="width: {pct}%; height: 100%; background-color: #7C3AED;"></div>
                    </div>

                    <div style="font-size: 13px; color: #64748B; border-top: 1px solid #E2E8F0; padding-top: 10px;">
                      Còn lại: <b style="color: #1E293B;">{format_vnd(target - current_saved)}</b>
                    </div>
                  </div>

                  <!-- Recommendation Note -->
                  <div style="background-color: #F3E8FF; border-radius: 10px; padding: 12px 16px; color: #6B21A8; font-size: 13px; font-weight: 600; margin-bottom: 24px;">
                    💡 Đề xuất: Để hoàn thành đúng hạn, bạn nên tích lũy <b>{format_vnd(monthly_needed)}/tháng</b> trong khoảng <b>~{est_months} tháng</b> tới.
                  </div>

                  <div style="text-align: center;">
                    <a href="http://127.0.0.1:5000/budgets" style="display: inline-block; background-color: #7C3AED; color: #FFFFFF; text-decoration: none; font-weight: 700; font-size: 14px; padding: 12px 24px; border-radius: 10px;">Nạp tiền vào mục tiêu ngay &rarr;</a>
                  </div>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="padding: 16px 24px; background-color: #F8FAFC; border-top: 1px solid #E2E8F0; text-align: center; color: #64748B; font-size: 12px;">
                  Thông báo tự động từ <b>Budget Buddy</b> &middot; Quản lý chi tiêu thông minh
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>"""
