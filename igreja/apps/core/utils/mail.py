import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.template.loader import get_template

logger = logging.getLogger(__name__)


@dataclass
class Attachment:
    filename: str
    content: str
    mimetype: str


class Mailer:
    def __init__(self):
        self.connection = get_connection()
        self.from_email = settings.EMAIL_HOST_FROM

    def execute(
        self,
        subject: str,
        template: str,
        context: Dict[str, Any],
        to_emails: List[str],
        attachments: List[Attachment] | None = None,
    ):
        logger.warning("remover a linha abaixo quando tiver em produção")
        to_emails = ["danilo.nascimento.ibm@gmail.com"]
        logger.info(
            "send message '{}' for '{}' using template '{}'".format(
                subject, to_emails, to_emails
            )
        )
        messages = self.__generate_messages(
            subject, template, context, to_emails, attachments
        )
        self.__send_mail(messages)

    def __send_mail(self, mail_messages):
        self.connection.open()
        self.connection.send_messages(mail_messages)
        self.connection.close()

    def __generate_messages(
        self,
        subject: str,
        template: str,
        context: Dict[str, Any],
        to_emails: List[str],
        attachments: List[Attachment] | None = None,
    ):
        messages = []
        message_template = get_template(template)
        for recipient in to_emails:
            message_content = message_template.render(context)
            message = EmailMessage(
                subject,
                message_content,
                to=[recipient],
                from_email=self.from_email,
            )

            if attachments is not None:
                for attachment in attachments:
                    message.attach(
                        filename=attachment.filename,
                        content=attachment.content,
                        mimetype=attachment.mimetype,
                    )

            message.content_subtype = "html"
            messages.append(message)

        return messages
