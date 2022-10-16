import pymysql as m
import datetime
from loguru import logger
import smtplib  # 引用控值邮箱发送邮件的库
from email.mime.text import MIMEText  # 引入mail.mime的MIMEText 类来实现支持HTML格式的邮件（email.mime是smtplib模块邮件内容主体的扩展）
from email.mime.multipart import MIMEMultipart  # 引进MIMEMultipart可以同时添加正文和附件


def senMail(receiver, content):
    # 设置基础内容
    config = {
        "admin": "发送者邮箱",
        "key": "发送者邮箱服务器密钥",
        "theme": "【订阅推送】 教务处通知"
    }
    send_msg = ""
    i = 1
    for x in content:
        send_msg = send_msg + "<br/><br/>" + f"[{i}] " + x
        i = i + 1
    print(send_msg)

    msg = MIMEMultipart()
    mail_msg = '''
    <div>
    <includetail>
        <div style="font:Verdana normal 14px;color:#000;">
            <div style="position:relative;">
                <style>
                    .title_bold {
                        font-family: PingFangSC-Medium, "STHeitiSC-Light", BlinkMacSystemFont, "Helvetica", "lucida Grande", "SCHeiti", "Microsoft YaHei";
                        font-weight: bold;
                    }

                    .mail_bg {
                        background-color: #F5F5F5;
                    }

                    .mail_cnt {
                        padding: 60px 0 160px;
                        max-width: 700px;
                        margin: auto;
                        color: #2b2b2b;
                        -webkit-font-smoothing: antialiased;
                    }

                    .mail_container {
                        background-color: #fff;
                        margin: auto;
                        max-width: 702px;
                        border-radius: 2px;
                    }

                    .eml_content {
                        padding: 0 50px 30px 50px;
                        font-family: "Helvetica Neue", "Arial", "PingFang SC", "Hiragino Sans GB", "STHeiti", "Microsoft YaHei", sans-serif;
                    }

                    .mail_header {
                        text-align: right;
                    }

                    .top_line_left {
                        width: 88%;
                        height: 3px;
                        background-color: #2984EF;
                        float: left;
                        margin-right: 1px;
                        border-top-left-radius: 2px;
                        display: inline-block;
                    }

                    .top_line_right {
                        width: 12%;
                        height: 3px;
                        background-color: #8BD5FF;
                        float: right;
                        border-top-right-radius: 2px;
                        margin-top: -3px;
                    }

                    .main_title {
                        font-size: 16px;
                        line-height: 24px;
                    }

                    .main_subtitle {
                        line-height: 28px;
                        font-size: 16px;
                        margin-bottom: 12px;
                    }

                    .item_level_1 {
                        margin-top: 60px;
                    }

                    .item_level_2 {
                        margin-top: 40px;
                    }

                    .level_1_title {
                        font-size: 16px;
                        line-height: 28px;
                    }

                    .level_2_title {
                        font-size: 14px;
                        line-height: 28px;
                        font-weight: 600;
                    }

                    .item_txt {
                        font-size: 14px;
                        line-height: 28px;
                    }

                    .mail_footer {
                        font-size: 12px;
                        line-height: 17px;
                        color: #bebebe;
                        margin-top: 60px;
                        letter-spacing: 1px;
                    }

                    .mail_logo {
                        /*这里修改LOGO*/
                        background-image: url("https://exmail.qq.com/zh_CN/htmledition/images/wwbiz_independent/notify_push/logo_2x.png");
                        background-size: 34px 24px;
                        width: 34px;
                        height: 24px;
                        background-repeat: no-repeat;
                        display: inline-block;
                        margin: 27px 0 20px 0;
                        clear: left;
                    }

                    .img_position {
                        max-width: 100%;
                    }

                    .normalTxt {
                        font-size: 14px;
                        line-height: 24px;
                        margin-top: 10px;
                    }

                    @media (max-width: 768px) {
                        .top_line {
                            display: none;
                        }

                        .mail_bg {
                            background: #fff;
                        }

                        .mail_cnt {
                            padding-bottom: 0;
                            padding-top: 0;
                        }

                        .eml_content {
                            padding: 0 12px 50px;
                        }

                        .phoneFontSizeTitle {
                            font-size: 18px !important;
                        }

                        .phoneFontSizeContent {
                            font-size: 16px !important;
                            line-height: 28px !important;
                        }

                        .phoneFontSizeTitleLarge {
                            font-size: 20px !important;
                        }

                        .phoneFontSizeTips {
                            font-size: 14px !important;
                        }
                    }
                </style>

                <div class="qmbox">
                    <div class="mail_bg">
                        <div class="mail_cnt">
                            <div class="mail_container">
                                <div class="top_line">
                                    <div class="top_line_left"></div>
                                    <div class="top_line_right"></div>
                                </div>
                                <div class="eml_content">
                                    <div class="mail_header">
                                        <div class="mail_logo"></div>
                                    </div>
                                    <div class="">
                                        <p style="font-size: 16px;margin-top:20px;" class="phoneFontSizeTitle">
                                            主任，您好！
                                        </p>
                                        <p style="font-size: 16px;margin-top:10px;padding-bottom: 20px"
                                            class="title_bold phoneFontSizeTitle">
                                            教务处通知已更新，更新内容如下：
                                        </p>
                                        <div style="margin-bottom: 40px;margin-top: 30px;overflow: hidden;">
                                            <div style="font-size: 16px;line-height: 28px;margin-bottom: 10px;"
                                                class="phoneFontSizeTitle">''' + send_msg + '''</div>
                                            <div style="display: inline-block;margin-top: 20px;margin-bottom: 20px;">
                                                <img class="img_position"
                                                    src="https://s1.ax1x.com/2022/10/16/xBUrHf.png"
                                                    onerror="">
                                            </div>
                                        </div>

                                    </div>
                                    <div class="mail_footer">
                                        Copyright &copy; 2022 Colyn, All Rights Reserved.
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!--<![endif]-->
    </includetail>
    </div>
    '''

    msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))
    # # 添加附件
    # att1 = MIMEText(open('D:\\weread_spider.txt', 'rb').read(), 'base64', 'utf-8')
    # att1["Content-Type"] = 'application/octet-stream'
    # att1["Content-Disposition"] = 'attachment;filename="test.pdf"'
    # msg.attach(att1)

    # 配置调用邮件信息
    msg['Subject'] = config["theme"]
    msg['From'] = config["admin"]

    # 执行命令
    s = smtplib.SMTP_SSL('smtp.qq.com', 465)
    s.login(config["admin"], config["key"])

    for recv in receiver:
        msg['To'] = recv
        s.send_message(msg)

    s.quit()
    print('邮件发送成功!')


