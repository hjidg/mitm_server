

import requests
import time
import json

def ql_ini(qlurl,qlid,qlsecret):
    '''
    '''
    url = f'{qlurl}/open/auth/token?client_id={qlid}&client_secret={qlsecret}'
    headers = {'Content-Type':'text/json' }
    r = requests.get(url=url,headers=headers)
    token = r.json().get('data').get('token')
    return token

def ql_get_user_envs(qlurl,token,username):
    '''
        remarks = {app}: {username}
        env = {'value':xxx,'name':xxx,'status':x,'_id':xxx}
    '''
    # envs
    url = f'{qlurl}/open/envs?t={int(time.time())}'
    headers = {'Authorization': f'Bearer {token}','Content-Type':'text/json' }
    r = requests.get(url=url,headers=headers)
    qlenvs = r.json().get('data')
    return [env for env in qlenvs if username==env.get('remarks').split(': ')[-1]]

def ql_envs(qlurl,token):
    '''
        env = {'value':xxx,'name':xxx,'status':x,'_id':xxx}
    '''
    # envs
    url = f'{qlurl}/open/envs?t={int(time.time())}'
    headers = {'Authorization': f'Bearer {token}','Content-Type':'text/json' }
    r = requests.get(url=url,headers=headers)
    qlenvs = r.json().get('data')
    return qlenvs

def ql_add(qlurl,token,name,value,remarks):
    reqData = {
        'name':name,
        'value':value,
        'remarks':remarks,
    }
    url = f'{qlurl}/open/envs?t={int(time.time())}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    body = [reqData]
    r = requests.post(url=url,headers=headers,data=json.dumps(body))
    return r.text

def ql_update(qlurl,token,name,value,remarks,_id):
    reqData = {
        'name':name,
        'value':value,
        'remarks':remarks,
        '_id':_id,
    }
    url = f'{qlurl}/open/envs?t={int(time.time())}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    body = reqData
    r = requests.put(url=url,headers=headers,data=json.dumps(body))
    return r.text

def ql_delete(qlurl,token,_id):
    url = f'{qlurl}/open/envs?t={int(time.time())}'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    body = [_id]
    r = requests.delete(url=url,headers=headers,data=json.dumps(body))
    return r.text
