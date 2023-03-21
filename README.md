# ERNIEBot


在Python上使用文心一言。可拓展为各种聊天机器人。

> 欢迎提交Pull Request来改进此项目
> Make a pull request to improve this project

## 功能 / Fetures
- [ ] 基于ACS-Token逆向（暂时未解决）
- [x] 使用Selenium和Browsermob-Proxy来与文心一言模拟交互

# 使用 / Get Start

1. 克隆此仓库（未来将会上传到pypi）
2. 执行`pip install -r requirements.txt`
3. 执行`python src/wenxin/wenxin.py`

如果要在你的项目上使用：

1. 克隆此仓库（未来将会上传到pypi），将src/wenxin文件夹复制至你的项目上
2. 执行`pip install -r requirements.txt`
3. 使用以下代码：
```
from wenxin.wenxin import WenXinBot
from wenxin.wenxin import WenxinRevError

# wenxin_cookies_dict_list 内容详见下文
wx = WenXinBot(wenxin_cookies_dict_list)
# 初始化selenium，debug=True时，会输出调试信息，方便调试。headless=False时，会打开浏览器。
wx.initSelenium(debug=False, headless=True)
# 超时设置，单位秒，防止长时间等待，当超时后，会将已经生成的文本返回
res = wx.chatViaSelenium('hello', timeout=20)
print(res)

```

wx = WenXinBot()需要传入一个cookie参数，获取方法如下：

