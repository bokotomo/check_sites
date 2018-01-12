# -*- coding: utf-8 -*-
import sys
from os import path
import urllib.request
import json
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.utils import formataddr
from email.header import Header
import setting

class NotificationManager:
    """
    メールとslackへテキストを送信するクラス
    """
    def send_error_message_to_mail(self, text):
        """
        メールを送る
        """
        to = setting.slack_bot_email_to
        subject = "通知"
        self.__send_via_gmail(to, subject, text)

    def send_error_message_to_slack(self, text):
        """
        スラックにメッセージを送る
        """
        url = setting.slack_bot_url
        method = "POST"
        param = {
            "payload": {
                'channel': setting.slack_bot_channel,
                'username': setting.slack_bot_username,
                'text': text
            }
        }
        self.__send_http_request(url=url, method=method, param=param)

    def __send_via_gmail(self, to, subject, text):
        """
        smtpにてメール送信
        """
        from_addr = setting.SMTP_GMAIL_FROM
        message = self.__create_message(to, from_addr, subject, text)
        smtp = smtplib.SMTP(setting.SMTP_GMAIL_HOST, setting.SMTP_GMAIL_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(from_addr, setting.SMTP_GMAIL_PASS)
        smtp.sendmail(from_addr, [to], message.as_string())
        smtp.close()

    def __create_message(self, to, from_addr, subject, body):
        """
        メッセージをエンコードして返す
        """
        encoding = 'utf-8'
        sender_name = Header(from_addr, encoding).encode()
        recipient_name = Header(from_addr, encoding).encode()
        message = MIMEText(body.encode(encoding), 'plain', _charset=encoding)
        message['Subject'] = Header(subject, encoding )
        message['From'] = formataddr((sender_name, from_addr))
        message['To'] = formataddr((recipient_name, to))
        message['Date'] = formatdate()
        return message

    def __send_http_request(self, url="", method="", param={}):
        """
        httpリクエストを送る
        """
        response_body = ""
        encoded_param = urllib.parse.urlencode(param).encode(encoding='utf-8')
        headers = {"Content-Type": "application/json"}
        json_data = json.dumps(param).encode("utf-8")
        with urllib.request.urlopen(url=url, data=encoded_param) as response:
            response_body = response.read().decode("utf-8")
            return response_body

