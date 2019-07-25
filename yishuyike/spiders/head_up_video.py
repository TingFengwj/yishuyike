import os
import shutil
import json
import requests
import time
import hashlib


def listdir(path, out_path_final):
    """
    :param path: 文件download路径
    :return: None
    """
    for file in os.listdir(path):
        file_name = file
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            target_content = []
            for video in os.listdir(file_path):
                target_content.append(video)
            out_path = u"%s\%s.mp4" % (out_path_final, file_name)  # 输出文件夹目录
            f = open(out_path, 'wb+')
            try:
                for i in range(len(target_content)):
                    new_path = r'C:\Users\EDZ\Desktop\video\%s\%s%d.mp4' % (file_name, file_name, i)
                    print(new_path)
                    for line in open(new_path, 'rb'):
                        f.write(line)
                    f.flush()
                return True
            except Exception as e:
                print(e)
                return False


def del_file(path):
    for i in os.listdir(file_dir):
        path_file = os.path.join(file_dir, i)
        if os.path.isdir(path_file):
            shutil.rmtree(path_file)
        else:
            os.remove(path_file)


def send_verifycode(tel_number):
    hl = hashlib.md5()
    hl.update(str(tel_number).encode(encoding='utf-8'))
    cykey = hl.hexdigest()
    uuid = "ffffffff-a13e-0106-ffff-ffffeb2eca03"
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 6  Build/NMF26X) AppleWebKit/534.30 (KHTML, "
                      "like Gecko) Version/4.0 Mobile Safari/534.30",
        "Connection": "close",
        "uuid": "ffffffff-a13e-0106-ffff-ffffeb2eca03",
        "deviceResolution": "1280*720",
        "ipAddress": "172.17.100.15",
        "phoneName": "shamu",
        "operateVersion": "5.1.1",
        "localPhoneModel": "Android",
        "deviceModel": "MI 6",
        "registrationId": "1a0018970afb2bb2aa4",
        "appVersion": "2.5.1",
        "operateSystem": "Android",
        "phoneType": "WIFI",
        "token": "",
        "cykey": cykey,
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "325",
        "Host": "api.chiyue365.com",
        "Accept-Encoding": "gzip",
    }
    verifycode_url = 'https://api.chiyue365.com/v5/verifycode'
    data = {
        "customerMobile": str(tel_number),
        "traceId": cykey,
        "userInfoVersion": "0",
        "cysecret": int(time.time() * 1000),
    }
    resp = requests.post(url=verifycode_url, headers=headers, data=data, timeout=5)
    if resp.status_code == 200:
        return tel_number, uuid, cykey
    else:
        print('验证码发送出现问题，请重新启动程序')
        return False


def login(verify_code, tel_number, uuid, cykey):
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 6  Build/NMF26X) AppleWebKit/534.30 (KHTML, "
                      "like Gecko) Version/4.0 Mobile Safari/534.30",
        "Connection": "close",
        "uuid": uuid,
        "deviceResolution": "1280*720",
        "ipAddress": "172.17.100.15",
        "phoneName": "shamu",
        "operateVersion": "5.1.1",
        "localPhoneModel": "Android",
        "deviceModel": "MI 6",
        "registrationId": "1a0018970afb2bb2aa4",
        "appVersion": "2.5.1",
        "operateSystem": "Android",
        "phoneType": "WIFI",
        "token": "",
        "cykey": cykey,
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "325",
        "Host": "api.chiyue365.com",
        "Accept-Encoding": "gzip",
    }
    data_login = {
        "customerMobile": str(tel_number),
        "verifyCode": str(verify_code),
        "uuid": uuid,
        "registrationId": "",
        "operateSystem": "android",
        "operateVersion": "5.1.1",
        "appVersion": "2.5.1",
        "deviceModel": "MI 6 ",
        "deviceResolution": "1280*720",
        "phoneType": "WIFI网络",
        "traceId": "03c08535eeb36a25ac1186cfbed1b0d3",
        "userInfoVersion": "0",
        "cysecret": int(time.time() * 1000),
    }
    login_url = 'https://api.chiyue365.com/v5/login'
    resp = requests.post(url=login_url, headers=headers, data=data_login, timeout=5)
    token = json.loads(resp.text)['data']['token']
    return token, cykey


file_dir = r"C:\Users\EDZ\Desktop\video"  # ts文件的保存路径  video文件夹需要新建,注意配置23行new_path
out_path_final = r'C:\Users\EDZ\Desktop\final'  # 最终文件输出路径：final文件夹需要新建
listdir(file_dir, out_path_final)
