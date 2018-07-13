import os
import my_config
import smtplib
from email.header import Header
from email.mime.text import MIMEText
 
# 第三方 SMTP 服务
mail_host = "smtp.163.com"      # SMTP服务器
mail_user = my_config.Mail_user_name    # 用户名
mail_pass = my_config.Mail_user_password  # 授权密码，非登录密码
sender = my_config.Mail_user_name    # 发件人邮箱(最好写全, 不然会失败)
 
title_for_confirm = '验证邮箱'  # 邮件主题
title_for_reset_password = '更改密码' 

def creat_body_for_confirm(email,reg_time,confirm):
     send_message = my_config.host_ip + ":" + my_config.port + "/confirm/" +email + "/" + str(reg_time) + "/" + str(confirm)
     return send_message

def send_email_for_confirm(to_email, email,reg_time,confirm):
    msg = "点击该链接完成验证:"
    body = creat_body_for_confirm(email,reg_time,confirm)
    message = MIMEText("点击该链接完成验证:"+body, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    receivers = to_email
    message['To'] = ",".join(receivers)
    message['Subject'] = title_for_confirm

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证        
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

  
def send_email_for_reset_password(to_email, body):
    msg = "点击该链接完成验证:"
    
    message = MIMEText("点击该链接更改密码:"+body, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    receivers = to_email
    message['To'] = ",".join(receivers)
    message['Subject'] = title_for_reset_password

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证        
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

 