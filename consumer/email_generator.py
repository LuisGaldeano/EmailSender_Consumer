import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate, make_msgid
from smtplib import SMTP

from jinja2 import Environment, FileSystemLoader
from uuid import uuid4

from consumer.settings.settings import FROM_EMAIL_NAME, FROM_EMAIL, FROM_EMAIL_PASSWORD


class EmailGenerator:
    template_path = None
    extra_parameters = None
    to_email = None
    mail_uuid = None
    custom_data = None

    def __init__(
        self,
        notification_template: str,
        extra_parameters: dict = None,
        to_email: str = None,
        custom_data: dict = None
    ):
        template_path = f"templates/{notification_template.replace(':', '/')}"

        if os.path.isdir(template_path):
            if not os.path.isdir(f"{template_path}/email"):
                raise ValueError('Not valid notification type')
        else:
            raise ValueError(f"{notification_template} is not valid template")

        if not to_email:
            raise ValueError("Needed to_email parametrer")

        self.template_path = f'{template_path}'
        self.extra_parameters = extra_parameters
        self.to_email = to_email
        self.custom_data = custom_data

    def save_mail(self, rendered_content: str, rendered_subject):
        self.mail_uuid = uuid4()
        if not os.path.isdir(f"sent/{self.template_path}"):
            os.mkdir(f"sent/{self.template_path}")
        with open(
            f"sent/{self.template_path}/{self.to_email}-{rendered_subject}-{self.mail_uuid}.html", "w"
        ) as save_file:
            save_file.write(rendered_content)
            save_file.close()

    def create_mail(self):
        with open(f"{self.template_path}/email/content.html", "r") as email_template:
            content = email_template.read()
        email_template.close()
        with open(f"{self.template_path}/email/subject.txt", "r") as email_subject:
            subject = email_subject.read()
        email_subject.close()

        content_template = Environment(loader=FileSystemLoader('templates/')).from_string(content)
        render_content = content_template.render(extra=self.extra_parameters, custom_data=self.custom_data)
        subject_template = Environment(loader=FileSystemLoader('templates/')).from_string(subject)
        render_subject = subject_template.render(extra=self.extra_parameters, custom_data=self.custom_data)

        message = MIMEMultipart()
        message['Subject'] = render_subject
        message['From'] = formataddr((FROM_EMAIL_NAME, FROM_EMAIL))
        message['To'] = self.to_email
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
            server.sendmail(FROM_EMAIL, self.to_email, msg_body)

            server.quit()
            return [True, f'The email has been sent to {self.to_email}']
        except Exception as ex:
            return [False, str(ex)]

    def send(self):
        email_result = self.send_mail()
        if not email_result:
            return [False, 'Email has not been sent']

        return email_result
