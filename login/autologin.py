import os
import sys
import requests

def response_status(obj:object):
    print(obj.status_code)
    print(obj.headers)
    print(obj.text)
    
current_dir = os.getcwd()
sys.path.append(current_dir)
import YourAccount
#print(YourAccount.uid) 测试导入是否成功


dcr = requests.get("http://192.168.10.1")
detect_response = dcr.text
if(detect_response[:31] != "<script>top.self.location.href="):
    print("Warning!You should check your network or you've already pass the check!")
else:
    print("Entering login_page......")
    relocation = detect_response.split('\'')[1] #获取重定向后的地址
    print(relocation)
    server_address = relocation.split('index.jsp?')[0]  #截断获取host验证地址根目录，以此作为登录页面的前半部分
    server_ip = server_address.replace('/eportal/','')  #获取hostip
    queryStrings = relocation.split('index.jsp?')[1]    #截断获取login所需参数queryString
    username = str(YourAccount.uid)   #用户名
    password = str(YourAccount.pwd)     #密码
    login_url = server_address + "InterFace.do?method=login"
    login_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": server_ip, "Connection": "close", "Referer": relocation}
    login_data = {"userId" : username,"password" : password,"service" : '',"queryString" : queryStrings,"operatorPwd" : '',"operatorUserId" : '',"validcode": '', "passwordEncrypt": "false"}
    autologin_response = requests.post(url=login_url,headers = login_headers,data = login_data)
    if "userIndex" in autologin_response.text and "success" in autologin_response.text:
        response_status(autologin_response)
         #修改了判断条件
        print("Login Successfully!!!")
        success_text = autologin_response.text
        userindex = success_text.replace(':',',').replace('\"','').split(',')[1]
        with open("./file.txt",'r+') as f:  #这里用的./是因为需要在当前工作目录下
            f.truncate()
            f.write(str(server_ip) + '\n')
            f.write(str(userindex) + '\n')
        with open("./file.txt",'r+') as f:
            for i in  f.readlines():
                print(i)
            print("Welcome!Your userIndex is " + userindex)
    else:
        print("Error!!!!")
        response_status(autologin_response)
        
