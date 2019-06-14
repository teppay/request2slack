#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

from flask import Flask, request
from slack_notifier import Slack

from pprint import pprint


try:
    bot_token = os.environ['REQ2SLACK_BOTTOKEN']
except KeyError:
    raise Exception('Set Bot User OAuth Access Token to environment argument "REQ2SLACK_BOTTOKEN"')

try:
    channel = os.environ['REQ2SLACK_CHANNEL']
except KeyError:
    raise Exception('Set destination channel to environment argument "REQ2SLACK_CHANNEL"')


app = Flask(__name__)
slack = Slack(bot_token)

@app.route('/', methods=['GET', 'POST'])
def index():
    path = request.path
    if request.query_string:
        path += '?' + request.query_string.decode('utf-8')
    request_ = f'{request.method} {path}'

    headers = ''
    for name, value in request.headers:
        headers += f'{name}: `{value}`\n'

    attachments = [
        {
            'pretext': 'new Request!!',
            'title': 'Request',
            'text': request_,
            'color': 'good'
        },
        {
            'title': 'Headers',
            'text': headers,
            'color': 'good'
        },
    ]
    data = request.get_data()
    if data:
        attachments.append({
            'title': 'Body',
            'text': f'`{data.decode("utf-8")}`',
            'color': 'good',
        })

    info = ''
    info += f'Remote IP: `{request.remote_addr}`'
    attachments.append({
        'title': 'Info',
        'text': info,
        'fallback': 'new Request!',
        'footer': 'Send from request2slack',
        'ts': time.time()
    })

    slack.send_attachments_by_channel_name(channel, attachments)
    return 'Thanks for nice request!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')