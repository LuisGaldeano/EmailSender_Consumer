import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate, make_msgid
from smtplib import SMTP

from jinja2 import Environment, FileSystemLoader
from uuid import uuid4

from settings.settings import FROM_EMAIL, FROM_EMAIL_PASSWORD, FROM_EMAIL_NAME


class EmailGenerator:
    template = None
    username = None
    client_email = None
    mail_uuid = None
    address = None

    def __init__(
        self,
        template: str,
        username: str = None,
        client_email: str = None,
        address: str = None
    ):
        self.output_path = template.replace(':', '/')
        self.template_path = f"templates/{self.output_path}"

        if os.path.isdir(self.template_path):
            if not os.path.isdir(f"{self.template_path}/email"):
                raise ValueError('Not valid notification type')
        else:
            raise ValueError(f"{template} is not valid template")

        if not client_email:
            raise ValueError("Needed client_email parameter")

        self.username = username
        self.client_email = client_email
        self.address = address

    def save_mail(self, rendered_content: str, rendered_subject):
        self.mail_uuid = uuid4()
        if not os.path.isdir("sent"):
            os.mkdir("sent")
        if not os.path.isdir(f"sent/{self.output_path}"):
            os.mkdir(f"sent/{self.output_path}")
        with open(
            f"sent/{self.output_path}/{self.client_email}-{rendered_subject}-{self.mail_uuid}.html", "w"
        ) as save_file:
            save_file.write(rendered_content)
            save_file.close()

    def create_mail(self):
        with open(f"{self.template_path}/email/content.html", "r") as email_template:
            content = email_template.read()
        with open(f"{self.template_path}/email/subject.txt", "r") as email_subject:
            subject = email_subject.read()

        content_template = Environment(loader=FileSystemLoader('templates/')).from_string(content)
        render_content = content_template.render(extra=self.username, custom_data=self.address)
        subject_template = Environment(loader=FileSystemLoader('templates/')).from_string(subject)
        render_subject = subject_template.render(extra=self.username, custom_data=self.address)

        message = MIMEMultipart()
        message['Subject'] = render_subject
        message['From'] = formataddr((FROM_EMAIL_NAME, FROM_EMAIL))
        message['To'] = self.client_email
        message['Date'] = formatdate(localtime=True)
        message['Message-ID'] = make_msgid(domain="luisgaldeano.com")
        message.attach(MIMEText(render_content, "html"))
        msg_body = message.as_string()

        return msg_body, render_content, render_subject

    def send_mail(self) -> list:
        try:
            msg_body, render_content, render_subject = self.create_mail()
            self.save_mail(rendered_content=render_content, rendered_subject=render_subject)
            server = SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(FROM_EMAIL, FROM_EMAIL_PASSWORD)
            server.sendmail(FROM_EMAIL, self.client_email, msg_body)

            server.quit()
            return [True, f'The email has been sent to {self.client_email}']
        except Exception as ex:
            return [False, str(ex)]

    def send(self):
        email_result = self.send_mail()
        if not email_result:
            return [False, 'Email has not been sent']

        return email_result
