# -*- coding: utf-8 -*-
"""生成 6 张泳道图（活动图）SVG。

泳道为纵向列，活动自上而下流动，箭头跨泳道时走折线。
输出：build/diagrams/<file>.svg

用法：  python build/gen_swimlanes.py
"""

import os
from xml.sax.saxutils import escape as E

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams")

FS = 13.0            # 节点文字字号
LANE_HEAD = 30       # 泳道表头高
PAD_TOP = 16
PAD_BOT = 22
NODE_PAD_X = 13
NODE_PAD_Y = 9
MIN_LANE = 168
MAX_LANE = 300
GAP = 34             # 相邻秩之间的垂直间隙

LANE_BG = ["#F7FBFC", "#FFFFFF"]
CFG = dict(
    stroke="#0E7490", fill="#E6F4F8", text="#12333D",
    dec_stroke="#B45309", dec_fill="#FEF6E7",
    start_fill="#0E7490", end_stroke="#0E7490",
    line="#94A3B8",
)


def text_w(s, fs=FS):
    """估算字符串像素宽度（中文按 1em，西文按 0.55em）。"""
    w = 0.0
    for ch in s:
        w += fs if ord(ch) > 0x2E80 else fs * 0.55
    return w


def wrap(s, maxw, fs=FS):
    """按宽度换行，中文逐字断行。"""
    lines, cur = [], ""
    for ch in s:
        if ch == "\n":
            lines.append(cur); cur = ""
            continue
        if text_w(cur + ch, fs) > maxw and cur:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines or [""]


def node_h(text, width, kind):
    if kind in ("start", "end"):
        return 34
    if kind == "decision":
        return 58
    inner = width - 2 * NODE_PAD_X
    n = len(wrap(text, inner))
    return max(38, n * (FS + 5) + 2 * NODE_PAD_Y)


