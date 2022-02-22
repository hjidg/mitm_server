
from .myfunc import get_toml

def get_conf(all_data_path):
    '''
        青龙环境变量格式，有的是以@分隔，有的是&，有新的环境变量格式就写到下面
    '''
    conf = []
    data = get_toml(all_data_path)

    app,name,lj = ['京东','JD_WSCK','&']
    value ='&'.join([f'pin={account.get("pin")};wskey={account.get("wskey")};' for account in data.get(app)])
    conf.append([name,value,app])

    app,name,lj = ['饿了么','elmck','@']
    value = lj.join([account.get(name) for account in data.get(app)])
    conf.append([name,value,app])

    app,name,lj = ['滴滴果园','ddgyurl','@']
    value = lj.join([account.get(name) for account in data.get(app)])
    conf.append([name,value,app])

    app,name,lj = ['美团','mtTk','@']
    value = lj.join([account.get(name) for account in data.get(app)])
    conf.append([name,value,app])

    app,name,lj = ['快手极速版','kshd','@']
    value = lj.join([account.get(name) for account in data.get(app)])
    conf.append([name,value,app])
    
    return conf
