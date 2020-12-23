import json
#from ResHub.controller.Search import translate_by_api


class Body:
    def __init__(self):
        self.must_list = []
        self.should_list = []
        self.not_list = []

    def add_must(self, key, value):
        self.must_list.append({
            "match": {
                key: value
            }
        })

    def add_should(self, key, value):
        self.should_list.append({
            "match": {
                key: value
            }
        })

    def add_not(self, key, value):
        self.not_list.append({
            "match": {
                key: value
            }
        })

    def get_body(self):
        if self.should_list:
            self.must_list.append({
                "bool": self.should_list
            })
        return {
            "query": {
                "bool": {
                    "must": self.must_list,
                    "must_not": self.not_list
                }
            }
        }


a = Body()
a.add_must( "text", "计算机")
a.add_must("text", "软件")
a.add_should("title", '人')

print((a.get_body()))
