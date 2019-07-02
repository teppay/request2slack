request2slack
---

## Overview
This program listen to HTTP request and notice the request via Slack bot.
This can be used to test your API client, collect webhooks, or ...

## Requirements
- Python3
- Python libraries
  - Install using `pipenv` (OR see Pipfile)

## Usage
If this application is running on 80/tcp on your server,

```sh
$ curl http://<your server>/
```

![screenshot](https://github.com/teppay/request2slack/blob/images/screenshot.png?raw=true)

## Install
### Direct ver.
```sh
# set environment arguments
$ export REQ2SLACK_BOTTOKEN=xoxb-xxx # Bot User OAuth Access Token
$ export REQ2SLACK_CHANNEL=request2slack # destination channel

# edit blacklist
$ mv blacklist.yaml.example blacklist.yaml
$ vi blacklist.yaml

# install dependencies
$ pipenv install

# run!
$ pipenv run start
```

### Docker ver.
```sh
# edit .env
$ cp .env.example .env
$ vi .env

# edit blacklist
$ mv blacklist.yaml.example blacklist.yaml
$ vi blacklist.yaml

# build
$ docker build -t request2slack ./

# run!
$ docker run --rm --env-file=.env -p '80:80' request2slack
```

## Option
`-p, --port`: listening port, Default=80

## Features
### Notification Blacklist
If you want to exclude specific User Agents from notifications, Edit `blacklist.yaml`.