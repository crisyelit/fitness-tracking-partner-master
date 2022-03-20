from celery import shared_task

from utils.mailer import Mailer


@shared_task
def sendEmail(msg_subject, template_name, context, to):
	Mailer().sender(subject=msg_subject, template_name=template_name, context=context, to=to)
