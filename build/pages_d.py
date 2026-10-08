# -*- coding: utf-8 -*-
"""模块四：数据可视化与报表 —— 原型页面定义（MB-VIS-*）。"""

from wire_kit import *  # noqa: F401,F403

PROT_COLORS = [("#b91c1c", "极危 CR"), ("#ea580c", "濒危 EN"), ("#d97706", "易危 VU"),
               ("#0891b2", "近危 NT"), ("#15803d", "无危 LC"), ("#94a3b8", "数据缺乏 DD")]


def _p1():
    """MB-VIS-1 综合数据看板。"""
    lc = line_chart(
        ["11月", "12月", "1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月"],
        [("观测次数", "#0e7490", [6, 5, 7, 9, 14, 18, 21, 19, 16, 13, 11, 9]),
         ("新增物种记录", "#22c55e", [12, 9, 15, 11, 24, 31, 28, 22, 19, 17, 14, 12])],
        w=700, h=228, ymax=40)

    dn = donut([("极危 CR", 46, "#b91c1c"), ("濒危 EN", 98, "#ea580c"), ("易危 VU", 173, "#d97706"),
                ("近危 NT", 214, "#0891b2"), ("无危 LC", 612, "#15803d"), ("数据缺乏 DD", 143, "#94a3b8")])

    body = (stats([
        stat("物种总数", "1,286", "种", "＋38", icon="🐟"),
        stat("观测记录", "1,342", "条", "＋24", icon="📍"),
        stat("生态系统", "12", "个", "＋1", icon="🌿"),
        stat("参与人员", "28", "人", "＋3", icon="👥"),
    ]) + '<div class="cols"><div style="flex:1">'
        + card("", '<div class="chartbox" style="border:none;padding:0">'
               '<h3>观测活动与物种收录趋势（近 12 个月）</h3>'
               '<div class="cs">数据来源：模块三（观测次数）· 模块二（新增物种记录）</div>'
               + lc + '</div>')
        + '</div><div style="width:404px;flex:0 0 404px">'
        + card("", '<div class="chartbox" style="border:none;padding:0">'
               '<h3>物种保护等级构成</h3><div class="cs">数据来源：模块二 · 共 1,286 种</div>'
               + '<div style="display:flex;align-items:center;gap:16px">' + dn
               + '<div style="flex:1">'
               + bars([("极危 CR", "46", 8), ("濒危 EN", "98", 16), ("易危 VU", "173", 28),
                       ("近危 NT", "214", 35), ("无危 LC", "612", 100), ("数据缺乏", "143", 23)])
               + '</div></div></div>')
        + '</div></div>'
        + '<div class="cols" style="margin-top:13px">'
        + '<div style="width:560px;flex:0 0 560px">'
        + card("各生态系统观测次数", '<div class="chartbox" style="border:none;padding:0">'
               '<div class="cs" style="margin-bottom:10px">数据来源：模块三 · 近 12 个月累计</div>'
               + hbar_chart([("红树林", 61, "#15803d"), ("河口 / 浅海", 45, "#0891b2"),
                             ("珊瑚礁", 34, "#b91c1c"), ("海草床", 28, "#22c55e"),
                             ("深海", 6, "#475569")], w=500)
               + '</div>', tag="单位：次")
        + '</div>'
        + '<div style="flex:1">'
        + card("最新数据动态", '<div class="tl">'
               '<div class="it"><span class="d"></span><div class="c">'
               '<b>张海宁</b> 新增观测记录 OBS-2026-0142（关联 1 个物种）'
               '<div class="tm">2026-10-08 11:05 · 湛江港航道外侧</div></div></div>'
               '<div class="it"><span class="d"></span><div class="c">'
               '<b>王庆林</b> 更新物种「鹿角珊瑚」保护等级为 极危 CR'
               '<div class="tm">2026-10-07 16:48</div></div></div>'
               '<div class="it"><span class="d"></span><div class="c">'
               '<b>李雨欣</b> 新增观测记录 OBS-2026-0139（关联 3 个物种）'
               '<div class="tm">2026-09-28 09:12 · 流沙湾海草床东区</div></div></div>'
               '<div class="it"><span class="d g"></span><div class="c">'
               '<b>张海宁</b> 新增物种「中华白海豚」'
               '<div class="tm">2026-10-08 08:55</div></div></div>'
               '</div><div style="margin-top:11px;display:flex;gap:8px">'
               + btn("查看全部动态") + btn("导出版本看板", "pri") + '</div>', tag="实时")
        + '</div></div>')
    return ("MB-VIS-1", "综合数据看板", shell("vis", "数据可视化与报表 / 综合数据看板",
            "综合数据看板", "MB-VIS-1",
            actions=btn("刷新数据") + btn("导出看板 PDF", "pri"), body=body))


