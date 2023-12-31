import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.text import MIMEText
from email.header import Header

smtp_server = 'smtp.163.com'
mail_user = 'eblab001@163.com'
mail_pass = 'OCRJMURWBSMFEOCN'
name = ["", "", "", "", "", "", "", "", "", "", ""]
email = ["", "", "", "", "", "", "", "", "", "", ""]


def nameemail(namelist):
    nameres = []
    emailres = []
    for a in namelist:
        if a in name:
            index = name.index(a)
            nameres.append(name[index])
            emailres.append(email[index])
    return nameres, emailres


def send_email(subject, to_email, message):
    sender = mail_user
    receivers = [to_email]  # 接收邮件，可设置为你的163邮箱或其他邮箱

    # 创建一个带附件的实例
    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = Header("会议邀请", 'utf-8')  # 发送者
    message['To'] = Header(to_email, 'utf-8')  # 接收者

    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(smtp_server, 25)  # 163邮箱服务器的端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)


# old
# def send_email(subject, receiver, message, attachment=None):
#     """
#
#     :param subject: 邮件主题
#     :param receiver: 收件人，可以是多个，用逗号分隔
#     :param message: 邮件正文，可以是纯文本，也可以是HTML
#     :param attachment: 附件，可以是多个，用逗号分隔
#
#     """
#     # 构造一个MIMEMultipart对象代表邮件，往里面加MIMEText作为邮件正文，加MIMEBase表示邮件附件。
#     msg = MIMEMultipart()
#     # 设置邮件头部信息
#     msg['From'] = mail_user
#     msg['To'] = receiver
#     msg['Subject'] = subject
#     # 如果传入的message不是HTML或者不存在的话，则把message当做纯文本发送
#     if os.path.exists(message) and message[-5:] == '.html':
#         file = open("%s" % (message), 'rb')
#         body = MIMEText(file.read(), 'html', 'utf-8')
#     else:
#         body = MIMEText(message, 'plain', 'utf-8')
#     msg.attach(body)
#
#     # 附件
#     if attachment is not None:
#         for file in attachment.split(','):
#             # 构造发送附件格式
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(open(file, 'rb').read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
#             msg.attach(part)
#
#     # 发送邮件
#     server = smtplib.SMTP_SSL(smtp_server)
#     server.ehlo()
#     # server.starttls()
#     server.login(mail_user, mail_pass)
#     server.sendmail(mail_user, receiver, msg.as_string())
#     server.quit()


def sendByName(namelist):
    nameres, emailres = nameemail(namelist)
    nums = len(nameres)

    for i in range(nums):
        subject = "彩云阁10月第三次会议纪要及会议分析数据"
        receiver = emailres[i]
        message = nameres[i] + "你好，本次会议已上传，可以访问 http://8.142.25.8  查看历史会议记录，相关记录和会上分析数据在附件"
        attachment = 'content.txt,emotion.xls'
        send_email(subject, receiver, message, attachment)


def sendAll(namelist):
    nameres = name
    emailres = email
    nums = len(nameres);
    for i in range(nums):
        subject = "彩云阁10月第三次会议纪要及会议分析数据"
        receiver = emailres[i]
        message = nameres[i] + "你好，本次会议已上传，可以访问 http://8.142.25.8  查看历史会议记录，相关记录和会上分析数据在附件"
        attachment = 'content.txt,emotion.xls'
        send_email(subject, receiver, message, attachment)


def sendInvite(namelist, url, theme, hoster, selectDay, link, number):
    for name, email in namelist.items():
        subject = theme + "会议邀请"
        message = name + "您好：\n  主持人" + hoster + "邀请您参加" + theme + "讨论班，会议时间为" + selectDay + "。\n您可以填写是否发言以及上传pdf等信息，为主持人更好安排会议流程,\n腾讯会议链接为：" + link + "\n会情分析系统链接为： " + url + "  (请在会情分析系统上传您的议程)\n" + "腾讯会议会议号为：  " + number + "\n感谢您的参与。"
        send_email(subject, email, message)


if __name__ == '__main__':
    send_email('会议邀请测试', '22210240325@m.fudan.edu.cn', "测试")
