CRLF = '\r\n'


class ResponseMock(object):

    def __init__(self, code, status, headers, body, content_id):
        self.status_code = int(code)
        self.status_message = status
        self.headers = headers
        self.content = body
        self.content_id = content_id


def build_multipart(items, payload=None):
        from urllib2 import urlparse
        boundary = 'gapi_uniq_boundary'

        contents = []
        if payload:
            contents.append(payload)
        item_id = 0
        for uuid, item in items.items():
            lines = []
            url_parts = urlparse.urlsplit(item['url'])
            if url_parts.query:
                path = '%s?%s' % (url_parts.path, url_parts.query)
            else:
                path = url_parts.path
            lines.append("--" + boundary)
            if item['payload']:
                lines.append('Content-Length: %s' % len(item['payload']))
            lines.append("Content-Type: application/http")
            lines.append("Content-ID: <item:%s>" % uuid)
            lines.append("")
            lines.append("%s %s" % (item['method'], path))
            for header_name, header_value in item['headers'].items():
                lines.append("%s: %s" % (header_name, header_value))
            if item['payload']:
                lines.append("Content-Length: %s" % len(item['payload']))
            lines.append("")
            if item['payload']:
                lines.append(item['payload'])
            contents.append(CRLF.join(lines))
            item_id += 1

        payload = CRLF.join(contents) + CRLF + ('--%s--' % boundary)

        headers = {
            'content-type': 'multipart/mixed; boundary=%s' % boundary,
            'Content-Length': len(payload),
        }

        return headers, payload


def parse_multipart(response):
    headers, body = response.headers, response.content
    boundary = headers['content-type'].split('boundary=')[1]
    body.rstrip('--' + boundary + '--' + CRLF)
    items = body.split('--' + boundary)
    responses = {}
    items.pop(0)
    item_id = 1
    for item in items:
        lines = item.split(CRLF)
        lines.pop(0)
        if lines == [u''] and item_id == len(items):
            break
        boundary_headers = parse_headers(lines)
        http_ver, http_code, http_status = lines.pop(0).split(' ')
        item_headers = parse_headers(lines)
        item_body = CRLF.join(lines)
        content_id = boundary_headers['content-id']
        content_id = content_id[1:-1].split('item:', 1)[1]
        responses[content_id] = ResponseMock(http_code, http_status, item_headers, item_body, content_id=content_id)
        item_id += 1
    return responses


def parse_header(header_line):
    key, val = header_line.split(':', 1)
    return key.strip().lower(), val.strip()


def parse_headers(lines):
    line = lines.pop(0)
    headers = []
    while line:
        headers.append(parse_header(line))
        line = lines.pop(0)
    return dict(headers)


if __name__ == '__main__':
    import json
    parse_multipart(*json.loads(open('/tmp/tmp.json').read()))
