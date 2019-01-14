# Emailer

A simple library to send emails via Python.

Cloned from [sohums' Emailify](https://github.com/sohums/Emailify) with the Spotify functionality stripped out.

### Example
```python
from emailer import Email, Session

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
