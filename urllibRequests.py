import urllib.request
import urllib.parse

def get(urlStr,params={}):
    reqdata = urllib.request.Request(urlStr)
    reqdata.add_header('User-Agent',
                       'VocabTool/0.2 (https://github.com/RihanWu/vocabtool)')
    if params != {}:
        reqdata.data = urllib.parse.urlencode(params).encode('ascii')
    req = urllib.request.urlopen(reqdata)
    return req.read()
