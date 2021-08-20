import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from User import User
ENABLE_EMAIL = True
FROM_EMAIL = 'gabriel.ruiseco.utt@gmail.com'
FROM_EMAIL_PASSWORD = 'ygepfbvmhpqxuyaa'
serverRoute = "https://orionserver.herokuapp.com/"
apiRoute = "https://orionserver.herokuapp.com/api"

class ApiConsumption:

    user = User()

    @staticmethod
    def login():
        payload = {'email': ApiConsumption.user.email, 'password': ApiConsumption.user.password}
        req = requests.post(serverRoute+"login", params=payload)
        response = req.json()
        req2 = requests.get(serverRoute+"uid", params={'email': 'mail@mail.com'})
        token = response['token']
        ApiConsumption.user.saveToken(token)
        ApiConsumption.user.saveID(req2.text)
        return ApiConsumption.user.getToken()

    @staticmethod
    def uploadFile(name):
        try:
            files = {'image': open(name, 'rb')}
            req = requests.post(serverRoute+"mongocreate", files=files)
            result = req.json()
            print(result)
            try:
                params = {"imageUrl": serverRoute +"serveFile?photo="+result['photo'], "faceSetToken": "b4f325f3e99b63ae39ef93ae73e2e118"}
                req2 = requests.post(serverRoute+"search", params=params)
                print(req2.text)
                result2 = req2.json()
                if result2['confidence'] > 90:
                    print('abriendo')
                else:
                    print('negado')
            except Exception as err:
                print(err)
            return result
        except Exception as err:
            print(err)

        def send_email_notification():
            if ENABLE_EMAIL:
                sender = EmailSender(FROM_EMAIL, FROM_EMAIL_PASSWORD)
                email = Email(
                    sender,
                    'Video Doorbell',
                    'Notification: A visitor is waiting',
                    'A new visitant is added to your gallery'
                )
                email.send(ApiConsumption.user.email)

        def ring_doorbell(pin):
            send_email_notification()

class EmailSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class Email:
    def __init__(self, sender, subject, preamble, body):
        self.sender = sender
        self.subject = subject
        self.preamble = preamble
        self.body = body

    def send(self, to_email):
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = self.subject
        msgRoot['From'] = self.sender.email
        msgRoot['To'] = to_email
        msgRoot.preamble = self.preamble
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        msgText = MIMEText(self.body)
        msgAlternative.attach(msgText)
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(self.sender.email, self.sender.password)
        smtp.sendmail(self.sender.email, to_email, msgRoot.as_string())
        smtp.quit()