def build(d):
    lanes, nodes, edges = d["lanes"], d["nodes"], d["edges"]

    # ---- 泳道宽度按内容估算 ----
    lw = []
    for i, name in enumerate(lanes):
        cand = [text_w(name, FS + 1.5)]
        cand += [text_w(v[2]) for v in nodes.values() if v[0] == i]
        lw.append(int(max(MIN_LANE, min(MAX_LANE, max(cand) + 2 * NODE_PAD_X + 8))))
    # 左留白：供回边绕行并放置回边标签
    back_labels = [e[2] for e in edges
                   if len(e) > 3 and e[3].get("back") and len(e) > 2 and e[2]]
    left = int(max([text_w(l, 11) for l in back_labels] + [0]) + 40) if back_labels else 0
    total_w = sum(lw) + left

    # ---- 秩（最长路径），忽略回边 ----
    back = set()
    for e in edges:
        if len(e) > 3 and e[3].get("back"):
            back.add((e[0], e[1]))
    adj = {k: [] for k in nodes}
    indeg = {k: 0 for k in nodes}
    for e in edges:
        if (e[0], e[1]) in back:
            continue
        adj[e[0]].append(e[1])
        indeg[e[1]] += 1

    rank = {k: 0 for k in nodes}
    indeg2 = dict(indeg)
    q = [k for k in nodes if indeg2[k] == 0]
    while q:
        n = q.pop(0)
        for m in adj[n]:
            rank[m] = max(rank[m], rank[n] + 1)
            indeg2[m] -= 1
            if indeg2[m] == 0:
                q.append(m)

    # 节点可带第 4 个元素指定显示次序（用于调整分支的上下位置）
    for k, v in nodes.items():
        if len(v) > 3:
            rank[k] = v[3]
    for e in edges:
        if len(e) > 3 and e[3].get("back"):
            continue
        if rank[e[1]] <= rank[e[0]]:
            print(f"    ⚠ {d.get('name','?')}: 边 {e[0]}→{e[1]} 未向下 "
                  f"({rank[e[0]]}→{rank[e[1]]})")

    # ---- 同一（秩, 泳道）单元内的节点纵向堆叠，避免重叠 ----
    nrank = max(rank.values()) + 1
    VG = GAP // 2
    cells = {}
    for k in nodes:
        cells.setdefault((rank[k], nodes[k][0]), []).append(k)

    def cell_h(ks, li):
        return (sum(node_h(nodes[k][2], lw[li], nodes[k][1]) for k in ks)
                + VG * (len(ks) - 1))

    row_h = [0] * nrank
    for (r, li), ks in cells.items():
        row_h[r] = max(row_h[r], cell_h(ks, li))

    row_y, y = [], PAD_TOP
    for r in range(nrank):
        row_y.append(y)
        y += row_h[r] + GAP

    # ---- 几何 ----
    lane_x, x = [], left
    for w in lw:
        lane_x.append(x)
        x += w
    cx = [lane_x[i] + lw[i] / 2 for i in range(len(lanes))]

    pos = {}
    for (r, li), ks in cells.items():
        off = row_y[r] + (row_h[r] - cell_h(ks, li)) / 2
        for k in ks:
            kind, txt = nodes[k][1], nodes[k][2]
            nh = node_h(txt, lw[li], kind)
            pos[k] = dict(l=lane_x[li] + NODE_PAD_X, t=off, w=lw[li] - 2 * NODE_PAD_X,
                          h=nh, cx=cx[li], kind=kind, txt=txt)
            off += nh + VG

    total_h = y - GAP + PAD_BOT
    H = total_h + LANE_HEAD

    # ---- 输出 ----
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{H}" '
         f'viewBox="0 0 {total_w} {H}" font-family="Microsoft YaHei,SimHei,sans-serif">']
    s.append('<defs>'
             '<marker id="ar" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto">'
             f'<path d="M0,0 L9,4.5 L0,9 z" fill="{CFG["line"]}"/></marker>'
             '<marker id="ar2" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto">'
             f'<path d="M0,0 L9,4.5 L0,9 z" fill="{CFG["stroke"]}"/></marker>'
             '</defs>')

    s.append(f'<g transform="translate(0,{LANE_HEAD})">')
    for i in range(len(lanes)):
        s.append(f'<rect x="{lane_x[i]}" y="{-LANE_HEAD}" width="{lw[i]}" height="{H}" '
                 f'fill="{LANE_BG[i % 2]}" stroke="#D7E3E8"/>')
    for i, name in enumerate(lanes):
        s.append(f'<rect x="{lane_x[i]}" y="{-LANE_HEAD}" width="{lw[i]}" height="{LANE_HEAD}" '
                 f'fill="#0B4251"/>')
        s.append(f'<text x="{cx[i]}" y="{-LANE_HEAD + 20}" text-anchor="middle" font-size="13.5" '
                 f'fill="#FFFFFF" font-weight="bold">{E(name)}</text>')

    # 连线先画，节点覆盖其上
    for e in edges:
        src, dst = e[0], e[1]
        label = e[2] if len(e) > 2 else ""
        opt = e[3] if len(e) > 3 else {}
        a, b = pos[src], pos[dst]

        if opt.get("back"):
            xs = max(12, left - 14)
            y1, y2 = a["t"] + a["h"] / 2, b["t"] + b["h"] / 2
            s.append(f'<path d="M{a["l"]},{y1:.1f} L{xs},{y1:.1f} L{xs},{y2:.1f} '
                     f'L{b["l"] - 2},{y2:.1f}" fill="none" stroke="{CFG["line"]}" stroke-width="1.3" '
                     f'stroke-dasharray="5,4" marker-end="url(#ar)"/>')
            if label:
                s.append(f'<text x="{xs - 8:.1f}" y="{(y1 + y2) / 2:.1f}" text-anchor="end" '
                         f'font-size="11" fill="{CFG["dec_stroke"]}">{E(label)}</text>')
            continue

        y1, y2 = a["t"] + a["h"], b["t"]
        mid = (y1 + y2) / 2
        dash = ' stroke-dasharray="5,4"' if opt.get("dashed") else ""
        mk = "ar" if opt.get("dashed") else "ar2"
        if abs(a["cx"] - b["cx"]) < 1.5:
            d_attr = f'M{a["cx"]:.1f},{y1:.1f} L{b["cx"]:.1f},{y2 - 1:.1f}'
        else:
            d_attr = (f'M{a["cx"]:.1f},{y1:.1f} L{a["cx"]:.1f},{mid:.1f} '
                      f'L{b["cx"]:.1f},{mid:.1f} L{b["cx"]:.1f},{y2 - 1:.1f}')
        s.append(f'<path d="{d_attr}" fill="none" stroke="{CFG["line"]}" stroke-width="1.3"'
                 f'{dash} marker-end="url(#{mk})"/>')
        if label:
            lx = (a["cx"] + b["cx"]) / 2 if abs(a["cx"] - b["cx"]) > 1.5 else a["cx"] + 9
            ly = mid - 4
            tw = text_w(label, 11) + 8
            s.append(f'<rect x="{lx - tw / 2:.1f}" y="{ly - 11}" width="{tw:.1f}" height="15" rx="3" '
                     f'fill="#FFFFFF" fill-opacity="0.92"/>')
            s.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="11" '
                     f'fill="{CFG["dec_stroke"]}">{E(label)}</text>')

    # 节点
    for k, v in nodes.items():
        p = pos[k]
        kind, txt = v[1], v[2]
        if kind == "start":
            s.append(f'<circle cx="{p["cx"]:.1f}" cy="{p["t"] + p["h"] / 2:.1f}" r="13" '
                     f'fill="{CFG["start_fill"]}"/>')
        elif kind == "end":
            s.append(f'<circle cx="{p["cx"]:.1f}" cy="{p["t"] + p["h"] / 2:.1f}" r="14" '
                     f'fill="#FFFFFF" stroke="{CFG["end_stroke"]}" stroke-width="2"/>')
            s.append(f'<circle cx="{p["cx"]:.1f}" cy="{p["t"] + p["h"] / 2:.1f}" r="8.5" '
                     f'fill="{CFG["end_stroke"]}"/>')
        elif kind == "decision":
            cxx, cyy = p["cx"], p["t"] + p["h"] / 2
            hw, hh = p["w"] / 2, p["h"] / 2
            s.append(f'<polygon points="{cxx:.1f},{cyy - hh:.1f} {cxx + hw:.1f},{cyy:.1f} '
                     f'{cxx:.1f},{cyy + hh:.1f} {cxx - hw:.1f},{cyy:.1f}" '
                     f'fill="{CFG["dec_fill"]}" stroke="{CFG["dec_stroke"]}" stroke-width="1.4"/>')
            lines = wrap(txt, p["w"] * 0.62, FS - 1)
            for i, ln in enumerate(lines):
                ly = cyy - (len(lines) - 1) * 8 + i * 16 + 4.5
                s.append(f'<text x="{cxx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="{FS - 1}" '
                         f'fill="#7A4A08">{E(ln)}</text>')
        else:
            s.append(f'<rect x="{p["l"]:.1f}" y="{p["t"]:.1f}" width="{p["w"]:.1f}" '
                     f'height="{p["h"]:.1f}" rx="6" fill="{CFG["fill"]}" '
                     f'stroke="{CFG["stroke"]}" stroke-width="1.3"/>')
            lines = wrap(txt, p["w"] - 2 * NODE_PAD_X)
            for i, ln in enumerate(lines):
                ly = p["t"] + (p["h"] - len(lines) * (FS + 5)) / 2 + i * (FS + 5) + FS + 1
                s.append(f'<text x="{p["cx"]:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="{FS}" '
                         f'fill="{CFG["text"]}">{E(ln)}</text>')
    s.append('</g></svg>')

    return "\n".join(s), total_w, H


