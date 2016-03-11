import urllib.request
import urllib.parse

def get(urlStr,params={}):
    if params == {}:
        req = urllib.request.urlopen(urlStr)
    else:
        reqdata = urllib.request.Request(urlStr,urllib.parse.urlencode(params).encode('ascii'))
	req = urllib.request.urlopen(reqdata)
    return req.read()