class mySQL(object):
    def __init__(self, field: str):
        self.field = field
        self.db = m.connect(host="localhost", user="root", password="xxx", database="xxx")
        self.cur = self.db.cursor()
        self.dict = []

    def closeDB(self):
        self.cur.close()
        self.db.close()

    def getData(self, get_date):
        self.cur.execute(f"select cid from {self.field} where cdate='{get_date}'")
        for _ in self.cur.fetchall():
            self.dict.append(_[0])

        return self.dict

    def setData(self, set_data):

        try:
            # 执行SQL语句 插入多条数据
            self.cur.executemany(f"insert into {self.field}(cid,content,cdate,url) values(%s,%s,%s,%s);", set_data)
            # 提交数据
            self.db.commit()
            print("success")
            return 0

        except Exception as e:
            # 发生错误回滚
            self.db.rollback()
            print("error")
            logger.error(e)
            return 1


class Date(object):
    """
    日期处理对象
    """

    def __init__(self):
        self.date = datetime.date.today()

    def getToday(self):
        return self.date

    def str2Date(self, str_date):
        return datetime.date(*map(int, str_date.split('-')))

    def todayCmpDate(self, str_date):
        return str(self.date) == str_date


#
# date_str = '2022-10-14'
#
# d = Date()
# print("Today: " + str(d.getToday()))
# print(type(d.str2Date(date_str)))
# print(d.todayCmpDate(date_str))
# sql = mySQL("jwc")
# print(sql.getData(d.getToday()))


# data = [("1", "张三", "2022-10-14", "25",),
#         ("2", "李四", "2022-10-14", "20"),
#         ("3", "王五", "2022-10-14", "23")
#         ]

# sql.setData(data)
# msg = ["你好呀", "你好呀", "你好呀"]
# senMail(["xxx@foxmail.com"], msg)
# print("你好\n呀你好\n呀")
# print(f"你好\n呀你好\n呀")

