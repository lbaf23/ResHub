import json
# from ResHub.controller.Search import translate_by_api
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
        self.sort_list = []
        self.range_list = []
        self.from_page = 0
        self.page_size = 10

    def set_from_page(self, from_page):
        self.from_page = from_page

    def set_page_size(self, page_size):
        self.page_size = page_size

    def add_must(self, key, value, expand=False):
        if value != '':
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
        if value != '':
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
        if value != '':
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

    def add_range(self, key, value_from, value_to, from_eq=False, to_eq=False):
        l = "gt"
        h = "lt"
        if from_eq:
            l = "gte"
        if to_eq:
            h = "lte"
        self.range_list = ({
            key: {
                l: value_from,
                h: value_to
            }
        })

    def add_sort(self, key, sort_type_desc=True):
        o = "desc"
        if not sort_type_desc:
            o = "asc"
        self.sort_list.append({
            key: {
                "order": o
            }
        })

    def get_body(self):
        if self.must_list:
            self.should_list.append({
                "bool": {
                    "must": self.must_list
                }
            })
        global_list = [{
            "bool": {
                "should": self.should_list
            }
        }]
        if self.range_list:
            global_list.append({
                "range": self.range_list
            })
        return {
            "query": {
                "bool": {
                    "must": global_list,
                    "must_not": self.not_list
                }
            },
            "sort": self.sort_list,
            "size": self.page_size,
            "from": self.from_page
        }
