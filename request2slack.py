#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import yaml

from flask import Flask, request
from slack_notifier import Slack
from argparse import ArgumentParser


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

with open('./blacklist.yaml', 'r') as blacklist_yaml:
    blacklist = yaml.load(blacklist_yaml, Loader=yaml.SafeLoader)


def replace_specialchars(s):
    has_mal_chars = False
    mal_chars = ['`', '\n']
    for c in mal_chars:
        if c in s:
            has_mal_chars = True
            s = s.replace(c, '--')
    if has_mal_chars:
        s = s + ' (special chars(backquotes, \\n) are replaced with "--")'
    print(s)

    return s


@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if blacklist['ua'] and request.headers.get('User-Agent') in blacklist['ua']:
        return 'Thanks for nice request!'

    path = request.path
    if request.query_string:
        path += '?' + request.query_string.decode('utf-8')
    request_ = replace_specialchars(f'{request.method} {path}')

    message = f'Request: `{request_}`\n'

    # list of headers that are sent to slack
    headers = [
        'User-Agent',
    ]

    for h in headers:
        value = request.headers.get(h)
        if value:
            message += f'{replace_specialchars(h)}: `{replace_specialchars(value)}`\n'

    ip = request.headers.get('X-Real-IP')
    if not ip:
        ip = request.remote_addr

    message += f'Remote IP: `{ip}`\n'

    data = request.get_data()
    if data:
        message += f'Data: `{data}`\n'

    attachments = [
        {
            'pretext': 'new Request!!',
            'text': message,
            'color': 'good',
            'fallback': 'new Request!',
            'footer': 'Send from request2slack',
            'ts': time.time()
        },
    ]

    slack.send_attachments_by_channel_name(channel, attachments)
    return 'Thanks for nice request!'

if __name__ == '__main__':
    arg_parse = ArgumentParser()
    arg_parse.add_argument('--port', '-p', type=int, default=80, help='listening port')
    args = arg_parse.parse_args()

    app.run(host='0.0.0.0', port=args.port)