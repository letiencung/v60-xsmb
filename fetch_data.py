#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tai du lieu XSMB moi nhat tu xosodaiphat.com -> data.json (chay tren GitHub Actions)."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import re, json, urllib.request
from datetime import datetime, timezone, timedelta

LABELS = [
    ("G.DB", "Đặc biệt", 1, 5, True), ("G.1", "Giải nhất", 1, 5, False),
    ("G.2", "Giải nhì", 2, 5, False), ("G.3", "Giải ba", 6, 5, False),
    ("G.4", "Giải tư", 4, 4, False), ("G.5", "Giải năm", 6, 4, False),
    ("G.6", "Giải sáu", 3, 3, False), ("G.7", "Giải bảy", 4, 2, False),
]

def main():
    req = urllib.request.Request("https://xosodaiphat.com/xsmb-xo-so-mien-bac.html",
                                 headers={"User-Agent": "Mozilla/5.0"})
    page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
    page = page.replace("G.ĐB", "G.DB")
    marks = [(m.group(1), m.group(2), m.group(3), m.start())
             for m in re.finditer(r"xsmb-(\d{2})-(\d{2})-(\d{4})\.html", page)]
    seen, days = set(), []
    for i, (d, mo, y, idx) in enumerate(marks):
        dd = f"{d}-{mo}-{y}"
        if dd in seen: continue
        seen.add(dd)
        end = marks[i+1][3] if i+1 < len(marks) else len(page)
        part = page[idx:end]
        data, ok = [], True
        for gl, tl, ct, sz, sp in LABELS:
            pm = re.search(r"<td>" + re.escape(gl) + r"([\s\S]*?)(?=<td>G\.|$)", part)
            if not pm: ok = False; break
            nums = re.findall(r">(\d+)</span>", pm.group(1))
            if len(nums) != ct or any(len(n) != sz for n in nums): ok = False; break
            obj = {"label": tl, "numbers": nums}
            if sp: obj["special"] = True
            data.append(obj)
        if not ok: continue
        # Kiem tra 107 chu so
        total = sum(len(n) for row in data for n in row["numbers"])
        if total != 107: continue
        days.append({"day": dd, "data": data})
    days.sort(key=lambda x: datetime.strptime(x["day"], "%d-%m-%Y"))
    if len(days) < 3:
        raise SystemExit("LOI: khong du du lieu (< 3 ngay)")
    vn_now = datetime.now(timezone(timedelta(hours=7))).isoformat()
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"updated": vn_now, "days": days}, f, ensure_ascii=False, separators=(",", ":"))
    print(f"OK: {len(days)} ngay, {days[0]['day']} -> {days[-1]['day']}, GDB={days[-1]['data'][0]['numbers'][0]}")

if __name__ == "__main__":
    main()
