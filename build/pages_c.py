# -*- coding: utf-8 -*-
"""模块三：生态系统与观测记录管理 —— 原型页面定义（MB-ECO-* / MB-OBS-*）。"""

from wire_kit import *  # noqa: F401,F403


def _eco1():
    """MB-ECO-1 生态系统列表。"""
    rows = [
        [ck(), '<div class="thumb">🪸</div>', '<span class="lk">徐闻珊瑚礁生态系统</span>',
         '<span class="tag pri">珊瑚礁</span>', "徐闻县角尾乡近岸（110.21°E, 20.24°N）",
         "1,850 ha", "126", "34", "2026-10-06",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<div class="thumb">🌿</div>', '<span class="lk">湛江红树林生态系统</span>',
         '<span class="tag ok">红树林</span>', "湛江市麻章区、廉江市沿海（110.35°E, 21.15°N）",
         "7,240 ha", "218", "61", "2026-10-05",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<div class="thumb">🌱</div>', '<span class="lk">流沙湾海草床</span>',
         '<span class="tag info">海草床</span>', "雷州市流沙湾（109.92°E, 20.42°N）",
         "960 ha", "74", "28", "2026-09-28",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<div class="thumb">🌊</div>', '<span class="lk">雷州湾河口浅海生态系统</span>',
         '<span class="tag">河口 / 浅海</span>', "雷州湾中部（110.18°E, 20.86°N）",
         "3,400 ha", "152", "45", "2026-09-21",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<div class="thumb">🕳</div>', '<span class="lk">琼东南深海冷泉区</span>',
         '<span class="tag warn">深海</span>', "琼东南盆地（111.60°E, 18.90°N，水深 1,180 m）",
         "—", "31", "6", "2026-08-14",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
    ]
    body = (filters(
        [("生态系统名称", "text", "请输入名称关键字"),
         ("生态系统类型", "sel", "全部"),
         ("保护级别", "sel", "全部"),
         ("地理位置", "text", "输入地名或经纬度")],
        btn("查询", "pri") + btn("重置"))
        + card("", table(
            ["<span class='ck'></span>", "图", "生态系统名称", "类型", "地理位置（中心点）",
             "面积", "关联物种数", "观测次数", "最近观测", "操作"], rows)
            + '<div style="padding:0 16px 12px">' + btn("新建生态系统", "pri") + " "
            + btn("批量删除", "dg") + " " + btn("导出清单") + '</div>'
            + pager("共 12 个生态系统"), pad=False))
    return ("MB-ECO-1", "生态系统列表", shell("eco", "生态系统管理 / 生态系统列表",
            "生态系统列表", "MB-ECO-1",
            actions=btn("新建生态系统", "pri") + btn("在地图上查看"), body=body))


def _eco2():
    """MB-ECO-2 新建 / 编辑生态系统。"""
    body = (card("", form_title("1", "基本信息") + '<div class="grid3">'
                + field("生态系统名称", "徐闻珊瑚礁生态系统", req=True)
                + field("生态系统类型", "珊瑚礁", "sel", req=True,
                        hint="珊瑚礁 / 红树林 / 海草床 / 深海 / 河口浅海 / 潮间带")
                + field("保护级别", "国家级自然保护区", "sel")
                + field("中心点经度", "110.21")
                + field("中心点纬度", "20.24")
                + field("平均水深", "8.5 m")
                + field("面积", "1850 ha")
                + field("管理单位", "广东徐闻珊瑚礁国家级自然保护区管理局", span=True) + '</div>')
            + '<div style="height:13px"></div>'
            + card("", form_title("2", "地理范围与生态特征") + '<div class="grid3">'
                   + field("经度范围", "110.05°E ~ 110.38°E")
                   + field("纬度范围", "20.10°N ~ 20.38°N")
                   + field("岸线长度", "约 42 km")
                   + field("主导物种", "鹿角珊瑚、蜂巢珊瑚、石斑鱼、锦绣龙虾", span=True)
                   + field("生态特征描述", "分布于徐闻角尾乡至灯楼角一带近岸浅水区，以造礁石珊瑚为主，"
                           "共记录造礁石珊瑚 40 余种。礁区水质清澈，是南海北部重要的珊瑚礁分布区，"
                           "同时为多种经济鱼类提供育幼场与栖息地。", "area", span=True)
                   + field("主要威胁", "海水升温导致珊瑚白化、过度捕捞、沿岸工程泥沙淤积", "area", span=True)
                   + '</div>'
                   + '<div style="margin-top:13px">'
                   + mapbox(980, 240, pins=[(240, 120, "#0e7490"), (330, 100, "#0891b2"),
                                            (420, 140, "#0e7490"), (520, 108, "#0891b2")],
                            land=[(150, 60, 300, 140, -5), (520, 40, 240, 110, 6)],
                            scale="Leaflet | 可绘制多边形划定范围 | 20 km")
                   + '<div class="mini" style="margin-top:7px">当前绘制范围：'
                     '<b>4 个顶点</b> 多边形（点击「绘制范围」开始圈画，双击闭合多边形）。</div></div>')
            + '<div style="height:15px"></div><div style="display:flex;gap:9px">'
            + btn("保存", "pri") + btn("保存并继续新建") + btn("取消") + '</div>')
    return ("MB-ECO-2", "新建生态系统", shell("eco", "生态系统管理 / 新建生态系统",
            "新建生态系统", "MB-ECO-2", actions=btn("查看该生态系统历史"), body=body))


def _obs1():
    """MB-OBS-1 观测记录列表。"""
    rows = [
        [ck(), '<span class="lk">OBS-2026-0142</span>', "2026-10-08 09:20",
         "湛江港航道外侧<br><span class='mono'>110.42°E, 21.18°N</span>",
         '<span class="tag">河口 / 浅海</span>', "张海宁", "26.4 ℃ / 30.2 ‰",
         '<span class="tag pri">1</span>', '<span class="tag ok">已提交</span>',
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<span class="lk">OBS-2026-0141</span>', "2026-10-06 15:40",
         "徐闻珊瑚礁保护区南片<br><span class='mono'>110.22°E, 20.23°N</span>",
         '<span class="tag pri">珊瑚礁</span>', "王庆林", "27.1 ℃ / 33.8 ‰",
         '<span class="tag pri">6</span>', '<span class="tag ok">已提交</span>',
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<span class="lk">OBS-2026-0140</span>', "2026-10-05 10:05",
         "湛江红树林保护区高桥片<br><span class='mono'>109.88°E, 21.42°N</span>",
         '<span class="tag ok">红树林</span>', "张海宁", "28.6 ℃ / 24.7 ‰",
         '<span class="tag pri">4</span>', '<span class="tag ok">已提交</span>',
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<span class="lk">OBS-2026-0139</span>', "2026-09-28 08:50",
         "流沙湾海草床东区<br><span class='mono'>109.94°E, 20.44°N</span>",
         '<span class="tag info">海草床</span>', "李雨欣（学生）", "29.3 ℃ / 32.1 ‰",
         '<span class="tag pri">3</span>', '<span class="tag warn">待补全</span>',
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<span class="lk">OBS-2026-0138</span>', "2026-09-21 11:15",
         "雷州湾东部浅水区<br><span class='mono'>110.31°E, 20.81°N</span>",
         '<span class="tag">河口 / 浅海</span>', "王庆林", "28.1 ℃ / 31.4 ‰",
         '<span class="tag pri">5</span>', '<span class="tag ok">已提交</span>',
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<span class="lk">OBS-2026-0137</span>', "2026-08-14 16:30",
         "琼东南深海冷泉区<br><span class='mono'>111.60°E, 18.90°N</span>",
         '<span class="tag warn">深海</span>', "王庆林", "4.2 ℃ / 34.9 ‰",
         '<span class="tag pri">2</span>', '<span class="tag ok">已提交</span>',
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
    ]
    body = (filters(
        [("观测编号", "text", "如 OBS-2026-0142"),
         ("生态系统", "sel", "全部"),
         ("观测人员", "sel", "全部"),
         ("观测时间", "date", "2026-09-01 ~ 2026-10-08"),
         ("地理位置", "text", "输入地名或经纬度")],
        btn("查询", "pri") + btn("重置") + btn("导出记录"))
        + card("", table(
            ["<span class='ck'></span>", "观测编号", "观测时间", "地点（经纬度）", "生态系统",
             "观测人员", "水温 / 盐度", "关联物种", "状态", "操作"], rows)
            + '<div style="padding:0 16px 12px">' + btn("新建观测记录", "pri") + " "
            + btn("批量删除", "dg") + " "
            + '<span class="mini" style="margin-left:6px">「关联物种」列显示本次观测所关联的物种数，'
              '点击可跳转至关联详情</span></div>' + pager("共 142 条记录"), pad=False))
    return ("MB-OBS-1", "观测记录列表", shell("obs", "观测记录管理 / 观测记录列表",
            "观测记录列表", "MB-OBS-1",
            actions=btn("新建观测记录", "pri") + btn("在地图上查看"), body=body))


def _obs2():
    """MB-OBS-2 新建观测记录（第 2 步：环境参数）。"""
    body = (steps(["基本信息", "环境参数", "关联物种", "确认提交"], 2)
            + card("", form_title("1", "观测基本信息") + '<div class="grid3">'
                   + field("观测编号", "OBS-2026-0143", hint="系统自动生成")
                   + field("观测时间", "2026-10-08 09:20", "date", req=True)
                   + field("观测类型", "野外调查", "sel", req=True)
                   + field("所属生态系统", "河口 / 浅海 — 雷州湾河口浅海生态系统", "sel", req=True)
                   + field("观测人员", "张海宁、王庆林、李雨欣", req=True)
                   + field("天气 / 海况", "晴，风力 3 级，浪高 0.4 m", "sel")
                   + field("地点描述", "湛江港航道外侧约 2.5 km 处", span=True)
                   + field("经度", "110.42")
                   + field("纬度", "21.18")
                   + field("定位方式", "GPS 实测", "sel") + '</div>'
                   + '<div style="margin-top:13px">'
                   + mapbox(980, 210, pins=[(470, 96, "#dc2626")],
                            land=[(180, 40, 300, 120, -5), (620, 30, 240, 100, 6)],
                            scale="Leaflet | 点击地图选择观测地点 | 20 km")
                   + '<div class="mini" style="margin-top:7px">已选定观测点：'
                     '<b class="mono">110.42°E, 21.18°N</b>（点击地图可重新选点）</div></div>')
            + '<div style="height:13px"></div>'
            + card("", form_title("2", "环境参数") + '<div class="grid3">'
                   + field("水温 (℃)", "26.4", req=True)
                   + field("盐度 (‰)", "30.2", req=True)
                   + field("pH 值", "8.12")
                   + field("溶解氧 (mg/L)", "7.35")
                   + field("水深 (m)", "6.8", req=True)
                   + field("透明度 (m)", "1.9")
                   + field("流速 (m/s)", "0.35")
                   + field("底质类型", "泥沙质", "sel")
                   + field("潮汐状态", "涨潮", "sel") + '</div>'
                   + '<div style="margin-top:13px">' + note(
                       "环境参数将用于模块五「观测记录智能标签与异常检测」。例如盐度显著高于该生态系统常年均值时，"
                       "系统将自动生成「高盐度环境」标签，并结合物种分布判断是否存在异常。", blue=True) + '</div>')
            + '<div style="height:15px"></div><div style="display:flex;gap:9px">'
            + btn("上一步") + btn("保存草稿") + btn("下一步：关联物种", "pri") + btn("取消") + '</div>')
    return ("MB-OBS-2", "新建观测记录（环境参数）", shell("obs", "观测记录管理 / 新建观测记录",
            "新建观测记录", "MB-OBS-2", sub="第 2 步 / 共 4 步", body=body))


def _obs3():
    """MB-OBS-3 观测-物种关联（核心交互）。"""
    cands = [
        ("🐬", "中华白海豚", "Sousa chinensis", '<span class="tag warn">易危</span>', "哺乳纲 / 鲸偶蹄目"),
        ("🐢", "绿海龟", "Chelonia mydas", '<span class="tag err">濒危</span>', "爬行纲 / 龟鳖目"),
        ("🐠", "大黄鱼", "Larimichthys crocea", '<span class="tag err">极危</span>', "硬骨鱼纲 / 鲈形目"),
        ("🐟", "鲻鱼", "Mugil cephalus", '<span class="tag ok">无危</span>', "硬骨鱼纲 / 鲻形目"),
    ]
    cl = "".join(
        f'<div class="cand"><div class="thumb">{ic}</div>'
        f'<div><div style="font-weight:600">{nm}</div>'
        f'<div class="mini"><i>{sn}</i> · {tax}</div></div>'
        f'<div style="margin-left:auto;display:flex;align-items:center;gap:9px">{tg}'
        f'<span class="btn sm">＋ 关联</span></div></div>'
        for ic, nm, sn, tg, tax in cands)

    linked = [
        ["🐬", "<b>中华白海豚</b><div class='mini'><i>Sousa chinensis</i></div>",
         "6", "游弋、跃出水面", "成体 4 头，幼体 2 头，判定为同一群体", "张海宁", '<span class="lk">编辑</span>'],
        ["🐢", "<b>绿海龟</b><div class='mini'><i>Chelonia mydas</i></div>",
         "1", "浮出水面换气", "背甲长约 80 cm，未采集样本", "王庆林", '<span class="lk">编辑</span>'],
        ["🐟", "<b>鲻鱼</b><div class='mini'><i>Mugil cephalus</i></div>",
         "约 200", "集群游动", "估算生物量约 15 kg，为白海豚潜在摄食对象", "李雨欣", '<span class="lk">编辑</span>'],
    ]

    body = (steps(["基本信息", "环境参数", "关联物种", "确认提交"], 3)
            + note("本步骤是模块三的核心交互点：一次观测可关联 <b>一个或多个</b> 物种，并逐个记录估算数量、"
                   "行为描述等详细信息。关联的物种来自模块二「物种信息管理」，若目标物种尚未收录，"
                   "可点击「新增物种」即时录入后在本次观测中引用。", title="操作说明", blue=True)
            + '<div style="height:13px"></div>'
            + '<div class="cols">'
            + '<div style="width:398px;flex:0 0 398px">'
            + card("① 选择物种（来自模块二）", '<div class="fld" style="margin-bottom:12px">'
                   + '<div class="ipt" style="width:100%">🐬 请输入中文名或学名检索…</div></div>'
                   + '<div class="mini" style="margin-bottom:9px">检索到 <b>4</b> 个匹配物种（按名称相关度排序）</div>'
                   + cl
                   + '<div style="margin-top:11px;display:flex;gap:9px">' + btn("＋ 新增物种（本次观测专用）", "pri")
                   + btn("按分类阶元浏览") + '</div>', tag="可多选")
            + '</div>'
            + '<div style="flex:1">'
            + card("② 本次观测已关联的物种", table(
                ["图", "物种", "估算数量", "行为 / 状态", "详细备注", "记录人", "操作"], linked)
                + '<div style="padding:0 16px 4px"><span class="mini">共关联 <b>3</b> 个物种；'
                  '估算数量为原始记录值，不参与后续统计的加权计算。</span></div>', tag="3 条")
            + '<div style="height:13px"></div>'
            + card("③ 本次观测总体备注", field(
                "备注", "本次观测共发现 3 个物种。中华白海豚群体在航道外侧缓慢游弋约 25 分钟，"
                        "未观察到捕食行为；绿海龟仅短暂浮出水面一次。海面有零星渔船作业。",
                "area", span=True))
            + '</div></div>'
            + '<div style="height:15px"></div><div style="display:flex;gap:9px">'
            + btn("上一步") + btn("保存草稿") + btn("下一步：确认提交", "pri") + btn("取消") + '</div>')
    return ("MB-OBS-3", "观测记录关联物种", shell("obs", "观测记录管理 / 新建观测记录",
            "观测记录 — 关联多个物种", "MB-OBS-3", sub="第 3 步 / 共 4 步", body=body))


def _obs4():
    """MB-OBS-4 观测记录详情。"""
    linked = [
        ["🐬", '<span class="lk">中华白海豚</span><div class="mini"><i>Sousa chinensis</i></div>',
         '<span class="tag warn">易危</span>', "6", "游弋、跃出水面",
         "成体 4 头，幼体 2 头，判定为同一群体"],
        ["🐢", '<span class="lk">绿海龟</span><div class="mini"><i>Chelonia mydas</i></div>',
         '<span class="tag err">濒危</span>', "1", "浮出水面换气", "背甲长约 80 cm，未采集样本"],
        ["🐟", '<span class="lk">鲻鱼</span><div class="mini"><i>Mugil cephalus</i></div>',
         '<span class="tag ok">无危</span>', "约 200", "集群游动", "估算生物量约 15 kg"],
    ]
    body = ('<div class="cols"><div style="flex:1">'
            + card("", '<div style="display:flex;align-items:baseline;gap:12px">'
                   + '<span style="font-size:20px;font-weight:700">观测记录 OBS-2026-0142</span>'
                   + '<span class="tag ok">已提交</span>'
                   + '<span class="mini" style="margin-left:auto">记录人 张海宁 · 提交于 2026-10-08 11:05</span></div>'
                   + '<div class="hr"></div>' + dl_list([
                       ("观测时间", "2026-10-08 09:20（野外调查）"),
                       ("观测地点", "湛江港航道外侧约 2.5 km　<span class='mono'>110.42°E, 21.18°N</span>　GPS 实测"),
                       ("所属生态系统", '<span class="tag">河口 / 浅海</span> 雷州湾河口浅海生态系统'),
                       ("观测人员", "张海宁、王庆林、李雨欣"),
                       ("天气 / 海况", "晴，风力 3 级，浪高 0.4 m"),
                       ("统一社会信用代码", "—"),
                   ], "132px 1fr"))
            + card("环境参数", '<div class="grid3" style="gap:11px 16px">'
                   + kv([("水温", "26.4 ℃"), ("盐度", "30.2 ‰"), ("pH", "8.12")])
                   + kv([("溶解氧", "7.35 mg/L"), ("水深", "6.8 m"), ("透明度", "1.9 m")])
                   + kv([("流速", "0.35 m/s"), ("底质类型", "泥沙质"), ("潮汐状态", "涨潮")])
                   + '</div>')
            + card("关联物种（3 个）", table(
                ["图", "物种", "保护等级", "估算数量", "行为 / 状态", "详细备注"], linked)
                + '<div style="padding:0 16px 4px"><span class="mini">'
                  '关联数据由模块三在观测记录创建时录入，并同步供模块四统计分析使用。</span></div>', pad=False)
            + card("观测备注", '<div style="font-size:12.5px;line-height:1.9;color:var(--ink-2)">'
                   '本次观测共发现 3 个物种。中华白海豚群体在航道外侧缓慢游弋约 25 分钟，未观察到捕食行为；'
                   '绿海龟仅短暂浮出水面一次。海面有零星渔船作业。<br>'
                   '现场照片 12 张，水下摄像 1 段（时长 3 分 12 秒）。</div>')
            + '</div><div style="width:360px;flex:0 0 360px">'
            + card("观测地点", mapbox(328, 220, pins=[(164, 108, "#dc2626")],
                   land=[(40, 40, 130, 90, -5), (200, 30, 110, 80, 6)],
                   scale="示意 · 观测点定位"))
            + card("观测时间轴", timeline([
                ("创建观测记录（草稿）", "2026-10-08 09:26", True),
                ("填写环境参数", "2026-10-08 09:41", True),
                ("关联物种 3 个", "2026-10-08 10:12", True),
                ("提交记录", "2026-10-08 11:05", True),
                ("（可选）管理员复核", "待触发", False),
            ]))
            + card("后续操作", '<div style="display:flex;flex-direction:column;gap:9px">'
                   + btn("编辑该观测记录") + btn("复制为新观测记录")
                   + btn("在模块四中查看该点统计") + '</div>')
            + '</div></div>')
    return ("MB-OBS-4", "观测记录详情", shell("obs", "观测记录管理 / 观测记录详情",
            "观测记录详情 — OBS-2026-0142", "MB-OBS-4",
            actions=btn("编辑", "pri") + btn("删除", "dg") + btn("导出记录单"), body=body))


def _obs5():
    """MB-OBS-5 观测记录编辑 / 删除。"""
    rows = [
        [ck(), '<span class="lk">OBS-2026-0142</span>', "2026-10-08 09:20",
         "湛江港航道外侧<br><span class='mono'>110.42°E, 21.18°N</span>",
         '<span class="tag">河口 / 浅海</span>', "张海宁", "26.4 ℃ / 30.2 ‰",
         '<span class="tag pri">1</span>', '<span class="lk">详情</span>'],
        [ck(), '<span class="lk">OBS-2026-0141</span>', "2026-10-06 15:40",
         "徐闻珊瑚礁保护区南片<br><span class='mono'>110.22°E, 20.23°N</span>",
         '<span class="tag pri">珊瑚礁</span>', "王庆林", "27.1 ℃ / 33.8 ‰",
         '<span class="tag pri">6</span>', '<span class="lk p">操作中…</span>'],
    ]
    dlg = dialog("编辑观测记录 — OBS-2026-0142", tabs(["基本信息", "环境参数", "关联物种"])
                 + '<div class="grid2">'
                 + field("观测时间", "2026-10-08 09:20", "date", req=True)
                 + field("所属生态系统", "雷州湾河口浅海生态系统", "sel", req=True)
                 + field("观测人员", "张海宁、王庆林、李雨欣", req=True)
                 + field("天气 / 海况", "晴，风力 3 级，浪高 0.4 m", "sel")
                 + field("地点描述", "湛江港航道外侧约 2.5 km 处", span=True)
                 + field("经度", "110.42") + field("纬度", "21.18")
                 + field("水温 (℃)", "26.4") + field("盐度 (‰)", "30.2")
                 + field("观测备注", "本次观测共发现 3 个物种。中华白海豚群体在航道外侧缓慢游弋约 25 分钟。",
                         "area", span=True)
                 + '</div>'
                 + '<div style="margin-top:13px">' + note(
                     "修改观测记录会同步更新模块四中该观测点的统计结果。若已关联物种，"
                     "可切换到「关联物种」标签页增删关联。", blue=True) + '</div>',
                 footer=btn("取消") + btn("保存修改", "pri"), wide=True)
    body = card("", table(
        ["<span class='ck'></span>", "观测编号", "观测时间", "地点（经纬度）", "生态系统",
         "观测人员", "水温 / 盐度", "关联物种", "状态"], rows) + dlg, pad=False)
    return ("MB-OBS-5", "编辑观测记录", shell("obs", "观测记录管理 / 观测记录列表",
            "观测记录列表", "MB-OBS-5", actions=btn("新建观测记录", "pri"), body=body))


def pages():
    return [_eco1(), _eco2(), _obs1(), _obs2(), _obs3(), _obs4(), _obs5()]
