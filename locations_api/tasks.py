from celery import shared_task

import logging

from django.urls import reverse
from django.core.mail import send_mail
from django_learn.celery import app



@app.task
def country_created(mail):
    print("sending massage country created")
    message = 'Congratulations! Your country was successfully added!'
    send_mail('Country created', message, 'admin@world.com', [mail])


@app.task
def country_chanched(mail, name, link_for_view_country):
    message = f'Your country {name} was changed./n You can view changes at {link_for_view_country}'
    send_mail('Country chanched', message, 'admin@warld.com', [mail])
