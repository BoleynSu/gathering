#!/usr/bin/env python3
import os, sys, time, subprocess, smtplib, imapclient, email, uu, io, pyzmail, ssl
from datetime import datetime
from email.mime.text import MIMEText
from conf import EMAIL
from conf import USER
from conf import PASSWD
from conf import onError

def check():
  global server
  server.select_folder('INBOX')
  messages = server.search(["TO", EMAIL])
  response = server.fetch(messages, ['RFC822'])
  for msg_id, data in response.items():
      msg = email.message_from_bytes(data[b'RFC822'])
      msg = pyzmail.PyzMessage.factory(msg)
      frm = msg.get_address("from")[1]
      charset = msg.text_part.charset
      if not charset:
        charset = "utf-8"
      lines = msg.text_part.get_payload().decode(charset).split("\r\n")
      for line in lines:
        if line:
          cmd = [s.strip() for s in line.split(";")]
          subprocess.call([os.path.dirname(__file__) + "/cmd.py"] + [frm] + cmd)
          break
      server.delete_messages([msg_id])
      server.expunge()

server = None

while True:
  try:
    check()
  except:
    connected = False
    iteration = 0
    while (not connected) and (iteration < 20):
      iteration = iteration + 1
      try:
        if server == None:
          print("connecting...")
        else:
          print("reconnecting...")
        server = imapclient.IMAPClient("imap.gmail.com", use_uid=True, ssl=True, ssl_context=ssl.create_default_context(cafile="/etc/pki/tls/certs/ca-bundle.crt"))
        server.login(USER, PASSWD)
        check()
        connected = True
      except Exception as e:
        print(e)
        time.sleep(30)
    if not connected:
      onError()
      break
  time.sleep(5)

