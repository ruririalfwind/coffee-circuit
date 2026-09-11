#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
咖啡赛事台 · 每日自动巡检脚本
抓取 HOTELEX（上海博华）官方咖啡赛事栏目，把新赛事自动合并进 data.json。
只新增"完全未收录"的赛事，不覆盖人工维护的已有条目信息。
"""
import json, re, sys, datetime, urllib.request, os

HOTELEX_URL = "https://www.hotelex.cn/category/event/competition/coffee"
BASE = "https://www.hotelex.cn"
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data.json")
KEYWORDS = ["咖啡", "杯测", "冲煮", "拉花", "烘焙", "烈酒", "潮饮"]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def cat_of(title):
    if "杯测" in title or "品鉴" in title: return "tasting"
    if "冲煮" in title: return "brew"
    if "拉花" in title: return "latte"
    if "咖啡师" in title: return "barista"
    if "烘焙" in title: return "roast"
    return "sensory"

def fetch_html(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="ignore")

def parse_events(html):
    """从 HOTELEX 赛事页提取 (标题, 链接) 列表"""
    found = []
    for m in re.finditer(r'<a[^>]+href="([^"]*?(?:archives|competition/coffee)[^"]*)"[^>]*>([^<]{6,90})</a>', html):
        href, title = m.group(1), m.group(2).strip()
        if not any(k in title for k in KEYWORDS):
            continue
        if not re.search(r"202[67]", title):
            continue
        url = href if href.startswith("http") else BASE + href
        found.append({"title": title, "url": url})
    # 去重
    seen, out = set(), []
    for e in found:
        if e["title"] not in seen:
            seen.add(e["title"]); out.append(e)
    return out

def main():
    today = datetime.date.today().isoformat()
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    events = data.get("events", [])
    known = {e.get("name") for e in events}
    max_id = max((e.get("id", 0) for e in events), default=0)

    added = []
    try:
        html = fetch_html(HOTELEX_URL)
        remote = parse_events(html)
    except Exception as exc:
        print("抓取失败，保留现有数据：", exc)
        data["updated"] = today
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return 0

    for e in remote:
        if e["title"] in known:
            continue
        max_id += 1
        events.append({
            "id": max_id,
            "name": e["title"],
            "cat": cat_of(e["title"]),
            "lv": "国际 · 中国区",
            "date": "以官方公布为准",
            "place": "以官方公布为准",
            "fee": "以官方为准",
            "status": "open",
            "statusTxt": "自动收录 · 以官方为准",
            "region": "全国",
            "desc": "由每日自动巡检从 HOTELEX 官方赛事页抓取，具体赛区、时间与报名以官方详情为准。",
            "route": "分赛区 → 中国区 → 世界赛",
            "ch": "hotelex.cn · HOTELEX 公众号",
            "src": "来源：HOTELEX 官网（自动抓取）",
            "link": e["url"],
            "linkTxt": "HOTELEX 官方详情",
            "isNew": True
        })
        known.add(e["title"])
        added.append(e["title"])

    events.sort(key=lambda x: x.get("id", 0))
    data["events"] = events
    data["updated"] = today
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    if added:
        print("本次新增 %d 项赛事：" % len(added))
        for t in added:
            print("  +", t)
    else:
        print("无新增赛事。")
    return 0

if __name__ == "__main__":
    sys.exit(main())
