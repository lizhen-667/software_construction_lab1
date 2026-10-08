# -*- coding: utf-8 -*-
"""生成全部系统原型页面 HTML，并写出页面索引。

用法：  python build/gen_wireframes.py
输出：  build/wireframes/<PAGE_ID>.html
        build/pages.json   （页面索引：[{id, title, file}]）
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pages_a  # noqa: E402
import pages_b  # noqa: E402
import pages_c  # noqa: E402
import pages_d  # noqa: E402
import pages_e  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "wireframes")
BAR = "─" * 68


def main():
    os.makedirs(OUT, exist_ok=True)

    groups = [
        ("模块一 用户与权限管理", pages_a.pages()),
        ("模块二 物种信息管理", pages_b.pages()),
        ("模块三 生态系统与观测记录管理", pages_c.pages()),
        ("模块四 数据可视化与报表", pages_d.pages()),
        ("模块五 智能服务", pages_e.pages()),
    ]

    index, seen = [], set()
    for gname, plist in groups:
        print(f"\n{BAR}\n{gname}\n{BAR}")
        for pid, title, html in plist:
            if pid in seen:
                raise SystemExit(f"页面编号重复：{pid}")
            seen.add(pid)
            path = os.path.join(OUT, pid + ".html")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(html)
            index.append({"id": pid, "title": title, "group": gname, "file": pid + ".html"})
            print(f"  ✓ {pid:<14} {title:<24} {len(html):>7,} B")

    with open(os.path.join(HERE, "pages.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2)

    print(f"\n{BAR}\n共生成 {len(index)} 个原型页面 → {OUT}")
    print(f"页面索引 → {os.path.join(HERE, 'pages.json')}")


if __name__ == "__main__":
    main()
