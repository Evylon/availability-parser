#!/usr/bin/python3  

import urllib.request
import smtplib, ssl
import os, os.path
import json
from datetime import datetime

def main():
    mailconfig = loadMailConfig()
    if not mailconfig:
        exit(-1)

    # reference url for an item that is available
    # url = 'https://www.carlroth.com/de/de/buersten-reinigungsschwaemme/reinigungsbuerste-rotilabo/p/xk76.1'
    # desired url of an item that is currently not available
    url = 'https://www.carlroth.com/de/de/loesungen-fuer-die-gram-faerbung/ethanol-96-%25-vergaellt/p/t171.4'

    if not isAvailable(url):
        Log.log(Log.info, 'item is not available')
    else:
        Log.log(Log.info, 'HURRAY! THE ITEM IS AVAILABLE!')
        sendMail(mailconfig, url)

def isAvailable(url):
    # if this string is in the html body, the item is unavailable
    target = '<divclass="stock-container"><spanclass="stockstock--X"></span>Nichtverf'
    # fetch html from url and remove newline and whitespace
    html = urllib.request.urlopen(url).read()
    html = str(html).replace(' ', '').replace('\\n', '')

    return not target in html

def loadMailConfig():
    # constants
    configFilename = 'mailconfig.json'
    configFields = ['mailuser', 'password', 'sender', 'receiver', 'smtphost', 'port']
    # check if file exists
    if not os.path.isfile(configFilename):
        Log.log(Log.error, 'File "{0}" not found. Creating empty config file, please fill in the empty fiels'.format(configFilename))
        createEmptyMailconfig(configFilename, configFields)
        return None
    # try loading the mailconfig
    with open(configFilename, 'r') as configFile:
        try:
            mailconfig = json.load(configFile)
        except json.decoder.JSONDecodeError:
            Log.log(Log.error, 'Corrupt mailconfig. Creating empty config file, please fill in the empty fiels')
            createEmptyMailconfig(configFilename, configFields)
            return None
    # check all fields exists
    for key in configFields:
        if not key in mailconfig:
            Log.log(Log.error, 'File "mail.config" incomplete. {0} is missing. Renaming old config file and generating new config'.format(key))
            createEmptyMailconfig(configFilename, configFields)
            return None
    # return valid mailconfig
    return mailconfig

def createEmptyMailconfig(filename, configFields):
    saveOldMailconfig(filename)
    with open(filename, 'w') as configFile:
        json.dump({field: '' for field in configFields}, configFile)

def saveOldMailconfig(filename):
    if not os.path.exists(filename):
        return
    targetFileName = '{0}_old.json'.format(os.path.splitext(filename)[0])
    if os.path.exists(targetFileName):
        os.remove(targetFileName)
    os.rename(filename, targetFileName)

def sendMail(mailconfig, url):
    message = """\
Subject: The item you are obeserving is available!

Hi {receiver},

the item you are obeserving on
{url}
is now available!

Kind regards
Your availability parser
""".format(receiver = mailconfig['receiver'], url = url)

    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to server and send email
    server = smtplib.SMTP(mailconfig['smtphost'], mailconfig['port'])
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(mailconfig['mailuser'], mailconfig['password'])
    server.sendmail(mailconfig['sender'], mailconfig['receiver'], message)
    # with smtplib.SMTP_SSL(mailconfig['smtphost'], mailconfig['port'], context=context) as server:
    #     server.login(mailconfig['mailuser'], mailconfig['password'])
    #     server.sendmail(mailconfig['sender'], mailconfig['receiver'], message)

def getTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Log:
    error = 'ERROR'
    info = 'INFO'

    @staticmethod
    def log(tag, message):
        print('[{tag}] {time} {message}'.format(time = getTime, tag = tag, message = message))

if __name__ == "__main__":
    main()
