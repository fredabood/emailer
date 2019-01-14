# Emailer

A simple class to send emails via Python.

Cloned from [sohums' Emailify](https://github.com/sohums/Emailify) with the Spotify functionality stripped out.

```python
from emailer import Email, Session

# pass session to the Email class if you want to send more than one email
# otherwise the Email class will init a session and close it after sending
session = Session()

recipient = 'username@email.com'
subject = 'subject'
body = 'body text'
files = ['/path/to/file/one.ext', '/path/to/file/two.ext']

email = Email(
    recipient=recipient,
    body=body,
    subject=subject,
    files=files,
    session=session
)

email.send()
```
