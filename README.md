# xrp-notifier

A simple script that periodically checks an XRP account’s balance and sends an email notification if it exceeds 10 XRP.

## Installation

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install xrpl-py
```

## Running the script

```
XRP_NOTIFIER_GMAIL_ACCOUNT=<GMail account> \
XRP_NOTIFIER_GMAIL_PWD=<GMail pwd> \
XRP_NOTIFIER_SEND_TO=<Email recipient> \
XRP_NOTIFIER_XRP_ACCOUNT=<XRP account> \
python3 xrp-notifier.py
```

## Building a lambda package

On x86_64 machine,

```
./gen-lambda-package.sh
```

## AWS Lambda setup
At the bottom of the code tab, in runtime configuration, set handler to:

```
lambda.xrp_notifier.start_lambda
```

