# Emailer

A simple library to send emails via Python.

Cloned from [sohums' Emailify](https://github.com/sohums/Emailify) with the Spotify functionality stripped out.

### Example
```python
from emailer import Email

user = dict(
    username='your@email.com',
    password='yourpass',
)

email = Email(**user)

kwargs = dict(
    recipient='recipient@email.com',
    subject='subject',
    body='body text',
    files=['/path/to/file/one.ext', '/path/to/file/two.ext'],
)

email.send(**kwargs)

kwargs = dict(
    folder='INBOX',
    queries=['SINCE 05-Jul-2014'],
)

messages = email.read(**kwargs)
```
