# Telegram

This Python library provides utility classes and methods
for interacting with the Telegram Bot API.
It simplifies sending messages, documents, and media groups,
as well as handling proxy configurations and authentication.


# Usage

Before using the utilities,
initialize the `Telegram` class with your bot's authentication information.

Mandatory parameters token and chat_id can be specified during initialization
of Telegram class or create `~/.telegram/token` and `~/.telegram/chat`
files with token and chat ID.
Parameters specified at initialization in priority

```python
from telegram import Telegram

# Initialize Telegram
telegram = Telegram(token='YOUR_BOT_TOKEN', chat_id='YOUR_CHAT_ID')

# Sending a text message
telegram.send_message("Hello, World!")

# Sending a document
telegram.send_document('path/to/document.pdf', caption="Here is the document.")

# Sending a media group
document_paths = ['path/to/photo1.jpg', 'path/to/photo2.jpg']
telegram.send_media_group(document_paths, caption="Check out these photos!", media_type='photo')
```

## Proxy Configuration
The library supports proxy configuration using the Proxy and ProxyFile classes:

```python
from telegram import Telegram, Proxy

proxy = Proxy(login='your_login', password='your_password', ip='proxy_ip', port='proxy_port')

# Initialize Telegram via proxy

telegram = Telegram(token='YOUR_BOT_TOKEN', chat_id='YOUR_CHAT_ID', proxy=proxy)
```

Or you can use the `~/.telegram/proxy.json` file with the configuration:

```json
{
  "login": "your_login",
  "password": "your_password",
  "ip": "proxy_ip",
  "port": "proxy_port"
}
```
