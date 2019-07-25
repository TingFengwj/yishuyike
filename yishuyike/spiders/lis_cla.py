# -*- coding: utf-8 -*-
import json
import os
import re
import time
from os import path
import requests
import scrapy
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


class LisClaSpider(scrapy.Spider):
    name = 'lis_cla'

    def start_requests(self):
        yield scrapy.FormRequest(
            url='https://api.chiyue365.com/v4/packs?traceId=36d335127e3c9e59cddfd5dca15eed31&userInfoVersion'
                '=1551927507281&cysecret=%d' % int(time.time() * 1000),
            headers=header_365,
            callback=self.parse
        )

    def parse(self, response):
        resp = json.loads(response.body.decode())
        content = resp['data']['packs'][1::]
        for i in content:
            print(i['packId'])
            print(i['packTitle'])
            if i['packTitle'] == '创新设计思维':
                yield scrapy.FormRequest(
                    url='https://api.chiyue365.com/v4/playlist/pack/%d?pageSize=20&packId=%d&traceId'
                        '=36d335127e3c9e59cddfd5dca15eed31&userInfoVersion=%s&cysecret=%s ' % (i['packId'], i['packId'],
                                                                                               resp['extra'][
                                                                                                   'userInfoVersion'],
                                                                                               int(time.time() * 1000)),
                    headers=header_365,
                    meta={'packTitle': i['packTitle']},
                    callback=self.parse_test
                )

    def parse_test(self, response):
        resp = json.loads(response.body.decode())
        packTitle = response.meta['packTitle']
        for i in resp['data']['playListVOList']:
            # print(i['videoUrl'])
            resp = requests.get(
                url='http://player.pptvyun.com/svc/m3u8player/pl/%s.m3u8' % (i['videoUrl']),
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
                                     meta={'contentTitle': i['contentTitle'], "num": num, 'packtitle': packTitle}, )

    def parse_video(self, response):
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
