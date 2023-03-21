import requests
import time
import json
from selenium import webdriver
import time
from browsermobproxy import Server
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os, sys
url = 'https://yiyan.baidu.com/'
url_check = "https://yiyan.baidu.com/eb/chat/check"
url_new = "https://yiyan.baidu.com/eb/session/new"
url_new_text = "https://yiyan.baidu.com/eb/chat/new"
url_check = "https://yiyan.baidu.com/eb/chat/check"


abs_path = os.path.dirname(os.path.realpath(sys.argv[0])) + '/'

"""
    错误类
    code:
    0: 其他错误
    1: 未传入cookies
    2: 初始化selenium失败
    3: chat空消息
"""
class WenxinRevError(Exception):
        def __init__(self, value, code=0):
            self.value = value
            self.code = code

        def __str__(self):
            return repr(self.value)


class WenXinBot:
    def __init__(self, wenxin_cookies_dict_list) -> None:
        # self.cookies = cookies
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        #     'Cookie': wenxin_cookies,
        #     'Content-Type': 'application/json;charset=UTF-8',
        #     'Acs-Token': acs_token,
        # }
        # self.acs_token = acs_token
        if not wenxin_cookies_dict_list:
            raise WenxinRevError("必须传入cookies列表", 1)
        self.wenxin_cookies_dict_list = wenxin_cookies_dict_list

    def new_session(self, name):
        # 已实现
        ts = int(time.time() * 1000)
        data = {
            'deviceType': "pc",
            'sessionName': name,
            'timestamp': ts,
        }
        res = requests.post(url_new, headers=self.headers, json=data)
        session_id = res.json()['data']['sessionId']
        print(res.text)
        self.session_id = session_id
        return session_id
    
    def chat(self, text, sessionid):
        # 未实现，请不要调用此方法
        ts = int(time.time() * 1000)
        data = {
            'deviceType': "pc",
            'code': 0,
            'sessionId': str(sessionid),
            'timestamp': ts,
            'msg': "",
            'parentChatId': 0,
            "text": text,
            "type": 10,
            "sign": "",
            "jt": ""
        }
        res = requests.post(url_new_text, headers=self.headers, json=data)
        print(res.text)

    """
      初始化selenium
    """
    def initSelenium(self, headless=True, debug = False) -> bool:
        # 启动代理
        server_proxy = Server(abs_path+'wenxin/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat')
        server_proxy.start()
        self.seleniumDebug = debug
        print("[Wenxin] 开始模拟登录\n")
        try:
            self.proxy = server_proxy.create_proxy()
            options = webdriver.ChromeOptions()
            options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))
            options.add_argument('--incognito')
            options.add_argument('--ignore-certificate-errors')
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
            options.add_argument('window-size=1920x1080')
            options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
            options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片,提升速度
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('log-level=3')
            # options.binary_location = '98.0.4758.102_chrome_installer.exe'
            self.driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
            self.driver.get(url)
            time.sleep(5)
            self.driver.delete_all_cookies()

            # init_cookies_str = "HOSUPPORT=1; HOSUPPORT_BFESS=1; HISTORY=6bbc5533faa802df41ed93dc43a87ffcbc1b4e; HISTORY_BFESS=6bbc5533faa802df41ed93dc43a87ffcbc1b4e; __yjs_duid=1_2c2b4ddc6ecdf6dd3c027cc3b56af3101645928767022; BIDUPSID=6425B660DB32652C46F4C3DA34B8E3DE; PSTM=1645956349; Hm_lvt_90056b3f84f90da57dc0f40150f005d5=1654607966; USERNAMETYPE=3; SAVEUSERID=c21de9f0ea33bf2c8d3d0e5195da45; USERNAMETYPE_BFESS=3; SAVEUSERID_BFESS=c21de9f0ea33bf2c8d3d0e5195da45; BAIDUID=355F2EE1C5F9C3730C18C719B39A026A:SL=0:NR=10:FG=1; MCITY=-:; UBI=fi_PncwhpxZ~TaBBBVwL3UZ-GNQ8tBPA0fGAAIepfm8Jg24hOxJFP3onq4dHzN6ygZDaFoEfyDMCNMTRP08ATv5UfRSuJysfoHr~Yp8EKY0yQoBXgfBA3lO2td9Isuiw1VjapwwXsrPHBC72PGDxyMcp6i~Ocv8YeAvpd5EyZE2p3dtmkk8cMrmk4HgvIQtQ7Imh9saajjSn6J6OfopJAuPQkfzGTmvFM5bG60~; UBI_BFESS=fi_PncwhpxZ~TaBBBVwL3UZ-GNQ8tBPA0fGAAIepfm8Jg24hOxJFP3onq4dHzN6ygZDaFoEfyDMCNMTRP08ATv5UfRSuJysfoHr~Yp8EKY0yQoBXgfBA3lO2td9Isuiw1VjapwwXsrPHBC72PGDxyMcp6i~Ocv8YeAvpd5EyZE2p3dtmkk8cMrmk4HgvIQtQ7Imh9saajjSn6J6OfopJAuPQkfzGTmvFM5bG60~; STOKEN=37ef82cf09bda3ac186cbaed4e5dfe9ea3254d2e56be3c7403b4025a385b5551; BDUSS=lidzNnM3pDflY5Z0xUSFB1QmgxRUg4LVJxMkhIalFJaUVVNXpVc35udVdaelprRVFBQUFBJCQAAAAAAAAAAAEAAAC2j4BOysm76nNoaV9odW4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJbaDmSW2g5kUl; PTOKEN=ac920fa042c08036faaf20b5465a10cb; BDUSS_BFESS=lidzNnM3pDflY5Z0xUSFB1QmgxRUg4LVJxMkhIalFJaUVVNXpVc35udVdaelprRVFBQUFBJCQAAAAAAAAAAAEAAAC2j4BOysm76nNoaV9odW4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJbaDmSW2g5kUl; STOKEN_BFESS=37ef82cf09bda3ac186cbaed4e5dfe9ea3254d2e56be3c7403b4025a385b5551; PTOKEN_BFESS=ac920fa042c08036faaf20b5465a10cb; BAIDUID_BFESS=355F2EE1C5F9C3730C18C719B39A026A:SL=0:NR=10:FG=1; ZFY=yIJ3f0WDMslYdGakVbWOsVt8ykZe:A0wWGNbfpsLoWRI:C; __bid_n=18607531e6414876564207; MBD_AT=0; FPTOKEN=LwdBc0OpOjU4Ryk0cMs2t0P9dw7ke3aJSSmmy5Rmv0DL6SyGeVcMKLPJttn/hhZo7jEipQorYKRsDT0Scl1r4uQEEDNdIceulbjKQEFh5zbTi93Egf6Y74fyAb1phB4L/ySm/QO4F2gZMbL5zURMBSg1/oxJZT1lW3RC3PAs2r+M63lOj7gesHYmj1y5vkUaMImeaFdrHLpT1Fqn7zMrV6RImn/GfNLo5wz1DxZCRgu7ItmBMg+y1UF6nSXNQThVGvgyFbLa5lPbsDScgbk6UkXgvh2zYIezCtLwhZ+MXXkE4W3HRoTAQ3aGJ7Ua/1LuW/BU7P+eR5E3q34PfGmwnznP1+0ntmm/zUuHP/ILEDtRt8Bm0oUMI0TqrOnj+OY2c/rmGP118soQnfTrUYwutA==|pgfxTRqmBgcSFGW71fi0UtRH0y15D7UzRhZOpkPxp1I=|10|b01f78911dd7ed8c636e5dcec4daca6c; RT=\"sl=1&ss=lff1sknc&tt=dp&bcn=https://fclog.baidu.com/log/weirwood?type=perf&z=1&dm=baidu.com&si=97wfrppdd4s&ld=15p&ul=57y&hd=5bj\"; BA_HECTOR=a50l0g05048l01ag2l012gaa1i1g24m1m; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ab_sr=1.0.1_MGZiOTA2YzU0MjVhY2U4ZTM0MjdhODBmYmJjYjVkMTIyN2FlYTM5MDFmNDViZjA4ODIzNjA5NjE5YThmMzU0NmVlNDM2MzZlYjE3ODM1YTJhMTNlNjQ0MTMyNWFkMWI2NzJjNzFjYzY3YjA0YjA4N2M4ZjFkNjA2MWViNzA3ZWI2NWZhYmIzYzMxNTY1ODhiMDk3MjRkNzc1MTU4Y2UwMjc1NzgxNmVjZGVkNmZmZGNhYWYwOTAzOTMxZjA3ZGVh"
            # for tcookie in init_cookies_str.split(";"):
            #     t = {
            #         "name": tcookie.split("=")[0].strip(),
            #         "value": tcookie.split("=")[1].strip(),
            #     }
            #     wenxin_cookies_dict_list.append(t)
            # print(wenxin_cookies_dict_list)
            for t in self.wenxin_cookies_dict_list:
                self.driver.add_cookie(t)
            self.driver.get(url)
            time.sleep(3)
            print("[Wenxin] 加载完成")
        except Exception as e:
            print("[Wenxin] 在初始化Selenium时加载失败")
            raise WenxinRevError("在初始化Selenium时加载失败: "+str(e), 2)
        return True
        
        
    """
      通过Selenium来进行交互
    """
    def chatViaSelenium(self, text, timeout=20) -> str:
        if text == "":
            raise WenxinRevError("Chat输入为空", 3)
        ts = str(time.time())
        self.proxy.new_har(ts, options={'captureContent': True})
        # type = int(input("类型"))
        # val = input("值")
        # if type == 1:
        #     driver.find_element(By.XPATH, val).send_keys(text)
        # elif type == 2:
        input_area = self.driver.find_element(By.CLASS_NAME, 'wBs12eIN')
        input_area.send_keys(text)
        input_area.send_keys(Keys.ENTER)
        print("[Wenxin] 发送成功，正在收集信息..")
        capture_count = 0

        while True:
            time.sleep(2)
            result = self.proxy.har
            res_text = ''
            is_end = False
            for entry in result['log']['entries']:
                if('request' in entry and 'url' in entry['request'] and entry['request']['url'] == 'https://yiyan.baidu.com/eb/chat/query'):
                    if self.seleniumDebug: print("[Wenxin] [SUCCESS] Get query.")
                    if self.seleniumDebug: print(entry)
                    if ('response' in entry and 'content' in entry['response'] and 'text' in entry['response']['content']):
                        reply_data = json.loads(entry['response']['content']['text'])
                        if self.seleniumDebug: print("[Wenxin] [SUCCESS] Get Reply Data.")
                        if(reply_data['data']['content'] != ""):
                            res_text += reply_data['data']['content']
                            if self.seleniumDebug: print("isend:" + str(reply_data['data']['is_end']))
                            if(reply_data['data']['is_end'] == 1 or reply_data['data']['is_end'] == "1"):
                                is_end = True
                                if self.seleniumDebug: print("[Wenxin] [SUCCESS] Get is_end == 1.")
                                break
            
            if(is_end):
                if self.seleniumDebug: print("[Wenxin] [Reply] "+ res_text)
                return res_text
            else:
                capture_count += 1
                if self.seleniumDebug: print("[Wenxin] [Replying] "+ res_text)
            
            if(capture_count*2 > timeout):
                if self.seleniumDebug: print("[Wenxin] Timeout.")
                return res_text
            # driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[2]/textarea").send_keys(text)
            # driver.find_element(By.XPATH, "//*[@id=\"root\"]/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[3]/span[1]/svg/g/g[1]/g/path[2]").click()
    

    def check(self, text):
        ts = int(time.time() * 1000)
        data = {
            'deviceType': "pc",
            'timestamp': ts,
            'text': text,
        }
        res = requests.post(url_check, headers=self.headers, json=data)
        print(res.text)