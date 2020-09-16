from email.mime.text import MIMEText
import smtplib


class MailUtil(object):

    host = 'smtp.qq.com'
    sender = '1462232055@qq.com'
    user = '1462232055@qq.com'
    password = 'rfnupleuewmeiedb'

    def __init__(self, to_mail, cc_mail=None):
        self.__to_mail = to_mail
        self.__cc_mail = cc_mail
        self.__msg = None

    def mail_content(self, title, content, subtype=None, charset=None):
        if subtype is not None and charset is not None:
            self.__msg = MIMEText(content, subtype, charset)
        else:
            self.__msg = MIMEText(content)
        self.__msg['Subject'] = title
        self.__msg['From'] = self.sender
        self.__msg['To'] = ';'.join(self.__to_mail)
        if self.__cc_mail is not None:
            self.__msg['Cc'] = ';'.join(self.__cc_mail)
        return self

    def send(self):
        server = smtplib.SMTP_SSL(self.host, 465, timeout=2)
        server.login(self.sender, self.password)
        if self.__cc_mail is not None:
            server.sendmail(self.sender, self.__to_mail + self.__cc_mail, self.__msg.as_string())
        else:
            server.sendmail(self.sender, self.__to_mail, self.__msg.as_string())
