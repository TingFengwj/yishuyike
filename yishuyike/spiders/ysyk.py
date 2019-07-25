# -*- coding: utf-8 -*-
from os import path
import scrapy
import re
from run import *

header_365 = {"Accept-Language": "zh-CN,zh;q=0.8",
              "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; MI 6  Build/ID) AppleWebKit/534.30 ("
                            "KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
              "Connection": "close",
              "token": TOKEN,
              "cykey": CYKEY,
              "Host": "api.chiyue365.com",
              "Accept-Encoding": "gzip", }

header_pptv = {"Accept-Language": "zh-CN,zh;q=0.8",
               "User-Agent": "ExoSourceManager/2.3.8 (Linux;Android 4.4.2) ExoPlayerLib/2.8.0",
               "Connection": "Keep-Alive",
               "Host": "player.pptvyun.com",
               "Accept-Encoding": "gzip", }

download_path = r'C:\Users\EDZ\Desktop\video'


class YsykSpider(scrapy.Spider):
    name = 'ysyk'

    def start_requests(self):
        yield scrapy.FormRequest(
            url='https://api.chiyue365.com/v4/contents/tag/0/client?traceId=36d335127e3c9e59cddfd5dca15eed31'
                '&userInfoVersion=1551927507281&cysecret=%d' % int(time.time() * 1000),
            headers=header_365,
            callback=self.parse
        )

    def parse(self, response):
        resp = json.loads(response.body.decode())
        print(resp)
        for i in resp['data']['contents']:
            if i['videoDurationLabel'] != "0'0''":
                if i['contentTitle'] == "行动教练":  # 书的名字
                    yield scrapy.FormRequest(
                        url='https://api.chiyue365.com/v4/contents/%d?traceId=36d335127e3c9e59cddfd5dca15eed31'
                            '&userInfoVersion=%d&cysecret=%d' % (i['contentId'], resp['extra']['userInfoVersion'],
                                                                 int(time.time() * 1000)),
                        headers=header_365,
                        callback=self.parse_info,
                        meta={'contentTitle': i['contentTitle']}
                    )

    def parse_info(self, response):
        resp = json.loads(response.body.decode())
        contentTitle = response.meta['contentTitle']
        # print(resp)
        resp = requests.get(
            url='http://player.pptvyun.com/svc/m3u8player/pl/%s.m3u8' % (resp['data']['content']['videoUrl']),
            headers=header_pptv,
        )
        resp = resp.text
        url = re.findall('http.*\n.*?', resp)[-1]
        url = re.sub('[\r\n]', '', url)
        resp_new = requests.get(url=url,
                                headers=header_pptv
                                )
        content = resp_new.text
        video_url = re.findall('/.*', content)
        for url in video_url:
            num = re.findall('ts_name=\d+', url)[0][8::]
            yield scrapy.Request(url="http://123.149.169.34" + url, callback=self.parse_video,
                                 meta={'contentTitle': contentTitle, "num": num})

    def parse_video(self, response):  # 存储单个视频
        contentTitle = response.meta['contentTitle']
        num = response.meta['num']
        file_name = contentTitle + num + '.mp4'
        base_dir = download_path
        video_base_dir = path.join(base_dir, contentTitle)
        video_local_path = path.join(video_base_dir, file_name)
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        if not os.path.exists(video_base_dir):
            os.mkdir(video_base_dir)

        with open(video_local_path, "wb") as f:
            f.write(response.body)
        pass