def _p2():
    """MB-VIS-2 物种分布地图。"""
    m = mapbox(850, 600, pins=[
        (120, 340, "#b91c1c"), (168, 300, "#b91c1c"), (210, 372, "#ea580c"),
        (262, 265, "#d97706"), (310, 318, "#0891b2"), (356, 402, "#15803d"),
        (402, 246, "#b91c1c"), (448, 352, "#ea580c"), (494, 292, "#d97706"),
        (540, 398, "#15803d"), (586, 258, "#0891b2"), (632, 330, "#b91c1c"),
        (678, 288, "#ea580c"), (724, 366, "#15803d"), (770, 248, "#d97706"),
        (330, 448, "#0891b2"), (560, 452, "#15803d"), (720, 452, "#b91c1c"),
    ], pop=popup(600, 180, "中华白海豚 Sousa chinensis", [
        ("保护等级", '<span class="tag err">易危 VU</span>'),
        ("记录数", "8 个分布点"),
        ("分布区域", "珠江口、湛江港、雷州湾"),
        ("最近观测", "2026-10-08 OBS-2026-0142"),
    ]), land=[(60, 240, 300, 180, -6), (430, 210, 340, 160, 5), (640, 380, 240, 130, -4)],
        scale="Leaflet | 物种分布点 | 50 km")

    body = ('<div class="cols"><div style="width:282px;flex:0 0 282px">'
            + card("筛选条件", field("物种名称", "中华白海豚", req=True)
                   + field("保护等级", "全部", "sel")
                   + field("分类阶元", "全部", "sel")
                   + field("观测时间", "2023-01-01 ~ 2026-10-08", "date")
                   + field("数据来源", "物种信息库（模块二）", "sel")
                   + '<div style="display:flex;gap:8px;margin-top:4px">' + btn("查询", "pri") + btn("重置") + '</div>')
            + card("图例（保护等级）", legend([(c, t) for c, t in PROT_COLORS])
                   + '<div class="hr"></div><div class="mini" style="margin-bottom:7px">'
                     '当前显示 <b>8</b> 个分布点（中华白海豚）</div>'
                   + bars([("湛江港", 3, 100), ("雷州湾", 2, 67), ("硇洲岛", 2, 67), ("珠江口", 1, 33)]))
            + card("统计摘要", dl_list([("分布点数", "8 个"), ("涉及生态系统", "3 个"),
                                       ("最近更新", "2026-10-08")], "92px 1fr"))
            + '</div><div style="flex:1">' + card("", m, pad=False) + '</div></div>')
    return ("MB-VIS-2", "物种分布地图", shell("vis", "数据可视化与报表 / 物种分布地图",
            "物种分布地图", "MB-VIS-2",
            actions=btn("导出地图图片") + btn("导出点位数据", "pri"), body=body))


