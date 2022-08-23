import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from common.handler_logging import logger

logger = logger()


class SendMail:

    def __init__(self, file, user, pwd, mail_server, mail_sender, mail_receiver):
        self.user = user
        self.pwd = pwd
        self.file = file
        self.server = mail_server
        self.sender = mail_sender
        self.receiver = mail_receiver

        self.msg = MIMEMultipart()
        self.smtp = smtplib.SMTP()

        with open(self.file, 'rb') as f:
            self.read_file = f.read()

    # 邮件正文
    def send_mail(self):
        text = MIMEText(self.read_file, "html", "utf-8")
        self.msg.attach(text)

    # 邮件附件
    def accessory_mail(self, title, reports_name):

        self.msg["Subject"] = Header(title, "utf-8")
        file = MIMEText(self.read_file, "html", "utf-8")
        file['Content-Type'] = "application/octet-stream"
        file["Content-Disposition"] = "attachment; filename={}".format(reports_name)
        self.msg["To"] = '%s' % self.receiver
        self.msg.attach(file)

    # 连接发送邮件
    def connect_mail(self, title, reports_name, off=False):
        try:
            if off:
                self.send_mail()
                self.accessory_mail(title, reports_name)
                self.smtp.connect(self.server)
                self.smtp.login(self.user, self.pwd)
                self.smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
                self.smtp.quit()
                logger.info("email发送成功!")
            return

        except Exception as err:
            raise err


if __name__ == '__main__':
    pass
