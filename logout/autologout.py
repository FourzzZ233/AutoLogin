import requests

with open("./file.txt",'r+') as f:
    strs = []   #   0位是ip地址，1位是userindex
    for i in f.readlines():
        strs.append(str(i).replace("\n",""))    
    server_ip = strs[0] #存储一下ip地址
    #print(strs)
    # redirect_location = requests.get(url=strs[0],allow_redirects=False)
    # print(redirect_location.status_code)
    # print(redirect_location.headers)
    # lc = requests.get(url=redirect_location.headers.get('Location'),allow_redirects=False)
    # print(lc.status_code)
    # print(lc.headers)
    while(requests.get(url=strs[0],allow_redirects=False).status_code == 302):
        strs[0] = requests.get(url=strs[0],allow_redirects=False).headers.get('Location')
        print("Redirecting to "+strs[0])
    final_url = requests.get(strs[0]).url
    print("Now we enter " + final_url)

    logout_url = server_ip + '/eportal/InterFace.do?method=logout'
    logout_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": server_ip, "Connection": "close", "Referer": final_url}
    logout_data = {"userIndex":strs[1]}
    logout_response = requests.post(url=logout_url,headers=logout_headers,data=logout_data)
    if "success" in logout_response.text:
        logout_response.encoding = 'utf-8'  #解决中文乱码问题
        print(logout_response.status_code)
        print(logout_response.text)
    else:
        print("Error!!!")
        print(logout_response.content)