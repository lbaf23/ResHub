import json
#from ResHub.controller.Search import translate_by_api
import requests

def translate_by_api(str):
    """
   input : str 需要翻译的字符串
   output：translation 翻译后的字符串
   有每小时1000次访问的限制
   """
    # API
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数， i为要翻译的内容
    key = {
        'type': "AUTO",
        'i': str,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 通过 json.loads 把返回的结果加载成 json 格式
        result = json.loads(response.text)
        #         print ("输入的词为：%s" % result['translateResult'][0][0]['src'])
        #         print ("翻译结果为：%s" % result['translateResult'][0][0]['tgt'])
        translation = result['translateResult'][0][0]['tgt']
        return translation
    else:
        # 相应失败就返回空
        return ''


class Body:
    def __init__(self):
        self.must_list = []
        self.should_list = []
        self.not_list = []

    def add_must(self, key, value, expand=False):
        self.must_list.append({
            "match": {
                key: value
            }
        })
        if expand:
            ex = translate_by_api(value)
            if ex != '':
                self.should_list.append({
                    "match": {
                        key: ex
                    }
                })

    def add_should(self, key, value, expand=False):
        self.should_list.append({
            "match": {
                key: value
            }
        })
        if expand:
            ex = translate_by_api(value)
            if ex != '':
                self.should_list.append({
                    "match": {
                        key: ex
                    }
                })

    def add_not(self, key, value, expand=False):
        self.not_list.append({
            "match": {
                key: value
            }
        })
        if expand:
            ex = translate_by_api(value)
            if ex != '':
                self.not_list.append({
                    "match": {
                        key: ex
                    }
                })

    def get_body(self):
        if self.should_list:
            self.must_list.append({
                "bool": {
                    "should": self.should_list
                }
            })
        return {
            "query": {
                "bool": {
                    "must": self.must_list,
                    "must_not": self.not_list
                }
            }
        }
