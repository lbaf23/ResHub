import datetime

#根据时间生成id
def tid_maker():
    return 'create' + '{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now())