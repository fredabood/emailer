# Emailer

A simple library to send emails via Python.

Cloned from [sohums' Emailify](https://github.com/sohums/Emailify) with the Spotify functionality stripped out.

### How To
```python
from emailer import Email, Session

# pass session to the Email class if you want to send more than one email
# otherwise the Email class will init a session and close it after sending
session = Session()

kwargs = dict(
    recipient='username@email.com',
    subject='subject',
    body='body text',
    files=['/path/to/file/one.ext', '/path/to/file/two.ext'],
)

email = Email(**kwargs)

email.send()
```