# ==========================================================================
# 六张泳道图的定义
# ==========================================================================
def D2_1():
    L = ["用户 / 访客", "系统", "管理员", "科研人员 / 教师", "数据服务"]
    # 第 4 个数字为显示次序：登录分支排在注册分支之前，避免读成「先注册再登录」
    N = {
        "s":  (0, "start", "开始", 0),
        "a1": (0, "action", "访问系统", 1),
        "d1": (0, "decision", "是否已有账号？", 2),
        "a4": (0, "action", "登录（用户名 / 密码 / 验证码）", 3),
        "a3": (0, "action", "提交注册申请", 4),
        "b2": (1, "action", "生成待审核申请单", 5),
        "c1": (2, "action", "审核注册申请", 6),
        "c2": (2, "action", "分配角色 / 配置权限", 7),
        "b1": (1, "action", "校验身份与角色权限", 8),
        "b3": (1, "action", "发放会话令牌，装载权限", 9),
        "b4": (1, "action", "按权限过滤菜单与数据范围", 10),
        "a5": (0, "action", "按角色进入对应功能", 11),
        "r1": (3, "action", "维护物种信息（模块二）", 11),
        "a6": (0, "action", "查看公开物种信息 / 使用智能服务", 12),
        "r2": (3, "action", "维护生态系统与观测记录（模块三）", 12),
        "r3": (3, "action", "在观测中关联多个物种", 13),
        "e2": (4, "action", "智能服务（模块五）识别 / 补全 / 问答", 13),
        "e1": (4, "action", "数据可视化与报表（模块四）", 14),
        "b5": (1, "action", "记录用户活动日志", 15),
        "z":  (0, "end", "结束", 16),
    }
    E_ = [
        ("s", "a1", ""), ("a1", "d1", ""),
        ("d1", "a4", "是"), ("d1", "a3", "否"),
        ("a3", "b2", ""), ("b2", "c1", ""), ("c1", "c2", ""), ("c2", "b1", ""),
        ("a4", "b1", ""),
        ("b1", "b3", ""), ("b3", "b4", ""),
        ("b4", "a5", ""), ("a5", "a6", ""),
        ("b4", "a6", "公众"), ("a6", "z", ""),
        ("b4", "r1", "科研人员 / 教师"),
        ("r1", "r2", ""), ("r2", "r3", ""),
        ("r1", "e1", "", {"dashed": True}), ("r3", "e1", "", {"dashed": True}),
        ("r2", "e2", "", {"dashed": True}),
        ("e1", "z", ""), ("e2", "z", ""),
        ("b1", "b5", "", {"dashed": True}), ("c2", "b5", "", {"dashed": True}),
        ("r3", "b5", "", {"dashed": True}),
        ("b5", "z", "", {"dashed": True}),
    ]
    return dict(lanes=L, nodes=N, edges=E_, name="diagram-2-1")


