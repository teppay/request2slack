request2slack
---

## Overview
This program listen to HTTP request and notice the request via Slack bot.
This can be used to test your API client, collect webhooks, or ...

## Requirements
- Python3
- Python libraries
  - Install using `pipenv` (OR see Pipfile)

## Install
### Direct ver.
```sh
# set environment arguments
$ export REQ2SLACK_BOTTOKEN=xoxb-xxx # Bot User OAuth Access Token
$ export REQ2SLACK_CHANNEL=request2slack # destination channel

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

# build
$ docker build -t request2slack ./

# run!
$ docker run --rm --env-file=.env request2slack
```