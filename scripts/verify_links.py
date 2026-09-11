#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量核验 coffee-circuit data.json 中每条 link 的真实页面标题，判断与卡片赛事是否对应"""
import json, re, urllib.request, ssl, sys

UA_PC = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
UA_MOBILE = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(url, ua, timeout=18, follow=True):
    req = urllib.request.Request(url, headers=ua)
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
    try:
        with opener.open(req, timeout=timeout) as r:
            final = r.geturl()
            body = r.read(600000).decode("utf-8", errors="ignore")
            return final, body
    except Exception as e:
        return url, "ERROR: %s" % e

def extract_title(html):
    m = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]*)"', html)
    if m: return m.group(1)[:120]
    m = re.search(r'<meta[^>]+name="og:title"[^>]+content="([^"]*)"', html)
    if m: return m.group(1)[:120]
    m = re.search(r'<title[^>]*>([^<]{5,150})</title>', html)
    if m: return m.group(1).strip()[:120]
    m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', html)
    if m: return "DESC: " + m.group(1)[:120]
    return "(无标题信息)"

def main():
    with open(r"D:\# 本地AI任务\coffee-circuit-gh\data.json", encoding="utf-8") as f:
        data = json.load(f)
    for e in data["events"]:
        url = e.get("link", "")
        # 抖音链接换标准视频页抓标题（分享页不返回标题）
        m = re.search(r"video/(\d+)", url)
        if m and ("douyin" in url or "iesdouyin" in url):
            url = "https://www.douyin.com/video/%s" % m.group(1)
        ua = UA_MOBILE if ("douyin" in url or "iesdouyin" in url) else UA_PC
        final, body = fetch(url, ua)
        title = extract_title(body)
        print("=" * 90)
        print("[%02d] %s" % (e["id"], e["name"]))
        print("     期望: %s | %s | %s" % (e["date"], e["place"], e["ch"]))
        print("     link: %s" % url[:95])
        print("     实际跳转: %s" % final[:95])
        print("     页面标题/描述: %s" % title)

if __name__ == "__main__":
    sys.exit(main())