def _p3():
    """MB-VIS-3 观测地点地图。"""
    m = mapbox(850, 600, pins=[
        (150, 330, "#0e7490"), (232, 292, "#0e7490"), (286, 366, "#dc2626"),
        (338, 250, "#0e7490"), (392, 404, "#0e7490"), (446, 296, "#0e7490"),
        (500, 344, "#0e7490"), (554, 258, "#0e7490"), (608, 396, "#0e7490"),
        (662, 300, "#0e7490"), (716, 352, "#0e7490"), (770, 262, "#0e7490"),
        (300, 452, "#0e7490"), (520, 446, "#0e7490"), (690, 440, "#0e7490"),
    ], pop=popup(470, 170, "OBS-2026-0142 · 湛江港航道外侧", [
        ("观测时间", "2026-10-08 09:20"),
        ("生态系统", '<span class="tag">河口 / 浅海</span>'),
        ("观测人员", "张海宁、王庆林、李雨欣"),
        ("水温 / 盐度", "26.4 ℃ / 30.2 ‰"),
        ("关联物种", '<b>1</b> 个（中华白海豚）'),
    ]), land=[(80, 230, 310, 190, -6), (450, 200, 350, 170, 5), (650, 370, 230, 140, -4)],
        scale="Leaflet | 观测地点 | 50 km")

    body = ('<div class="cols"><div style="width:282px;flex:0 0 282px">'
            + card("筛选条件", field("观测编号", "全部")
                   + field("生态系统", "全部", "sel")
                   + field("观测人员", "全部", "sel")
                   + field("观测时间", "2025-10-01 ~ 2026-10-08", "date")
                   + field("关联物种", "全部", "sel")
                   + '<div style="display:flex;gap:8px;margin-top:4px">' + btn("查询", "pri") + btn("重置") + '</div>')
            + card("图例", legend([("#0e7490", "一般观测点"), ("#dc2626", "含濒危物种观测点")])
                   + '<div class="hr"></div><div class="mini" style="margin-bottom:9px">'
                     '按生态系统着色（可选）</div>'
                   + legend([("#15803d", "红树林"), ("#0891b2", "河口/浅海"),
                             ("#b91c1c", "珊瑚礁"), ("#22c55e", "海草床"), ("#475569", "深海")]))
            + card("点位概览", dl_list([("观测点总数", "142 个"), ("本年度新增", "38 个"),
                                       ("覆盖生态系统", "5 类")], "92px 1fr")
                   + '<div class="mini" style="margin-top:9px">点击地图上的标记可查看该次观测的概要信息，'
                     '并可跳转至观测记录详情页（MB-OBS-4）。</div>')
            + '</div><div style="flex:1">' + card("", m, pad=False) + '</div></div>')
    return ("MB-VIS-3", "观测地点地图", shell("vis", "数据可视化与报表 / 观测地点地图",
            "观测地点地图", "MB-VIS-3",
            actions=btn("导出地图图片") + btn("导出点位数据", "pri"), body=body))


