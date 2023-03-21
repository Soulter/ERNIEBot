from wenxin.wenxin import WenXinBot
from wenxin.wenxin import WenxinRevError

# wenxin_cookies_dict_list 详见下文
wx = WenXinBot(wenxin_cookies_dict_list)
# 初始化selenium，debug=True时，会输出调试信息，方便调试。headless=False时，会打开浏览器。
wx.initSelenium(debug=True, headless=False)
# 超时设置，单位秒，防止长时间等待，当超时后，会将已经生成的文本返回
res = wx.chatViaSelenium('hello', timeout=20)
print(res)
