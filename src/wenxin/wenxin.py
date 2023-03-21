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