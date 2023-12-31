import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
from email.utils import parseaddr
import smtplib


smtp_server = 'smtp.exmail.qq.com'
smtp_port = '465'
mail_user = '21210240113@m.fudan.edu.cn'
mail_pass = 'fDu150031'
name = ["吴斌","赵一飞","郭茹萍","王帅宇","顾珍桢","姚鑫玉","包智超","王朔","苏永甫","谢万超","徐铮"]
email = ["18110240013@fudan.edu.cn","19110240026@fudan.edu.cn","20212010126@fudan.edu.cn","20212010031@fudan.edu.cn","20210240352@fudan.edu.cn","20210240125@fudan.edu.cn","21210240113@m.fudan.edu.cn","21210240340@m.fudan.edu.cn","22210240271@m.fudan.edu.cn","22210240325@m.fudan.edu.cn","22210240335@m.fudan.edu.cn"]

def nameemail(namelist):
    nameres = []
    emailres = []
    for a in namelist:
        if a in name:
            index = name.index(a)
            nameres.append(name[index])
            emailres.append(email[index])
    return nameres, emailres


def send_email(subject, receiver, message, attachment=None):
    """

    :param subject: 邮件主题
    :param receiver: 收件人，可以是多个，用逗号分隔
    :param message: 邮件正文，可以是纯文本，也可以是HTML
    :param attachment: 附件，可以是多个，用逗号分隔

    """
	# 构造一个MIMEMultipart对象代表邮件，往里面加MIMEText作为邮件正文，加MIMEBase表示邮件附件。
    msg = MIMEMultipart()
    # 设置邮件头部信息
    msg['From'] = mail_user
    msg['To'] = receiver
    msg['Subject'] = subject
	# 如果传入的message不是HTML或者不存在的话，则把message当做纯文本发送
    if os.path.exists(message) and message[-5:] == '.html':
        file = open("%s" % (message), 'rb')
        body = MIMEText(file.read(), 'html', 'utf-8')
    else:
        body = MIMEText(message, 'plain', 'utf-8')
    msg.attach(body)

    # 附件
    for file in attachment.split(','):
        # 构造发送附件格式
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    # 发送邮件
    server = smtplib.SMTP_SSL(smtp_server)
    server.ehlo()
    # server.starttls()
    server.login(mail_user, mail_pass)
    server.sendmail(mail_user, receiver.split(','), msg.as_string())
    server.quit()



def sendByName(namelist):
    nameres, emailres = nameemail(namelist)
    nums =  len(nameres);
    for i in range(nums):
        subject = "彩云阁10月第三次会议纪要及会议分析数据"
        receiver = emailres[i]
        message = nameres[i] + "你好，本次会议已上传，可以访问 http://8.142.25.8  查看历史会议记录，相关记录和会上分析数据在附件"
        attachment = 'content.txt , emotion.xls'
        send_email(subject, receiver, message, attachment)

def sendAll(namelist):
    nameres = name
    emailres = email
    nums =  len(nameres);
    for i in range(nums):
        subject = "彩云阁10月第三次会议纪要及会议分析数据"
        receiver = emailres[i]
        message = nameres[i] + "你好，本次会议已上传，可以访问 http://8.142.25.8  查看历史会议记录，相关记录和会上分析数据在附件"
        attachment = 'content.txt , emotion.xls'
        send_email(subject, receiver, message, attachment)


# if __name__ == '__main__':
#     namelist = ['包智超']
#     sendByName(namelist)