def D3_1():
    L = ["申请者", "系统", "管理员"]
    N = {
        "s":  (0, "start", "开始"),
        "a1": (0, "action", "访问注册页面"),
        "a2": (0, "action", "选择申请角色（学生 / 公众）"),
        "a3": (0, "action", "填写并提交注册申请"),
        "b1": (1, "action", "校验表单：用户名唯一、密码规则、邮箱格式"),
        "b2": (1, "action", "生成申请单，状态 = 待审核"),
        "b3": (1, "action", "向管理员推送待办"),
        "c1": (2, "action", "查看待审核申请列表"),
        "c2": (2, "action", "打开申请详情"),
        "d1": (2, "decision", "审核结论？"),
        "c4": (2, "action", "填写审核意见，选择授予角色"),
        "b5": (1, "action", "创建账号，写入角色关系"),
        "b4": (1, "action", "发送账号开通 / 驳回通知邮件"),
        "a6": (0, "action", "接收审核结果通知"),
        "b6": (1, "action", "记录用户活动日志"),
        "z":  (0, "end", "结束"),
    }
    E_ = [
        ("s", "a1", ""), ("a1", "a2", ""), ("a2", "a3", ""), ("a3", "b1", ""),
        ("b1", "a3", "校验不通过", {"back": True}),
        ("b1", "b2", "校验通过"), ("b2", "b3", ""), ("b3", "c1", ""),
        ("c1", "c2", ""), ("c2", "d1", ""),
        ("d1", "c4", "通过 / 驳回"), ("c4", "b5", "通过"),
        ("c4", "b4", "驳回"), ("b5", "b4", ""),
        ("b4", "a6", ""), ("a6", "z", ""),
        ("b5", "b6", "", {"dashed": True}), ("c4", "b6", "", {"dashed": True}),
        ("b6", "z", "", {"dashed": True}),
    ]
    return dict(lanes=L, nodes=N, edges=E_)


def D4_1():
    L = ["科研人员 / 教师", "系统"]
    N = {
        "s":  (0, "start", "开始"),
        "a1": (0, "action", "请求新增物种信息"),
        "b1": (1, "action", "显示分步录入表单（第 1 步 / 共 3 步）"),
        "a2": (0, "action", "填写分类与基本信息（门纲目科属种）"),
        "a3": (0, "action", "填写形态特征、生活习性"),
        "a4": (0, "action", "标注分布区域（经纬度 / 地图选点）"),
        "a5": (0, "action", "上传图片、填写视频链接与参考文献"),
        "a7": (0, "action", "提交保存"),
        "b3": (1, "action", "校验必填项与字段格式"),
        "d1": (1, "decision", "中文名 / 学名是否已存在？"),
        "b5": (1, "action", "提示疑似重复，展示已有记录"),
        "b6": (1, "action", "生成物种编号，写入数据库"),
        "b7": (1, "action", "记录操作日志"),
        "b2": (1, "action", "调用大模型 AI 智能补全分类与描述"),
        "z":  (0, "end", "结束"),
    }
    E_ = [
        ("s", "a1", ""), ("a1", "b1", ""), ("b1", "a2", ""), ("a2", "a3", ""),
        ("a3", "a4", ""), ("a4", "a5", ""), ("a5", "a7", ""), ("a7", "b3", ""),
        ("b3", "a2", "校验不通过", {"back": True}),
        ("b3", "d1", "校验通过"), ("d1", "b5", "是"), ("b5", "b6", "确认非重复"),
        ("d1", "b6", "否"),
        ("b6", "b7", ""), ("b7", "z", ""),
        ("a3", "b2", "AI 补全", {"dashed": True}),
    ]
    return dict(lanes=L, nodes=N, edges=E_)


