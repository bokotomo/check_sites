# -*- coding: utf-8 -*-
import sys
import urllib.request as req
import urllib.parse as p
import urllib.error as err
from notification_manage import NotificationManager
import subprocess
import time
import setting

def main(args):
    """
    メイン関数
    """
    em = ErrorManager()
    for url in setting.check_sites_url:
        start = time.time()
        request = req.Request(url)
        try:
            response = req.urlopen(request)
            elapsed_time = time.time() - start
            time_str = "読み込み時間{0}".format(elapsed_time) + "[sec]"
            text = "*完了*\n%s" % (time_str)
        except err.URLError as e:
            elapsed_time = time.time() - start
            time_str = "読み込み時間{0}".format(elapsed_time) + "[sec]"
            text = "*「%s」からレスポンスがありません*\n%s\n--------------\n%s" % (url, e.reason, time_str)
        print(text)
        em.send_error_message_to_slack(text)

if __name__ == "__main__":
    main(sys.argv)

