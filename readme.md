# mitm_server_for_QL
## How to install
#
#### pip install -r requirements.txt
#### mitmdump (generate cert at /root/.mitmproxy)
#### \cp -rf /root/.mitmproxy/* .mitmproxy/
#### then copy cert to phone and trust it
#### go to qinglong settings-->appsetting and save it to ql/qlconf.toml
####    
#### python main.py  
#### ps -aux | grep "python main.py"
#### default port: 
#### 40080 http proxy, need auth with username and password of login page
#### 40082 webpage
#### some useful http proxy app: shadowrocket(ios) proxydroid(android) swithyomega(chrome)
## How to use
# 
#### sign up and it will generate your toml
#### or just login or edit
![image](https://github.com/HanEightTurtle/mitm_server/raw/master/IMG/login.png)
#### in user page, use your http proxy app to connect port 40080, dont forget authentication
![image](https://github.com/HanEightTurtle/mitm_server/raw/master/IMG/user.png)
#### then open app which needs to be captured, such as jd
#### see logs of user page, if capture succeed
#### then click renew button, it would refresh app status
#### finally, click submit, it would submit your appdata to ql
# 
## Add new addons
#### If u have any other ck needed to capture, just follow samples under folder 'addons'.
## Add new qlsend
#### just see ql/ql_sample.py
####
#
## Output:
#### There are user_tomls under folder 'tomls'. And all_data.toml under folder 'output'