def D5_1():
    L = ["科研人员 / 教师", "系统", "大模型服务（模块五）"]
    N = {
        "s":  (0, "start", "开始"),
        "a1": (0, "action", "请求新建观测记录"),
        "b1": (1, "action", "显示分步向导（第 1 步 / 共 4 步）"),
        "a2": (0, "action", "填写观测时间、地点、生态系统、观测人员"),
        "a3": (0, "action", "在地图上选点，回填经纬度"),
        "a4": (0, "action", "填写环境参数（水温、盐度、pH、溶解氧等）"),
        "b2": (1, "action", "校验必填项与环境参数取值范围"),
        "a5": (0, "action", "检索目标物种"),
        "b3": (1, "action", "从模块二返回匹配的物种候选列表"),
        "d1": (1, "decision", "候选列表中是否存在目标物种？"),
        "b6": (1, "action", "提供「新增物种」入口"),
        "a6": (0, "action", "选择一个或多个物种，逐个记录估算数量与行为"),
        "b4": (1, "action", "建立观测—物种关联关系"),
        "a8": (0, "action", "填写本次观测总体备注"),
        "a9": (0, "action", "确认提交"),
        "b7": (1, "action", "生成观测编号，写入数据库"),
        "b8": (1, "action", "更新模块四统计数据"),
        "b9": (1, "action", "记录操作日志"),
        "c1": (2, "action", "依据地点、时间、生态系统生成自动标签"),
        "c2": (2, "action", "检测观测数据与物种分布的冲突"),
        "z":  (0, "end", "结束"),
    }
    E_ = [
        ("s", "a1", ""), ("a1", "b1", ""), ("b1", "a2", ""), ("a2", "a3", ""),
        ("a3", "a4", ""), ("a4", "b2", ""),
        ("b2", "a2", "校验不通过", {"back": True}),
        ("b2", "a5", "校验通过"), ("a5", "b3", ""), ("b3", "d1", ""),
        ("d1", "b6", "否"), ("b6", "a5", "登记后重试", {"back": True}),
        ("d1", "a6", "是"), ("a6", "b4", ""), ("b4", "a8", ""),
        ("a8", "a9", ""), ("a9", "b7", ""), ("b7", "b8", ""), ("b8", "b9", ""),
        ("b7", "c1", "", {"dashed": True}), ("b4", "c2", "", {"dashed": True}),
        ("c1", "z", "", {"dashed": True}),
        ("c2", "a9", "异常提示，请核实", {"dashed": True, "back": True}),
        ("b9", "z", ""),
    ]
    return dict(lanes=L, nodes=N, edges=E_)


def D6_1():
    L = ["用户", "系统（模块四）", "模块二 物种信息", "模块三 观测记录"]
    N = {
        "s":  (0, "start", "开始"),
        "a1": (0, "action", "请求进入综合数据看板"),
        "b1": (1, "action", "并发请求模块二与模块三的数据接口"),
        "c1": (2, "action", "返回物种记录与分布点数据"),
        "c2": (3, "action", "返回观测记录、地点与生态系统数据"),
        "b2": (1, "action", "数据聚合与统计计算（分类占比、保护等级占比、观测次数）"),
        "b3": (1, "action", "渲染概览卡片、折线图、环形图、条形图"),
        "a2": (0, "action", "查看概览卡片与统计图表"),
        "a3": (0, "action", "下钻至物种分布地图 / 观测地点地图"),
        "a4": (0, "action", "选择报表类型、数据范围、时间范围与格式"),
        "d1": (1, "decision", "当前角色是否有导出权限？"),
        "b5": (1, "action", "按模板生成 Excel / PDF 报表"),
        "a5": (0, "action", "下载报表文件"),
        "b6": (1, "action", "记录导出操作至用户活动日志"),
        "z":  (0, "end", "结束"),
    }
    E_ = [
        ("s", "a1", ""), ("a1", "b1", ""), ("b1", "c1", ""), ("b1", "c2", ""),
        ("c1", "b2", ""), ("c2", "b2", ""), ("b2", "b3", ""), ("b3", "a2", ""),
        ("a2", "a3", ""), ("a3", "a4", ""), ("a4", "d1", ""),
        ("d1", "a4", "否，提示无权限", {"back": True}),
        ("d1", "b5", "是"), ("b5", "a5", ""), ("a5", "b6", ""), ("b6", "z", ""),
    ]
    return dict(lanes=L, nodes=N, edges=E_)