def _p4():
    """MB-VIS-4 物种统计分析。"""
    body = ('<div class="cols">'
            + '<div style="width:430px;flex:0 0 430px">'
            + card("", '<div class="chartbox" style="border:none;padding:0">'
                   '<h3>各分类单元占比</h3><div class="cs">数据来源：模块二 · 按物种数统计</div>'
                   + '<div style="display:flex;align-items:center;gap:14px">'
                   + donut([("脊索动物门", 612, "#0e7490"), ("节肢动物门", 238, "#0891b2"),
                            ("软体动物门", 186, "#22c55e"), ("刺胞动物门", 124, "#d97706"),
                            ("被子植物门", 74, "#ea580c"), ("其他", 52, "#94a3b8")], 168)
                   + '<div style="flex:1">'
                   + bars([("脊索动物门", "612", 100), ("节肢动物门", "238", 39),
                           ("软体动物门", "186", 30), ("刺胞动物门", "124", 20),
                           ("被子植物门", "74", 12), ("其他", "52", 8)]) + '</div></div></div>')
            + '</div>'
            + '<div style="flex:1">'
            + card("", '<div class="chartbox" style="border:none;padding:0">'
                   + '<h3>各门物种数（按保护等级堆叠）</h3>'
                   + '<div class="cs">数据来源：模块二 · 纵轴为物种数（种）</div>'
                   + grouped_bar(["脊索动物门", "节肢动物门", "软体动物门", "刺胞动物门", "被子植物门", "其他"],
                                 [("极危/濒危", "#b91c1c", [52, 14, 22, 41, 9, 6]),
                                  ("易危/近危", "#d97706", [118, 36, 44, 52, 21, 12]),
                                  ("无危/数据缺乏", "#0891b2", [442, 188, 120, 31, 44, 34])],
                                 w=690, h=224)
                   + legend([("#b91c1c", "极危 CR / 濒危 EN"), ("#d97706", "易危 VU / 近危 NT"),
                             ("#0891b2", "无危 LC / 数据缺乏 DD")]) + '</div>')
            + '</div></div>'
            + '<div class="cols" style="margin-top:13px">'
            + '<div style="width:560px;flex:0 0 560px">'
            + card("保护等级占比", '<div class="chartbox" style="border:none;padding:0">'
                   '<div class="cs" style="margin-bottom:11px">数据来源：模块二 · 共 1,286 种</div>'
                   + hbar_chart([("无危 LC", 612, "#15803d"), ("近危 NT", 214, "#0891b2"),
                                 ("易危 VU", 173, "#d97706"), ("数据缺乏 DD", 143, "#94a3b8"),
                                 ("濒危 EN", 98, "#ea580c"), ("极危 CR", 46, "#b91c1c")], w=500)
                   + '</div>')
            + '</div>'
            + '<div style="flex:1">'
            + card("重点保护物种（名录内）", table(
                ["物种", "保护等级", "分布生态系统", "观测次数"],
                [['<span class="lk">中华白海豚</span>', '<span class="tag err">国家一级</span>', "河口 / 浅海", "8"],
                 ['<span class="lk">绿海龟</span>', '<span class="tag err">国家一级</span>', "珊瑚礁、海草床", "5"],
                 ['<span class="lk">鹿角珊瑚</span>', '<span class="tag err">国家二级</span>', "珊瑚礁", "34"],
                 ['<span class="lk">秋茄（红树林）</span>', '<span class="tag warn">国家二级</span>', "红树林", "61"],
                 ['<span class="lk">锦绣龙虾</span>', '<span class="tag">—</span>', "珊瑚礁", "12"]])
                + '<div style="padding:0 16px 4px"><span class="mini">'
                  '点击物种名称可跳转至物种详情页（MB-SPEC-4）。</span></div>', pad=False)
            + '</div></div>')
    return ("MB-VIS-4", "物种统计分析", shell("vis", "数据可视化与报表 / 统计分析",
            "物种统计分析", "MB-VIS-4",
            actions=btn("切换图表类型") + btn("导出图表数据", "pri"), body=body))


