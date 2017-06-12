import smtplib
from email.mime.text import MIMEText
import base64
from cognub.botmail.recipients import propmix_recepients, test_recepients
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

class BotMail():
    bot = 'botmsg.noreply@cognub.com'
    code = 'Q29nbnViITIz'
    smtpid = 'smtp.gmail.com:587'
    signature = 'Regards,\r\nCognub development team.\r\n\r\n**do not reply, this is an auto generated email.**\r\n'

    def __init__(self):
        pass

    def _login(self):
        self.server = smtplib.SMTP(self.smtpid)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.bot, base64.b64decode(self.code))

    def send_mail(self, subject, text, to=propmix_recepients):

        self._login()
        msg = MIMEText(text + ' \r\n\r\n%s' % (self.signature))
        msg['Subject'] = subject
        msg['From'] = self.bot
        msg['To'] = ",".join(to)
        self.server.sendmail(self.bot, to, msg.as_string())
    def send_mailattach(self, subject, text,attach,filename, to=propmix_recepients):
        self._login()
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.bot
        msg['To'] = ",".join(to)
        signature = 'Regards,\r\nCognub development team.\r\n\r\n**do not reply, this is an auto generated email.**\r\n' 
        body = "Hey \n This is an alert for offmarket properties based on your subscription \r\n\r\n%s "% (signature)
        msg.attach(MIMEText(body, 'plain'))
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attach).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
         
        msg.attach(part)
        self.server.sendmail(self.bot, to, msg.as_string())
        
if __name__ == "__main__":
    botmail = BotMail()
    botmail.send_mail("Test Mail", "This is an automated test mail, kindly ignore", to=test_recepients)

