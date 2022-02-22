# mitm_server_for_QL
## How to use
#
#### pip install -r requirements.txt
#### 先运行mitmdump 自动生成证书，再拷贝到当前目录下 \cp -rf /root/.mitmproxy/* .mitmproxy/，证书传到手机并信任该证书
#### 去qinglong系统设置-->应用设置生成的配置 添加到 ql/qlconf.toml
#### default port: 
#### 40080 http proxy, need auth with username and password of login page
#### 40082 webpage
#### some useful http proxy app: shadowrocket(ios) proxydroid(android) swithyomega(chrome)
![image](https://github.com/HanEightTurtle/mitm_server/tree/master/IMG/login.png)
![image](https://github.com/HanEightTurtle/mitm_server/tree/master/IMG/user.png)
# 
## Add new addons
#### If u have any other ck needed to capture, just follow samples under folder 'addons'.
## Add new qlsend
#### just see ql/ql_sample.py
####
#
## Output:
#### There are user_tomls under folder 'tomls'. And all_data.toml under folder 'output'
