import urllib.request, re
req = urllib.request.Request('https://nync.yn.gov.cn/html/zhuantizhuanlan/2025kmhz/yilanhuazhan/', headers={'User-Agent':'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'ignore')
for m in re.finditer(r'href="([^"]+)"[^>]*>([^<]*(?:报名通道|双赛盛典)[^<]*)<', html):
    print(m.group(2).strip(), '->', m.group(1))
