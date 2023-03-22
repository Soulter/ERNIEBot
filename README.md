
# ERNIEBot

[![PyPi](https://img.shields.io/pypi/v/wenxin.svg)](https://pypi.python.org/pypi/wenxin)
[![Support_Platform](https://img.shields.io/pypi/pyversions/wenxin)](https://pypi.python.org/pypi/wenxin)


在Python上使用文心一言。可拓展为各种聊天机器人。

【已发现的问题】使用时，需要在你的项目根目录上加上/wenxin文件夹，然后将本项目src/wenxin/browsermob-proxy-2.1.4文件夹和chromedriver.exe复制到/wenxin中

【已发现的问题】请使用pypi wenxin库的1.1.4版本。

> 欢迎提交Pull Request或者Issues来改进此项目
> Make a pull request to improve this project

## 功能 / Fetures
- [ ] 基于ACS-Token逆向（暂时未解决）
- [x] 使用Selenium和Browsermob-Proxy来与文心一言模拟交互

# 使用 / Get Start

1. 执行`pip install wenxin -i https://pypi.org/simple/`
1. 【已发现的问题】需要在你的项目根目录上加上/wenxin文件夹，然后将本项目src/wenxin/browsermob-proxy-2.1.4文件夹和chromedriver.exe复制到/wenxin中
2. 使用以下代码：

```python
from wenxin.wenxin import WenXinBot
from wenxin.wenxin import WenxinRevError

# wenxin_cookies_dict_list 的内容详见下文
wx = WenXinBot(wenxin_cookies_dict_list)
# 初始化selenium，debug=True时，会输出调试信息，方便调试。headless=False时，会打开浏览器。
wx.initSelenium(debug=False, headless=True)
# 超时设置，单位秒，防止长时间等待，当超时后，会将已经生成的文本返回
res = wx.chatViaSelenium('hello', timeout=20)
print(res)

```

wx = WenXinBot()需要传入一个cookie参数，获取方法如下：

1. 使用一个获得资格的账号登录https://yiyan.baidu.com/ ，然后打开F12，找到如图所示的请求，右键另存为HAR

![image](https://user-images.githubusercontent.com/37870767/226515651-e7712406-a764-4c73-87b9-6b2b71bb9504.png)

2. 找到cookies，如下图所示，然后复制**整个**列表放到代码上。然后使用文本替换工具将`true`替换为`True`，`false`替换为False

![image](https://user-images.githubusercontent.com/37870767/226515947-53523ea2-ede4-4d42-9e87-7227a3446a52.png)

3. 替换文本完成后，得到的列表就是wx = WenXinBot()要传入的参数了。


