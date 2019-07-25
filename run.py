from scrapy import cmdline
from yishuyike.spiders.head_up_video import *

listen_class_cmd = ["scrapy", "crawl", "ysyk"]
read_book_cmd = ["scrapy", "crawl", "lis_cla"]

TOKEN = "674dfe79ddcc4c9e830ff31839b1e5cf",
CYKEY = "e40425e5eac569940c0f9ecaeb6dbd93",

if __name__ == '__main__':
    number = input('请输入手机号：')
    tel_number, uuid, cykey = send_verifycode(number)
    verify_code = input('请输入验证码：')
    TOKEN, CYKEY = login(verify_code, tel_number, uuid, cykey)
    print(TOKEN, CYKEY)
    video_type = input('请问下载什么部分视频课程?\n    1:读书部分视频\n    2:必修课部分视频')
    if video_type == "1":
        cmdline.execute(listen_class_cmd)
    else:
        cmdline.execute(read_book_cmd)