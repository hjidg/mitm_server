
import mitmproxy.http
from mitmproxy import ctx
from .utils import *

class elm(object):
    def __init__(self,q_msg,temp_folder='temp'):
        self.q_msg = q_msg
        self.toml_path = f'{temp_folder}/elm.toml'
        self.table = {}
        # 饿了么美团滴滴
        self.elm = 0
        self.meituan = 0
        self.ddgy = 0
        self.txstock = [0,0,0]
        self.jrttjsb = 0
            
    def request(self,flow: mitmproxy.http.HTTPFlow):           
        # 饿了么 打开吃货豆任务栏
        if self.elm == 0:
            if flow.request.pretty_url.startswith('https://h5.ele.me/svip/task-list'):
                app = '饿了么'
                res = "{{'elmck':'{}'}}"
                ck_keys = ['_tb_token_','cookie2']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    self.elm = res.format(ck_dict_to_str(dict(flow.request.cookies)))
                    self.table[app] = [eval(self.elm)]
                    save_toml(self.table,self.toml_path)
                    self.q_msg.put('----------饿了么 Success----------')
                    self.q_msg.put(dict2conf(res))
        # 美团
        if self.meituan == 0:
            if 'meituan.com' in flow.request.pretty_url:
                app = '美团'
                res = "{{'mtTk':'{}','sjpz':'False'}}"
                cookies_dict = dict(flow.request.cookies)
                if 'mt_c_token' in cookies_dict.keys():
                    self.meituan = res.format(cookies_dict['mt_c_token'])
                    self.table[app] = [eval(self.meituan)]
                    self.save_table()
                    self.q_msg.put('----------美团 Success----------')
                    self.q_msg.put(dict2conf(res))
        # 滴滴果园
        if self.ddgy == 0:
            if flow.request.pretty_url.startswith('https://game.xiaojukeji.com/api/game/mission/get?'):
                app = '滴滴果园'
                res = "{{'ddgyurl':'{}'}}"
                if flow.request.method == 'GET':
                    self.ddgy = res.format(flow.request.pretty_url)
                    self.table[app] = [eval(self.ddgy)]
                    self.save_table()
                    self.q_msg.put('----------滴滴果园 Success----------')
                    self.q_msg.put(dict2conf(res))
        # 腾讯自选股 app打开金币商城 微信
        if not all(self.txstock):
            if flow.request.pretty_url.startswith('https://wzq.tenpay.com/cgi-bin/activity_task_daily.fcgi?'):
                app = '腾讯自选股'
                res = "{{'TxStockAppUrl':'{0}','TxStockAppHeader':'{1}','TxStockWxHeader':'{2}'}}"
                headers_dict = dict(flow.request.headers)
                cookies_dict = dict(flow.request.cookies)
                if 'qlappid' not in cookies_dict.keys():
                    self.txstock[0] = flow.request.pretty_url
                    self.q_msg.put('----------TxStockAppUrl----------')
                    self.txstock[1] = str(headers_dict)
                    self.q_msg.put('----------TxStockAppHeader----------')
                else:
                    self.txstock[2] = str(headers_dict)
                    self.q_msg.put('----------TxStockWxUrl----------')
                if all(self.txstock):
                    txstock_dict = res.format(*self.txstock)
                    self.table = [eval(txstock_dict)]
                    self.save_table()
                    self.q_msg.put('----------腾讯自选股 Success----------')
                    self.q_msg.put(dict2conf(res))
        # 今日头条极速版
        if self.jrttjsb == 0:
            if any([item in flow.request.pretty_host for item in ['toutiaoapi.com','snssdk.com']]):
                app = '今日头条极速版'
                res = "{{'jrttjsbUA':'{0}','jrttjsbHeader':'{1}','jrttjsbReadNum':'10','jrttjsbFarm':'0'}}"
                hd_key = 'user-agent'
                ck_keys = ['passport_csrf_token_default','odin_tt']
                cookies_dict = dict(flow.request.cookies)
                if set(ck_keys) < set(cookies_dict.keys()):
                    headers_dict = {k.lower():v for k,v in dict(flow.request.headers).items()}
                    self.jrttjsb = res.format(headers_dict[hd_key],ck_dict_to_str(dict(flow.request.cookies)))
                    self.table[app] = [eval(self.jrttjsb)]
                    self.save_table()
                    self.q_msg.put('----------今日头条极速版 Success----------')
                    self.q_msg.put(dict2conf(res))
