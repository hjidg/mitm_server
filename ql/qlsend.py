


from .ql_sample import get_conf
from .util_ql import *

def qlsend(all_data_path,qlurl,qlid,qlsecret):
    conf = get_conf(all_data_path)
    token = ql_ini(qlurl,qlid,qlsecret)
    envs = ql_envs(qlurl,token)
    msg = []
    for name,value,app in conf:
        msg.append(send2ql(qlurl,token,envs,name,value,app))
    return msg

def send2ql(qlurl,token,envs,name,value,app):
    if value:
        if env_app:=[item for item in envs if item.get('name')==name]:
            _id = env_app[0].get('_id')
            ql_update(qlurl,token,name,value,app,_id)
            return app+' updated'
        else:
            r = ql_add(qlurl,token,name,value,app)
            return app+' added'
    else:
        if env_app:=[item for item in envs if item.get('name')==name]:
            _id = env_app[0].get('_id')
            ql_delete(qlurl,token,_id)
            return app+' deleted'
