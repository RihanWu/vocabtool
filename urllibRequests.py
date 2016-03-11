import urllib.request

def get(urlStr):
    req = urllib.request.urlopen(urlStr)
    return req.read()
