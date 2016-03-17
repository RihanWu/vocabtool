"""Use urllib for web communication"""

from sys import hexversion
# Check python version
if hexversion < 0x300000:
    import urllib2 as req
    import urllib as par
else:
    import urllib.request as req
    import urllib.parse as par


class Response():
    def __init__(self, data, charset='UTF-8'):
        self.text = data.decode(charset)


def _get_encoding(ctstr):
    return ctstr[ctstr.find('charset')+8:]


def _gunzip(data):
    if hexversion < 0x300000:
        import zlib
        return zlib.decompress(data, 16 + zlib.MAX_WBITS)
    else:
        import gzip
        return gzip.decompress(data)


def _inflate(data):
    import zlib
    try:
        return zlib.decompress(data)
    except zlib.error:
        return zlib.decompress(data, -zlib.MAX_WBITS)


def get(urlStr, params={}):
    """Get content on urlStr with params"""

    reqdata = req.Request(urlStr)
    reqdata.add_header('User-Agent',
                       'VocabTool/0.2 (https://github.com/RihanWu/vocabtool)')
    reqdata.add_header('Accept-Encoding', 'gzip, deflate')
    if params != {}:
        reqdata.data = par.urlencode(params).encode('ascii')
    resp = req.urlopen(reqdata)
    if resp.headers.get('Content-Encoding'):
        if resp.headers.get('Content-Encoding') == 'gzip':
            result = _gunzip(resp.read())
        elif resp.headers.get('Content-Encoding') == 'deflate':
            result = _inflate(resp.read())
        else:
            result = resp.read()
    else:
        result = resp.read()
    content_type = resp.headers.get('Content-Type')
    if (content_type and content_type.find('charset') != -1):
        return Response(result, _get_encoding(content_type))
    else:
        return Response(result)
