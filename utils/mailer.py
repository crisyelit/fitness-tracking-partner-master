
from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string

import smtplib


class Mailer():

	@classmethod
	def sender(cls, **kwargs):

		msg_from = kwargs.get('from', settings.DEFAULT_FROM_EMAIL)
		msg_subject = kwargs.get('subject')
		template_name = kwargs.get('template_name')
		context = kwargs.get('context')
		to = kwargs.get('to')

		html_content = render_to_string(f'mailing/{template_name}.html', context)

		msg = EmailMultiAlternatives(msg_subject, "",
									 f"App <{msg_from}>", to)

		msg.attach_alternative(html_content, "text/html")
		msg.send()
