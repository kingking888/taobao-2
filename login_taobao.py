import json
import re
import requests


"""
输入用户名之后，浏览器会发送一个post请求，如果返回为True，则会出现滑块，如果返回为Fasle则不会出现滑块

思维逻辑：
1.输入用户名
2.判断是否显示验证码，传入参数用户名+ua参数
3.返回True或False
4.输入密码
5.请求登录，传入用户名+ua参数+加密后的密码等大量参数
6.验证用户名和密码，通过后生成token
7.返回申请st码地址+token
8.申请st码，传入生成的token
9.返回st码
10.访问st码
11.返回cookie
12.登录成功

程序流程：
1.输入用户名，浏览器会向淘宝发起一个post请求，判断是否出现滑块验证！
2.用户输入密码后，浏览器向淘宝又发起一个post请求，验证用户名密码是否正确，如果正确则返回一个token
3.浏览器拿着token去阿里巴巴交换st码
4.浏览器获取st码之后，拿着st码获取cookies，登录成功
"""
session = requests.session()

class UserNameLogin():
    def __init__(self, username, ua, TBL_password2):
        """
        账号登录对象
        :param username:用户名
        :param ua:淘宝的ua参数
        :param TBL_password2:加密后的密码
        """
        # 监测是否需要验证码的url
        self.nick_check_url = "https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8"
        # 验证淘宝用户名和密码的url
        self.login_url = "https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F"
        # 访问st的url
        self.vst_url = "https://login.taobao.com/member/vst.htm?st={}"
        # 用户名
        self.username = username
        # 淘宝用户名，包含浏览器的一些信息，很多地方会使用，从浏览器或者抓包工具中复制，可重复使用
        self.ua = ua
        # 加密后的密码，从浏览器或者抓包工具中复制，可重复使用
        self.TBL_password2 = TBL_password2
        self.timeout = 3

    def nick_check(self):
        """
        检测账号是否需要验证码
        :return:
        """
        data = {
            "username": self.username,
            "ua": self.ua
        }
        try:
            response = session.post(self.nick_check_url, data=data, timeout=self.timeout)
            needcode = json.loads(response.text)["needcode"]
            return needcode
        except Exception as e:
            print("_nick_check  检查是否需要验证码失败：{}".format(e))
            return True


    def verity_password(self):
        """
        验证用户名和密码，获取st码链接
        :return:st码链接
        """
        verity_password_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "cache-control": "max-age=0",
            "origin": "https://login.taobao.com",
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fi.taobao.com%2Fmy_taobao.htm%3Fnekot%3DdzcyNDU1OTg0OA%253D%253D1565940773254",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
        verity_password_data = {
            "TPL_username": self.username,
            "ncoToken": "9bd9245bac5a2878ea05b2bb7ef647bfa3efa207",
            "slideCodeShow": "false",
            "useMobile": "false",
            "lang": "zh_CN",
            "loginsite": "0",
            "newlogin": "0",
            "TPL_redirect_url": "https://i.taobao.com/my_taobao.htm?nekot=dzcyNDU1OTg0OA%3D%3D1565940773254",
            "from": "tb",
            "fc": "default",
            "style": "default",
            "keyLogin": "false",
            "qrLogin": "true",
            "newMini": "false",
            "newMini2": "false",
            "loginType": "3",
            "gvfdcname": "10",
            "gvfdcre": "68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61317A30322E312E3735343839343433372E372E33333132373832646E695A61585A26663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246692E74616F62616F2E636F6D2532466D795F74616F62616F2E68746D2533466E656B6F74253344647A63794E4455314F5467304F412532353344253235334431353635393430373733323534",
            "TPL_password_2": self.TBL_password2,
            "loginASR": "1",
            "loginASRSuc": "1",
            "oslanguage": "zh-CN",
            "sr": "1366*768",
            "naviVer": "chrome|70.0353877",
            "osACN": "Mozilla",
            "osAV": "5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "osPF": "Win32",
            "appkey": "00000000",
            "mobileLoginLink": "https://login.taobao.com/member/login.jhtml?redirectURL=https://i.taobao.com/my_taobao.htm?nekot=dzcyNDU1OTg0OA%3D%3D1565940773254&useMobile=true",
            "um_token": "T128D1848D68C0663A200E498723F2A6A2F4C469E934EB346A8B3FEDAEF",
            "ua": self.ua,
        }
        try:
            response = session.post(self.login_url, headers=verity_password_headers, data=verity_password_data, timeout=self.timeout)
            st_token_url = re.search(r'<script src="(.*?)"></script>', response.text).group(1)
            print(st_token_url)
        except Exception as e:
            print("verity_password 验证用户名和密码请求失败：{}".format(e))
            return None
        if st_token_url:
            print("验证用户名密码成功， st码申请地址：{}".format(st_token_url))
            return st_token_url
        else:
            print("用户名密码验证失败，请更换data")
            return None

    def apply_st(self):
        """
        申请st码
        :return: st码
        """
        apply_st_url = self.verity_password()
        print(apply_st_url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }
        if apply_st_url:
            try:
                st_resp = session.get(apply_st_url, headers=headers)
                st_match = re.search(r'"st":"(.*?)"}', st_resp.text)
                if st_match:
                    st = st_match.group(1)
                    print("获取st码成功， st码：%s"% st)
                    return st
                else:
                    raise RuntimeError("获取st码失败")
            except Exception as e:
                print("申请st码请求失败，原因：".format(e))

    def login(self):
        """
        通过st码获取登录cookie
        :return:
        """
        is_check = self.nick_check()
        if not is_check:
            st = self.apply_st()

            headers = {
                "host": "login.taobao.com",
                "Connection": "Keep-Value",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
            }
            try:
                url = self.vst_url.format(st)
                print("st 拼接的url为：{}".format(url))
                response = session.get(url, headers=headers)
                response.raise_for_status()
                print(response.text)
                my_taobao_search = re.search(r'top.location.href = "(.*?)"', response.text)
                if my_taobao_search:
                    print("登录淘宝成功，跳转连接：{}".format(my_taobao_search.group(1)))
                    return my_taobao_search.group(1)
                else:
                    raise RuntimeError("登录失败！response:{}".format(response.text))
            except Exception as e:
                raise e


