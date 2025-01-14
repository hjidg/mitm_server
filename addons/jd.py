
import mitmproxy.http
from .utils import *

class jd(object):
    def __init__(self,child_conn,temp_folder='temp'):
        # app
        self.app = '京东'
        # result of capture
        self.res = {
            'pin':'',
            'wskey':''
        }
        # ini
        self.count = 0
        self.table = {}
        self.toml_path = f'{temp_folder}/{self.app}.toml'
        self.child_conn = child_conn

    def request(self,flow: mitmproxy.http.HTTPFlow):
        # 
        if self.count == 0:
            if flow.request.pretty_url.startswith('https://perf.m.jd.com/') and flow.request.method=='POST':
                cookies = dict(flow.request.cookies)
                if 'pt_pin' in cookies.keys():
                    self.res['pin'] = cookies.get('pt_pin')
                    #
                    self.child_conn.put(self.app+'----------get pt_pin Success----------')
            if flow.request.pretty_url.startswith('https://api.m.jd.com/') and flow.request.method=='POST':
                cookies = dict(flow.request.cookies)
                if 'wskey' in cookies.keys():
                    self.res['wskey'] = cookies.get('wskey')
                    #
                    self.child_conn.put(self.app+'----------get wskey Success----------')
            # check res and save
            if all(self.res.values()):
                self.table[self.app] = [self.res]
                self.count = 1
                self.child_conn.put(dict2conf(self.res))
                save_toml(self.table,self.toml_path)
                   