def _p5():
    """MB-VIS-5 生态系统与观测活动统计。"""
    body = (card("", '<div class="chartbox" style="border:none;padding:0">'
                 '<h3>各生态系统观测次数与发现物种数</h3>'
                 '<div class="cs">数据来源：模块三 · 近 12 个月</div>'
                 + grouped_bar(["红树林", "河口/浅海", "珊瑚礁", "海草床", "深海"],
                               [("观测次数", "#0e7490", [61, 45, 34, 28, 6]),
                                ("发现物种数", "#22c55e", [98, 76, 126, 54, 31])],
                               w=1120, h=250)
                 + legend([("#0e7490", "观测次数（次）"), ("#22c55e", "发现物种数（种）")]) + '</div>')
            + '<div class="cols" style="margin-top:13px">'
            + '<div style="flex:1">'
            + card("", '<div class="chartbox" style="border:none;padding:0">'
                   '<h3>观测活动月度趋势（按生态系统）</h3>'
                   '<div class="cs">数据来源：模块三 · 2026 年 1–10 月</div>'
                   + line_chart(["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月"],
                                [("红树林", "#15803d", [3, 4, 8, 11, 13, 12, 9, 7, 6, 5]),
                                 ("河口/浅海", "#0891b2", [2, 3, 4, 5, 6, 7, 8, 7, 5, 4]),
                                 ("珊瑚礁", "#b91c1c", [1, 2, 2, 2, 1, 2, 4, 3, 3, 3])],
                                w=680, h=210, ymax=15)
                   + legend([("#15803d", "红树林"), ("#0891b2", "河口 / 浅海"), ("#b91c1c", "珊瑚礁")])
                   + '</div>')
            + '</div>'
            + '<div style="width:412px;flex:0 0 412px">'
            + card("观测人员贡献统计", '<div class="chartbox" style="border:none;padding:0">'
                   '<div class="cs" style="margin-bottom:11px">数据来源：模块三 · 近 12 个月观测次数</div>'
                   + hbar_chart([("张海宁", 46, "#0e7490"), ("王庆林", 38, "#0891b2"),
                                 ("李雨欣", 24, "#22c55e"), ("陈志远", 18, "#d97706"),
                                 ("林嘉怡", 11, "#94a3b8"), ("其他", 5, "#cbd5e1")], w=352)
                   + '</div>')
            + '</div></div>'
            + '<div style="height:13px"></div>'
            + card("生态系统统计明细", table(
                ["生态系统", "类型", "观测次数", "发现物种数", "关联物种记录数", "最近观测", "操作"],
                [['<span class="lk">湛江红树林生态系统</span>', '<span class="tag ok">红树林</span>', "61", "98", "142", "2026-10-05", '<span class="lk">查看该生态系统统计</span>'],
                 ['<span class="lk">雷州湾河口浅海生态系统</span>', '<span class="tag">河口/浅海</span>', "45", "76", "118", "2026-10-08", '<span class="lk">查看该生态系统统计</span>'],
                 ['<span class="lk">徐闻珊瑚礁生态系统</span>', '<span class="tag pri">珊瑚礁</span>', "34", "126", "204", "2026-10-06", '<span class="lk">查看该生态系统统计</span>'],
                 ['<span class="lk">流沙湾海草床</span>', '<span class="tag info">海草床</span>', "28", "54", "76", "2026-09-28", '<span class="lk">查看该生态系统统计</span>'],
                 ['<span class="lk">琼东南深海冷泉区</span>', '<span class="tag warn">深海</span>', "6", "31", "38", "2026-08-14", '<span class="lk">查看该生态系统统计</span>']]),
                pad=False))
    return ("MB-VIS-5", "生态系统与观测活动统计", shell("vis", "数据可视化与报表 / 统计分析",
            "生态系统与观测活动统计", "MB-VIS-5",
            actions=btn("切换统计维度") + btn("导出图表数据", "pri"), body=body))