if __name__ == '__main__':
    username = "18392141557"
    ua = "119#Ml7iMx1yMDlzcMMzZwbNfuNz/ufQycWxAlp2xQTXi+14vLprczjiYqmD2mSMTL++q72oV+rnPviWYCCELZ1ByHWrt8IwMV4X3wgF9U+S4lkGq0AGOcS+N62y9AiNYBIp3FA8bXDL4lU233H28lo6YOgtWZHmnBBe3FN8fUWS4Q9LdFCCR2VVNlsCPFHrIGPOQtKUfwZW4lgLfVMmy2gS5tFGXRMIsYSm3FN89UWE4Z4mlZAWP0BV5N9Ame3PZSSe3AA89dao4lyCO0FbRUKONNFL93WzRBqed3N89w6O4QuGdeA85JPBN88LzwIZz/q1OO+NuTvx+s1rSR7scrAi+nn06TN9ZnIifUIq+4ziIwZj2egJsp/zjdrfB+kysij0sUOFQ3ufJfGoeKz/CtbtJlUMG6GO0nzgT9SVWAJF8dKMsMviSCNV/KXWbvxU5WtLauDORJMzsbAXP1dnGKq2N4JWIsy27Btgyj5PVTXiP3M2E1x2OWYAb7Pc305iRwXtKdPizbR5tNhGNQcYZVfGwuof5HUefGGMSDg43a1sNiZYVvaRtzRYuXPFo5MbmT6yWa39MGAz75x0Unf3PERoAQNSBS10d+mCQYGReg5Not4D5jwDvZzJ9lap7sCaxhw/vMD+8XpsHajrAp2sz3duP2YOC2oWNUJy5d5CF4OBg8TBN0svUQGjA54Vla0mRA814CXXG5NWhaqgZ+szFmxeO5hNe1H7S1L+bBuyxxAMyIi4nWuBONb1XmkAcmGpSEJ8f/YiN8UPDAUJ9aHbh7vg8rzYEsP633jzJrHJaJpA2oh+C2k2f6KEjP46alPuRwLVTJ9B9J39Ypnba/eo6SVauDyY/bKyYTMbwXml+0Nap5xl12MNDeOInoHhSwQHaKZqpKyWIKrkK/aZ3LSZaA0Zr0mZ/+4USuQhkDPwUBc+uGwG9Ve+KRi0PLPEvbxBwym9MZh5/pTfJFSA9uRyUfASGgK1asKy/oLElpHKcNgpgMt5VVbCCBbBGSGPYgfF3/I+VjE69B216w6GGQ/W5ndm9YlWFzRULPZ1pRsL2WSwkK/cnVonj7aMlh6lwLLxjX2Q3Mx5C4xcIE94J5wvkILajCRm8abM5b/JIilX3xk1H7mMGTQZfCv66/NheevlxOA0RuGACq7IDi0TdXR+FO=="
    TPL_password2 = "2c5dd3057d41a82031dcd2d6661f3282c94f87eccb1beee2ff129f2151d828ba734e388b562fa2cc239e9ac021f2417edaea2b40b90b9f47db211d5439c2f9841cd09146bddb2ef2c70a7030fb9ed4b5be5fc898de4833bba680ec275bbc2555398f53916cb1d89b2a47fdda3ede5f03156e7aac72629b3abcd3d11c8ebd4b2a"
    unlogin = UserNameLogin(username, ua, TPL_password2)
    s = unlogin.login()
    response = session.get(s)
    print(response.text)