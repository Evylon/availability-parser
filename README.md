# availability-parser
parse https://www.carlroth.com if status of an item is 'not available'

Small Parser with a bit config for checking the availability of an item at https://www.carlroth.com

The parser simply fetches the html code from a desired url and checks if it includes a desired substring. If the substring is not contained within the html code, a mail is send to a predefined mailadress.

Sender, receiver, mailserver and the observed url can be configured in a ```config.json``` with the following format:

```
{
  # username for logging into the mail account for sending a mail
  "mailuser": "parser@example.com",
  # password for the mail account
  "password": "secret",
  # mail that is put in the From: field of the mail
  "sender": "parser@example.com",
  # list ob receivers that the mail will be sent to 
  "receivers": ["user1@example.com", admin@nsa.gov],
  # url (or IP) of the smtp endpoint of the mail server. without "smtp." prefix!
  "smtphost": "example.com",
  # port of the smtp server. Usually 465 or 587
  "port": "465",
  # desired url of an item that is currently not available 
  "targetUrl": "https://www.example.com"
}
```

    
