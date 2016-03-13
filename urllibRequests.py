import sys
if sys.hexversion < 50331648:
    import urllib2 as uReq
    import urllib as uPar
else:
    import urllib.request as uReq
    import urllib.parse as uPar

class Response:
    def __init__(self,data,charset='UTF-8'):
        self.text = data.decode(charset)

def getEncoding(ctstr):
    return ctstr[ctstr.find('charset')+8:]

def gunzip(data):
    if sys.hexversion < 50331648:
        import zlib
        return zlib.decompress(data,16+zlib.MAX_WBITS)
    else:
        import gzip
        return gzip.decompress(data)

def inflate(data):
    import zlib
    try:
        return zlib.decompress(data)
    except zlib.error:
        return zlib.decompress(data,-zlib.MAX_WBITS)

def get(urlStr,params={}):
    reqdata = uReq.Request(urlStr)
    reqdata.add_header('User-Agent',
                       'VocabTool/0.2 (https://github.com/RihanWu/vocabtool)')
    reqdata.add_header('Accept-Encoding','gzip, deflate')
    if params != {}:
        reqdata.data = uPar.urlencode(params).encode('ascii')
    req = uReq.urlopen(reqdata)
    if req.headers.get('Content-Encoding') is not None:
        print(req.headers.get('Content-Encoding'))
        if req.headers.get('Content-Encoding') == 'gzip':
            result = gunzip(req.read())
        elif req.headers.get('Content-Encoding') == 'deflate':
            result = inflate(req.read())
        else:
            result = req.read()
    else:
        result = req.read()
    if (req.headers.get('Content-Type') is not None and
        req.headers.get('Content-Type').find('charset') != -1):
        return Response(result,getEncoding(req.headers.get('Content-Type')))
    else:
        return Response(result)
