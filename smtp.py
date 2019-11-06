# --*-- coding: utf-8 --*--
#!/usr/bin/python
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_mail(receiver,att):
    sender = 'sparkxyf@163.com'
    # receiver = '631102050@qq.com'
    smtpserver = 'smtp.163.com'
    username = 'sparkxyf'
    password = 'sparkxyf163'
    mail_title = '今日推荐'

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header(mail_title, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('今日邮件更新', 'plain', 'utf-8'))

    # 构造附件1（附件为TXT格式的文本）
    att1 = MIMEText(open(att, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    filename ='attachment; filename='+att
    att1["Content-Disposition"] = filename
    message.attach(att1)



    smtpObj = smtplib.SMTP_SSL(smtpserver)  # 注意：如果遇到发送失败的情况（提示远程主机拒接连接），这里要使用SMTP_SSL方法
    smtpObj.connect(smtpserver)
    smtpObj.login(username, password)
    smtpObj.sendmail(sender, receiver, message.as_string())
    print("邮件发送成功！！！")
    smtpObj.quit()



if __name__ == "__main__":
    try:
        send_mail('631102050@qq.com','a.txt')
    except Exception as e:
        print(str(e))