def D7_1():
    L = ["用户", "系统", "大模型服务", "模块二 物种信息"]
    N = {
        "s":  (0, "start", "开始"),
        "a1": (0, "action", "上传海洋生物图片（1～5 张）"),
        "a2": (0, "action", "设置识别参数（模式、置信度阈值、候选数）"),
        "a3": (0, "action", "发起智能识别"),
        "b1": (1, "action", "图片预处理与敏感信息过滤（去除 EXIF）"),
        "b2": (1, "action", "调用大模型多模态接口（超时与重试）"),
        "c1": (2, "action", "多模态识别：图像 → 物种名称与置信度"),
        "d1": (1, "decision", "最高置信度是否 ≥ 设定阈值？"),
        "b5": (1, "action", "返回最优结果与 Top N 候选列表"),
        "b6": (1, "action", "与模块二物种库比对，推荐关联记录"),
        "dd": (3, "action", "提供物种库匹配与已有记录"),
        "a5": (0, "action", "查看识别结果与候选列表"),
        "a6": (0, "action", "选择候选物种"),
        "a8": (0, "action", "对低置信度结果发起人工确认流程"),
        "a7": (0, "action", "采纳并关联 / 新建物种记录"),
        "b7": (1, "action", "将图片与分布点写入物种记录"),
        "b8": (1, "action", "记录识别日志（时间、置信度、操作人）"),
        "z":  (0, "end", "结束"),
    }
    E_ = [
        ("s", "a1", ""), ("a1", "a2", ""), ("a2", "a3", ""), ("a3", "b1", ""),
        ("b1", "b2", ""), ("b2", "c1", ""), ("c1", "d1", ""),
        ("d1", "b5", "是"), ("d1", "a8", "否，转人工确认"),
        ("b5", "b6", ""), ("b6", "dd", ""), ("dd", "a5", "返回匹配结果"),
        ("a8", "a6", "人工选择"), ("a5", "a6", ""), ("a6", "a7", ""),
        ("a7", "b7", ""), ("b7", "b8", ""), ("b8", "z", ""),
    ]
    return dict(lanes=L, nodes=N, edges=E_)


DIAGRAMS = [
    ("diagram-2-1", "系统总体业务流程图", D2_1),
    ("diagram-3-1", "用户注册与审核活动图", D3_1),
    ("diagram-4-1", "新增物种信息活动图", D4_1),
    ("diagram-5-1", "创建观测记录并关联多个物种活动图", D5_1),
    ("diagram-6-1", "查看综合数据看板并导出报表活动图", D6_1),
    ("diagram-7-1", "图像智能识别与物种鉴定活动图", D7_1),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    cards = []
    lock = []
    for name, title, fn in DIAGRAMS:
        svg, w, h = build(fn())
        with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(svg)
        cards.append(f'<div class="card" id="{name}"><img src="{name}.svg" '
                     f'width="{w}" height="{h}"></div>')
        lock.append(f'  ("{name}", {w}, {h}, "{title}"),')
        print(f"  ✓ {name:<14} {title:<34} {w}×{h} px")

    with open(os.path.join(OUT, "preview.html"), "w", encoding="utf-8") as fh:
        fh.write('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
                 'body{margin:0;background:#fff;font-family:sans-serif}'
                 '.card{display:block;margin:0;padding:0;background:#fff}'
                 '.card img{display:block}'
                 '</style></head><body>' + "".join(cards) + '</body></html>')

    # 供 gen_report.py 读取的尺寸表
    with open(os.path.join(OUT, "sizes.py"), "w", encoding="utf-8") as fh:
        fh.write("# 自动生成：泳道图文件名与像素尺寸\nSIZES = {\n" + "\n".join(lock) + "\n}\n")

    print(f"\n共 {len(DIAGRAMS)} 张泳道图 → {OUT}")
    print("预览页 → preview.html　尺寸表 → sizes.py")


if __name__ == "__main__":
    main()
