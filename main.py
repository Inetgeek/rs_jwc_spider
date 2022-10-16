#!/usr/bin/env python3
# -*- coding: utf-8 -*

from rsvcrack import RSV
import requests
from loguru import logger
import re
import utils as tool

config = {
    "text": r'<td class="llink">(.*)</td>',
    "time": r'<td width="14%">(.*)</td>',
    "cid": r"href='(.*)' target",
    "date": r'(\d{4}-\d{1,2}-\d{1,2})',
    "link": r"href='(.*)' target",
    "title": r"title='(.*)'>",
}

admin_data = {
    "token": "xxx",
    "title": "【机器人异常】\n\n",
    "send_to": "管理员QQ"
}

group_data = {
    "token": "xxx",
    "title": "【教务处通知】\n\n",
    "send_to_group": "QQ群"
}


class Notice(object):
    def __init__(self, _url, _gurl):
        self.url = _url
        self.gurl = _gurl
        self.get = None
        self.ck = None

    def getCookies(self) -> None:
        try:
            self.get = RSV(self.gurl)
            self.ck = self.get.crack()
            logger.success(f"cookies: {self.ck}")
        except Exception as e:
            admin_data["content"] = "老大，好像不能拿到cookie了..."
            requests.post('http://127.0.0.1:8080/report', json=admin_data)
            logger.error(f"获取cookies失败！" + str(e))

    def getRequest(self):
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            f"Referer": self.url,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\""
        }
        self.getCookies()
        if self.ck is None:
            logger.error("cookies is empty, can't get a request!")
            return None
        else:
            rep = requests.get(self.url, headers=header, cookies=self.ck)
            logger.success("the request send successfully!")
            rep.encoding = "utf-8"
            return rep.text

    def parseByRe(self):
        set_mail_data = []
        set_db_data = []
        set_qq_data = ""
        cid = ""
        link = ""
        msg = ""
        post_date = ""
        date = tool.Date()
        sql = tool.MySQL("jwc")
        try:
            html = self.getRequest()
            if html is None:
                pass
            else:
                get_cid = sql.getData(str(date.getToday()))
                print(date.getToday())
                print(get_cid)

                list_text = re.findall(config["text"], html)
                list_time = re.findall(config["time"], html)
                i = 1
                flag = 0
                for text, time in zip(list_text, list_time):
                    if str(re.findall(config["date"], time)[0]) == str(date.getToday()):  # 如果是今天通知
                        if re.findall(config["cid"], text)[0][7:19] in get_cid:  # 如果该条信息已存在
                            pass
                        else:  # 如果该条信息从未写入
                            cid = re.findall(config["cid"], text)[0][7:19]
                            link = "https://" + self.gurl + str(re.findall(config["link"], text)[0])
                            msg = str(re.findall(config["title"], text)[0])
                            post_date = str(re.findall(config["date"], time)[0])
                            print(f"[{i}] (cid=" + cid + ", link=" + link + ", title=" + msg + ", post_date=" + post_date + ")")
                            set_mail_data.append(msg + ": " + link)
                            set_qq_data = set_qq_data + msg + ": " + link + "\n\n"
                            set_db_data.append((cid, msg, post_date, link))
                            flag = 1
                            i = i + 1
                    else:
                        pass

                print("set_mail_data: " + str(set_mail_data))
                print("set_qq_data: " + str(set_qq_data))
                print("set_db_data: " + str(set_db_data))

                if flag:

                    """写入数据库"""
                    res = sql.setData(set_db_data)
                    if res:
                        pass
                    else:
                        admin_data["content"] = "老大，好像数据库报错了..."
                        requests.post('http://127.0.0.1:8080/report', json=admin_data)

                    """发邮件"""
                    tool.senMail(["xxx@foxmail.com"], set_mail_data)

                    """推送到QQ"""
                    group_data["content"] = set_qq_data + "[CQ:at,qq=all]"
                    requests.post('http://127.0.0.1:8080/report', json=group_data)

                else:
                    admin_data["content"] = "老大，今天没有新通知哦..."
                    requests.post('http://127.0.0.1:8080/report', json=admin_data)

                # 关闭数据库链接
                sql.closeDB()

        except Exception as e:
            logger.error(e)
            pass


if __name__ == '__main__':
    url = "https://jwc.xxx.edu.cn/xxx/list.htm"
    gurl = "jwc.xxx.edu.cn"

    n = Notice(url, gurl)
    n.parseByRe()
