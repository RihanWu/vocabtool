"""Use urllib for web communication"""

from sys import hexversion
# Check python version
if hexversion < 0x300000:
    import urllib2 as req
    import urllib as par
else:
    import urllib.request as req
    import urllib.parse as par


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


def get(urlStr, params=None, codec=""):
    """Get content on urlStr with params"""

    # Construct request
    reqdata = req.Request(urlStr)
    reqdata.add_header('User-Agent',
                       'VocabTool/0.2 (https://github.com/RihanWu/vocabtool)')
    reqdata.add_header('Accept-Encoding', 'gzip, deflate')
    if params:
        reqdata.data = par.urlencode(params).encode('ascii')
    resp = req.urlopen(reqdata)

    # Parse response
    if resp.headers.get('Content-Encoding'):
        if resp.headers.get('Content-Encoding') == 'gzip':
            result = _gunzip(resp.read())
        elif resp.headers.get('Content-Encoding') == 'deflate':
            result = _inflate(resp.read())
        else:
            result = resp.read()
    else:
        result = resp.read()

    # Decode result
    if codec:
        return result.decode(codec)
    else:
        content_type = resp.headers.get('Content-Type')
        if (content_type and content_type.find('charset') != -1):
            encoding = content_type[content_type.find('charset')+8:]
            return result.decode(encoding)
        # Default use UTF-8 to decode
        else:
            return result.decode('UTF-8')
