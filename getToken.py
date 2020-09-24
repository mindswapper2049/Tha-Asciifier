import urllib.request

host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=&client_secret="
request = urllib.request.Request(host)
request.add_header("Content-Type", "application/json; charset=UTF-8")
response = urllib.request.urlopen(request)
content = response.read()
if content:
    print(content)