def _p6():
    """MB-VIS-6 报表导出。"""
    rows = [
        ["TB20261008-03", "物种分布统计报表", "全库物种（1,286 种）", "2026-10-01 ~ 2026-10-08",
         '<span class="tag pri">Excel</span>', '<span class="tag ok">已完成</span>',
         "张海宁", "2026-10-08 10:32", '<span class="lnks"><span class="lk">下载</span><span class="lk p">删除</span></span>'],
        ["TB20261008-02", "综合数据看板快照", "全系统概览", "截至 2026-10-08",
         '<span class="tag err">PDF</span>', '<span class="tag warn">生成中…</span>',
         "王庆林", "2026-10-08 09:58", '<span class="lnks"><span class="lk p">下载</span><span class="lk p">删除</span></span>'],
        ["TB20261007-11", "观测活动统计报表", "雷州湾河口浅海生态系统", "2026-01-01 ~ 2026-10-07",
         '<span class="tag pri">Excel</span>', '<span class="tag ok">已完成</span>',
         "王庆林", "2026-10-07 17:21", '<span class="lnks"><span class="lk">下载</span><span class="lk p">删除</span></span>'],
        ["TB20261006-08", "物种名录（重点保护）", "国家一级 / 二级保护物种", "截至 2026-10-06",
         '<span class="tag err">PDF</span>', '<span class="tag ok">已完成</span>',
         "张海宁", "2026-10-06 14:05", '<span class="lnks"><span class="lk">下载</span><span class="lk p">删除</span></span>'],
    ]
    body = ('<div class="cols"><div style="width:640px;flex:0 0 640px">'
            + card("报表导出配置", form_title("1", "报表内容") + '<div class="grid2">'
                   + field("报表类型", "物种分布统计报表", "sel", req=True)
                   + field("统计维度", "按物种 × 生态系统", "sel", req=True)
                   + field("数据范围", "全部物种（1,286 种）", "sel", req=True)
                   + field("时间范围", "2026-10-01 ~ 2026-10-08", "date", req=True)
                   + field("数据来源", "模块二（物种）· 模块三（观测）", span=True)
                   + '</div><div class="hr"></div>'
                   + form_title("2", "输出格式与字段") + '<div class="grid2">'
                   + field("导出格式", "Excel (.xlsx)", "sel", req=True,
                           hint="Excel 便于二次统计；PDF 便于存档与打印")
                   + field("纸张方向", "横向", "sel")
                   + field("包含图表", "是（嵌入统计图）", "sel")
                   + field("文件名", "物种分布统计报表_20261008", "sel")
                   + '</div>'
                   + '<div style="margin-top:13px"><div class="mini" style="margin-bottom:8px">'
                     '导出字段（可多选）</div><div class="chips">'
                   + "".join(f'<span class="tag pri">{t}</span>' for t in
                             ["物种编号", "中文名", "学名", "门", "纲", "目", "科", "属",
                              "保护等级", "IUCN 等级", "分布区域", "分布点数", "观测次数", "关联生态系统"])
                   + '</div></div>'
                   + '<div style="margin-top:16px;display:flex;gap:9px">'
                   + btn("生成并下载报表", "pri") + btn("预览报表") + btn("保存为常用配置") + '</div>')
            + '</div><div style="flex:1">'
            + card("导出说明", note("报表数据实时取自模块二与模块三。导出动作将记入用户活动日志；"
                                   "单次导出上限 50,000 行，超出时系统自动分页生成多个文件。"
                                   "PDF 报表按 A4 横版排版，包含图表与数据附表。", blue=True)
                   + '<div style="height:11px"></div>'
                   + note("导出内容涉及校内科研数据，请遵守《数据使用规范》，不得擅自对外扩散。", title="数据合规提示"))
            + '<div style="height:13px"></div>'
            + card("最近导出记录", '<div class="tl">'
                   '<div class="it"><span class="d"></span><div class="c">'
                   '<b>物种分布统计报表</b>（Excel）<div class="tm">张海宁 · 2026-10-08 10:32</div></div></div>'
                   '<div class="it"><span class="d"></span><div class="c">'
                   '<b>观测活动统计报表</b>（Excel）<div class="tm">王庆林 · 2026-10-07 17:21</div></div></div>'
                   '<div class="it"><span class="d g"></span><div class="c">'
                   '<b>物种名录（重点保护）</b>（PDF）<div class="tm">张海宁 · 2026-10-06 14:05</div></div></div>'
                   '</div>')
            + '</div></div>'
            + '<div style="height:13px"></div>'
            + card("导出任务列表", table(
                ["任务编号", "报表名称", "数据范围", "时间范围", "格式", "状态", "导出人", "导出时间", "操作"],
                rows) + '<div style="padding:0 12px 4px">' + pager("共 34 条记录") + '</div>', pad=False))
    return ("MB-VIS-6", "报表导出", shell("vis", "数据可视化与报表 / 报表导出",
            "报表导出", "MB-VIS-6", actions=btn("导出记录管理"), body=body))


def pages():
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6()]
