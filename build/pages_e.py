# -*- coding: utf-8 -*-
"""模块五：智能服务 —— 原型页面定义（MB-AI-*）。"""

from wire_kit import *  # noqa: F401,F403


def _p1():
    """MB-AI-1 图像智能识别（上传）。"""
    rows = [
        ["AI20261008-11", '<div class="thumb">🐢</div>', "绿海龟", "Chelonia mydas",
         '<span class="tag ok">92.6%</span>', '<span class="tag ok">已采纳</span>', "李雨欣", "2026-10-08 09:14"],
        ["AI20261007-09", '<div class="thumb">🪸</div>', "鹿角珊瑚", "Acropora cervicornis",
         '<span class="tag warn">71.3%</span>', '<span class="tag warn">待人工确认</span>', "王庆林", "2026-10-07 15:02"],
        ["AI20261006-04", '<div class="thumb">🐠</div>', "大黄鱼", "Larimichthys crocea",
         '<span class="tag ok">88.1%</span>', '<span class="tag ok">已采纳</span>', "张海宁", "2026-10-06 10:38"],
    ]
    body = ('<div class="cols"><div style="width:700px;flex:0 0 700px">'
            + card("上传待识别图片", dropzone(
                "点击选择图片，或将图片拖拽到此处",
                "支持 JPG / PNG / HEIC，单张 ≤ 10 MB，单次最多 5 张")
                + thumbs(["🐢", "📷", "📷"])
                + '<div style="margin-top:14px;display:flex;gap:9px">' + btn("＋ 继续添加图片")
                + btn("清空") + '</div>', tag="已选 3 张")
            + '<div style="height:13px"></div>'
            + card("识别设置", '<div class="grid2">'
                   + field("识别模式", "多模态大模型识别（图像 → 物种）", "sel")
                   + field("置信度阈值", "≥ 70% 自动推荐；低于阈值转人工确认", "sel")
                   + field("返回候选数量", "Top 3", "sel")
                   + field("是否关联已有物种", "是（匹配模块二物种库）", "sel")
                   + field("拍摄地点", "湛江徐闻珊瑚礁保护区南片", span=True)
                   + field("拍摄时间", "2026-10-06 15:40", "date", span=True)
                   + '</div>'
                   + '<div style="margin-top:14px;display:flex;gap:9px;align-items:center">'
                   + btn("开始智能识别", "pri", sm=False)
                   + '<span class="mini">预计耗时 3–5 s · 识别结果需人工确认后方可写入物种库</span></div>')
            + '</div><div style="flex:1">'
            + card("功能说明", note("本功能调用大模型多模态接口，对上传的海洋生物图片进行物种识别，"
                                   "返回最可能的物种名称与置信度，并自动推荐模块二物种库中已有的关联物种记录。<br>"
                                   "若置信度低于设定阈值，系统将提供候选列表供用户选择，或发起人工确认流程。", blue=True)
                   + '<div style="height:11px"></div>'
                   + note("上传图片将进行敏感信息过滤（去除 EXIF 中的位置与设备信息）；"
                          "调用大模型接口的 API Key 保存在服务端本地配置，不暴露于前端。",
                          title="安全与合规"))
            + '<div style="height:13px"></div>'
            + card("识别小贴士", '<div class="tl">'
                   + '<div class="it"><span class="d"></span><div class="c">'
                     '主体清晰、单一物种占据画面主要区域时识别准确率最高<div class="tm">建议拍摄距离 0.5–2 m</div></div></div>'
                   + '<div class="it"><span class="d"></span><div class="c">'
                     '避免强反光、浑浊水体与大角度俯拍<div class="tm">水下拍摄建议使用补光灯</div></div></div>'
                   + '<div class="it"><span class="d g"></span><div class="c">'
                     '难以确定的样本可采用「候选列表 + 人工确认」流程<div class="tm">确认结果将作为模型反馈样本</div></div></div>'
                   + '</div>')
            + '</div></div>'
            + '<div style="height:13px"></div>'
            + card("历史识别记录", table(
                ["识别编号", "图片", "识别物种", "学名", "置信度", "处理状态", "提交人", "识别时间"], rows),
                pad=False))
    return ("MB-AI-1", "图像智能识别", shell("ai", "智能服务 / 图像智能识别",
            "图像智能识别与物种鉴定", "MB-AI-1",
            actions=btn("识别结果管理") + btn("进入智能问答"), body=body))


def _p2():
    """MB-AI-2 识别结果与物种鉴定。"""
    cands = [("1", "中华白海豚", "Sousa chinensis", "94.2%"),
             ("2", "太平洋驼海豚", "Sousa plumbea", "63.8%"),
             ("3", "宽吻海豚", "Tursiops truncatus", "41.5%")]
    cl = "".join(
        f'<div class="cand"><span class="rk">{r}</span>'
        f'<div><div style="font-weight:600">{nm}</div>'
        f'<div class="mini"><i>{sn}</i> · 模块二已有记录</div></div>'
        f'<span class="pc">{p}</span><span class="btn sm">选择</span></div>'
        for r, nm, sn, p in cands)

    body = ('<div class="cols"><div style="flex:1">'
            + card("识别结果", '<div class="ai">'
                   '<div class="pic">🐬</div><div class="res">'
                   '<div class="top"><span class="nm">中华白海豚</span>'
                   '<span class="sn">Sousa chinensis (Osbeck, 1765)</span>'
                   '<span class="tag ok" style="margin-left:auto">高置信度</span></div>'
                   '<div class="conf"><div class="lb"><span>识别置信度</span><b>94.2%</b></div>'
                   '<div class="bar"><i style="width:94.2%"></i></div></div>'
                   '<div class="mini">大模型多模态识别 · 耗时 3.6 s · 模型：视觉语言大模型（服务端调用）</div>'
                   + kv([("门", "脊索动物门 Chordata"), ("纲", "哺乳纲 Mammalia"),
                         ("目", "鲸偶蹄目 Cetartiodactyla"), ("科", "海豚科 Delphinidae"),
                         ("保护等级", '<span class="tag err">国家一级保护动物</span>'),
                         ("IUCN 等级", '<span class="tag warn">易危 VU</span>')])
                   + '</div></div>'
                   + '<div class="hr"></div>'
                   + '<div class="mini" style="line-height:1.9">'
                     '识别依据：体形呈纺锤形、吻突较长而尖、背鳍三角形位于体中部略后、'
                     '成体体色粉白，与中华白海豚形态特征高度一致。</div>')
            + '<div style="height:13px"></div>'
            + card("候选物种列表", cl + '<div class="mini" style="margin-top:6px">'
                   '置信度低于 70% 的候选将以「待人工确认」处理，可由用户选择或发起人工复核。</div>',
                   tag="Top 3")
            + '</div><div style="width:420px;flex:0 0 420px">'
            + card("关联已有物种记录（模块二）", note(
                "识别结果已自动匹配到模块二中的物种记录：<br>"
                "<b>中华白海豚 SPEC-2026-0187</b>（匹配度 100%）", title="推荐关联", blue=True)
                + '<div style="height:12px"></div>'
                + dl_list([("物种编号", "SPEC-2026-0187"), ("收录人", "张海宁"),
                           ("收录时间", "2026-08-28"), ("关联观测记录", "8 条")], "108px 1fr")
                + '<div style="margin-top:13px;display:flex;flex-direction:column;gap:9px">'
                + btn("采纳并关联到该物种", "pri")
                + btn("采纳并新建物种记录（模块二）")
                + btn("发起人工确认流程") + '</div>')
            + card("写入物种库预览", '<div class="mini" style="margin-bottom:9px">采纳后将在模块二中：</div>'
                   '<div class="tl">'
                   '<div class="it"><span class="d"></span><div class="c">'
                   '为该物种新增 1 张图片资料<div class="tm">标注来源：AI 识别 · 2026-10-06</div></div></div>'
                   '<div class="it"><span class="d"></span><div class="c">'
                   '在本条物种记录中追加 1 个分布点<div class="tm">110.22°E, 20.23°N（徐闻珊瑚礁南片）</div></div></div>'
                   '<div class="it"><span class="d g"></span><div class="c">'
                   '记录识别日志（识别时间、置信度、操作人）<div class="tm">用于模型质量追溯与分析</div></div></div>'
                   '</div>')
            + card("本次识别信息", dl_list([("识别编号", "AI20261008-12"), ("提交人", "王庆林"),
                                          ("识别时间", "2026-10-08 15:42"), ("图片来源", "野外拍摄"),
                                          ("处理状态", '<span class="tag warn">待确认</span>')], "108px 1fr"))
            + '</div></div>')
    return ("MB-AI-2", "识别结果与物种鉴定", shell("ai", "智能服务 / 图像智能识别 / 识别结果",
            "识别结果与物种鉴定", "MB-AI-2",
            actions=btn("重新识别") + btn("采纳并保存", "pri"), body=body))


def _p3():
    """MB-AI-3 文本辅助分类与补全。"""
    body = ('<div class="cols"><div style="flex:1">'
            + card("输入与补全", form_title("1", "输入物种名称")
                   + '<div class="grid2">' + field("中文名", "中华白海豚", req=True)
                   + field("学名（可留空）", "Sousa chinensis", hint="留空时由大模型依据中文名推断")
                   + '</div>'
                   + '<div style="margin-top:14px;display:flex;gap:9px;align-items:center">'
                   + btn("🤖 调用大模型自动补全", "pri", sm=False)
                   + '<span class="mini">约 2–4 s · 模型基于物种知识自动填充分类阶元与描述字段</span></div>'
                   + '<div class="hr"></div>'
                   + form_title("2", "补全结果（需人工确认后方可写入）")
                   + '<div class="grid3">'
                   + field("门", "脊索动物门 Chordata", hint="✓ 已自动填充")
                   + field("纲", "哺乳纲 Mammalia", hint="✓ 已自动填充")
                   + field("目", "鲸偶蹄目 Cetartiodactyla", hint="✓ 已自动填充")
                   + field("科", "海豚科 Delphinidae", hint="✓ 已自动填充")
                   + field("属", "驼海豚属 Sousa", hint="✓ 已自动填充")
                   + field("种", "中华白海豚 S. chinensis", hint="✓ 已自动填充")
                   + field("保护等级", "国家一级保护动物", hint="⚠ 请人工核实")
                   + field("IUCN 濒危等级", "易危 VU", hint="⚠ 请人工核实")
                   + field("CITES 附录", "附录 I", hint="⚠ 请人工核实")
                   + '</div>'
                   + '<div style="margin-top:14px">'
                   + field("形态特征（AI 生成初稿）",
                           "体呈纺锤形，成体体长 2.0–2.5 m。吻突较长而尖，背鳍位于体中部略后，呈三角形。"
                           "幼体体色灰黑，随年龄增长逐渐变浅，成体多为粉白色。", "area", span=True)
                   + field("生活习性（AI 生成初稿）",
                           "近岸性，多活动于河口、港湾及浅海水域，水深一般小于 20 m。以鲻鱼、黄姑鱼、"
                           "虾类等为食。群体活动，常见 3–10 头小群。", "area", span=True)
                   + '</div>'
                   + '<div style="margin-top:14px;display:flex;gap:9px">'
                   + btn("全部采纳", "pri") + btn("逐条采纳") + btn("重新生成") + btn("清空补全结果") + '</div>')
            + '</div><div style="width:400px;flex:0 0 400px">'
            + card("智能润色", '<div class="mini" style="margin-bottom:9px">对已有物种描述进行润色，提升数据规范性</div>'
                   + '<div style="border:1px solid var(--line);border-radius:6px;padding:11px;font-size:12px;line-height:1.8;color:var(--ink-2)">'
                   + '<div class="mini" style="margin-bottom:5px">原文</div>'
                   + '海豚身体是纺锤形的，嘴巴比较长比较尖，背上的鳍在身体中间靠后面一点的地方，'
                   + '小时候是灰黑色的，长大了就变成粉白色。</div>'
                   + '<div style="text-align:center;margin:9px 0;color:var(--primary)">↓ 🤖 智能润色</div>'
                   + '<div style="border:1px solid #bae6fd;background:var(--primary-ll);border-radius:6px;padding:11px;font-size:12px;line-height:1.8">'
                   + '<div class="mini" style="margin-bottom:5px">润色后</div>'
                   + '体呈纺锤形，吻突较长而尖，背鳍位于体中部略后。幼体体色灰黑，随年龄增长逐渐变浅，'
                   + '成体多为粉白色。</div>'
                   + '<div style="margin-top:11px;display:flex;gap:8px">' + btn("采纳润色结果", "pri") + btn("再生成") + '</div>')
            + card("功能说明", note("本功能在录入物种信息（模块二）时提供辅助：输入中文名或学名后，"
                                   "系统调用大模型自动补全分类信息（门纲目科属种）、形态特征、生活习性等字段，"
                                   "并对已有描述进行智能润色或生成摘要。<br>"
                                   "所有 AI 生成内容均以「初稿」标记，须人工确认后方可写入数据库，"
                                   "以确保科研数据的准确性。", blue=True))
            + '</div></div>')
    return ("MB-AI-3", "文本辅助分类与补全", shell("ai", "智能服务 / 文本辅助分类与补全",
            "文本辅助分类与补全", "MB-AI-3",
            actions=btn("查看调用日志") + btn("保存并写入物种库", "pri"), body=body))


def _p4():
    """MB-AI-4 智能问答与科研助手。"""
    body = ('<div class="cols"><div style="flex:1">'
            + card("", '<div class="chatwrap"><div class="chat">'
                   '<div class="msg u"><div class="av">张</div><div class="bub">'
                   '最近三年在湛江附近观测到的濒危物种有哪些？</div></div>'
                   '<div class="msg a"><div class="av">🤖</div><div class="bub">'
                   '根据模块二（物种信息）与模块三（观测记录）的数据，2023-10 至 2026-10 期间'
                   '<b>湛江近海</b>（经度 109.5°–110.8°E，纬度 20.1°–21.5°N）共记录到 '
                   '<b>4 个濒危物种</b>：'
                   '<ul>'
                   '<li><b>中华白海豚</b>（易危 VU）— 8 次观测，最近 2026-10-08 湛江港航道外侧，估算 6 头</li>'
                   '<li><b>绿海龟</b>（濒危 EN）— 2 次观测，最近 2026-10-06 徐闻珊瑚礁保护区南片</li>'
                   '<li><b>鹿角珊瑚</b>（极危 CR）— 34 次观测，主要分布于徐闻珊瑚礁自然保护区</li>'
                   '<li><b>大黄鱼</b>（极危 CR）— 5 次观测，最近 2026-10-07 雷州湾东部浅水区</li>'
                   '</ul>'
                   '其中<b>鹿角珊瑚</b>观测频次最高，但 2025 年以来单位面积覆盖率呈下降趋势，建议重点关注。'
                   '<div class="src">🔗 数据来源：模块二 SPEC-2026-0187 等 4 条物种记录 · '
                   '模块三 OBS-2026-0142 等 49 条观测记录<br>'
                   '🤖 查询已转换为结构化条件：'
                   '<span class="mono">protection_level IN (CR, EN, VU) AND '
                   'lat BETWEEN 20.1 AND 21.5 AND lon BETWEEN 109.5 AND 110.8 AND '
                   'obs_time BETWEEN 2023-10 AND 2026-10</span></div>'
                   '</div></div>'
                   '<div class="msg u"><div class="av">张</div><div class="bub">'
                   '请总结红树林生态系统中物种数量的变化趋势</div></div>'
                   '<div class="msg a"><div class="av">🤖</div><div class="bub">'
                   '正在检索模块三中「湛江红树林生态系统」的观测数据…'
                   '<div class="src">🤖 已定位 61 条观测记录，正在生成趋势总结</div></div></div>'
                   '</div>'
                   + '<div class="quicks">'
                   + "".join(f'<span class="tag pri" style="height:26px;padding:0 12px">{q}</span>' for q in
                             ["近三年观测次数最多的物种是？", "徐闻珊瑚礁的珊瑚白化记录",
                              "对比红树林与海草床的物种丰富度", "哪些物种只在深海生态系统中出现？"])
                   + '</div>'
                   + '<div class="composer"><div class="in">请输入问题，例如：最近三年在湛江附近观测到的濒危物种有哪些？</div>'
                   + btn("发送", "pri", sm=False) + '</div></div>', pad=False)
            + '</div><div style="width:378px;flex:0 0 378px">'
            + card("检索范围", '<div class="chips" style="margin-bottom:12px">'
                   + "".join(f'<span class="tag pri">{t}</span>' for t in
                             ["模块二 物种信息", "模块三 观测记录", "模块三 生态系统"])
                   + '</div>'
                   + field("时间范围", "近三年（2023-10 ~ 2026-10）", "date", span=True)
                   + field("空间范围", "湛江近海（109.5–110.8°E, 20.1–21.5°N）", span=True))
            + card("本次会话引用", dl_list([("物种记录", "4 条"), ("观测记录", "49 条"),
                                          ("生态系统", "3 个"), ("数据截止", "2026-10-08")], "96px 1fr")
                   + '<div style="margin-top:12px;display:flex;flex-direction:column;gap:8px">'
                   + btn("导出本次问答记录") + btn("生成分析报告（PDF）") + '</div>')
            + card("能力说明", note("支持自然语言提问；系统将问题转换为结构化查询，从模块二、模块三检索数据，"
                                   "并结合大模型生成回答，同时给出数据来源与查询条件，便于科研人员复核。<br>"
                                   "首字响应时间不超过 3 s；大模型服务调用具备超时与重试机制。", blue=True))
            + '</div></div>')
    return ("MB-AI-4", "智能问答与科研助手", shell("ai", "智能服务 / 智能问答与科研助手",
            "智能问答与科研助手", "MB-AI-4",
            actions=btn("清空会话") + btn("导出问答记录"), body=body))


def _p5():
    """MB-AI-5 物种描述多语言支持。"""
    body = ('<div class="cols"><div style="flex:1">'
            + card("翻译配置", '<div class="grid3">'
                   + field("物种", "中华白海豚（SPEC-2026-0187）", "sel", req=True)
                   + field("源语言", "中文", "sel")
                   + field("目标语言", "English", "sel", req=True)
                   + field("翻译范围", "形态特征 + 生活习性 + 保护信息", "sel")
                   + field("输出用途", "国际交流 / 科普展示", "sel")
                   + field("是否保留学名", "是（学名保持拉丁文斜体）", "sel")
                   + '</div>'
                   + '<div style="margin-top:14px;display:flex;gap:9px">'
                   + btn("🤖 生成译文", "pri") + btn("批量翻译多个物种") + btn("导入术语表") + '</div>')
            + '<div style="height:13px"></div>'
            + card("对照编辑", tabs(["形态特征", "生活习性", "保护信息"])
                   + '<div class="cols">'
                   + '<div style="flex:1"><div class="mini" style="margin-bottom:7px">中文原文（来自模块二）</div>'
                   + '<div style="border:1px solid var(--line);border-radius:6px;padding:13px;'
                     'font-size:12.5px;line-height:1.95;color:var(--ink-2);min-height:172px">'
                   + '<b style="color:var(--ink)">形态特征：</b>体呈纺锤形，成体体长 2.0–2.5 m，体重 150–230 kg。'
                     '吻突较长而尖，背鳍位于体中部略后，呈三角形。幼体体色灰黑，随年龄增长逐渐变浅，'
                     '成体多为粉白色，故称「中华白海豚」。'
                   + '<div class="hint" style="margin-top:9px">112 字 · 未修改</div></div></div>'
                   + '<div style="flex:1"><div class="mini" style="margin-bottom:7px">'
                     'English（AI 生成，可编辑）</div>'
                   + '<div style="border:1px solid #7dd3e0;background:var(--primary-ll);border-radius:6px;'
                     'padding:13px;font-size:12.5px;line-height:1.95;min-height:172px">'
                   + '<b>Morphology:</b> Body fusiform, adult body length 2.0–2.5 m, weight 150–230 kg. '
                     'Rostrum relatively long and pointed; dorsal fin triangular, positioned slightly '
                     'posterior to the mid-body. Calves are greyish-black and gradually lighten with age; '
                     'adults are mostly pinkish-white, hence the Chinese name meaning '
                     '&#8220;Chinese white dolphin&#8221;. '
                     '<i>Sousa chinensis</i>'
                   + '<div class="hint" style="margin-top:9px">已生成 · 术语表校验通过（学名、单位保留）</div></div></div>'
                   + '</div>'
                   + '<div style="margin-top:14px;display:flex;gap:9px">'
                   + btn("保存译文", "pri") + btn("重新生成") + btn("回写至模块二物种记录") + btn("导出双语对照表") + '</div>')
            + '</div><div style="width:396px;flex:0 0 396px">'
            + card("翻译状态总览", '<div class="mini" style="margin-bottom:11px">'
                   '模块二物种记录的多语言覆盖情况</div>'
                   + bars([("中文（原文）", "1,286", 100), ("English", "412", 32),
                           ("日本語", "86", 7), ("한국어", "54", 4)])
                   + '<div class="hr"></div>'
                   + dl_list([("本次翻译字数", "约 1,240 字"), ("术语表命中", "18 / 21 条"),
                              ("生成耗时", "4.2 s"), ("保存状态", '<span class="tag warn">未保存</span>')], "108px 1fr"))
            + card("已翻译物种", table(
                ["物种", "语言", "状态"],
                [['<span class="lk">中华白海豚</span>', "English", '<span class="tag warn">编辑中</span>'],
                 ['<span class="lk">绿海龟</span>', "English", '<span class="tag ok">已发布</span>'],
                 ['<span class="lk">鹿角珊瑚</span>', "English / 日本語", '<span class="tag ok">已发布</span>'],
                 ['<span class="lk">大黄鱼</span>', "English", '<span class="tag ok">已发布</span>']]))
            + card("能力说明", note("调用大模型将物种描述自动翻译为英文或其它语言，便于国际交流与科普展示。<br>"
                                   "翻译时自动保护学名、计量单位与专业术语，避免误译；"
                                   "译文经人工确认后方可发布到公众可见的页面。", blue=True))
            + '</div></div>')
    return ("MB-AI-5", "物种描述多语言支持", shell("ai", "智能服务 / 多语言支持",
            "物种描述多语言支持", "MB-AI-5",
            actions=btn("术语表管理") + btn("保存译文", "pri"), body=body))


def _p6():
    """MB-AI-6 观测记录智能标签与异常检测。"""
    body = ('<div class="cols"><div style="flex:1">'
            + card("观测记录 OBS-2026-0142", dl_list([
                ("观测时间", "2026-10-08 09:20（野外调查）"),
                ("观测地点", "湛江港航道外侧　<span class='mono'>110.42°E, 21.18°N</span>"),
                ("所属生态系统", '<span class="tag">河口 / 浅海</span> 雷州湾河口浅海生态系统'),
                ("观测人员", "张海宁、王庆林、李雨欣"),
                ("水温 / 盐度", "26.4 ℃ / 30.2 ‰　　pH 8.12　溶解氧 7.35 mg/L　水深 6.8 m"),
            ], "126px 1fr"))
            + '<div style="height:13px"></div>'
            + card("🤖 自动标签（大模型生成）", '<div class="mini" style="margin-bottom:11px">'
                   '系统依据地点、时间、生态系统与环境参数字段自动生成，可直接采用或删除</div>'
                   + '<div class="chips">'
                   + "".join(f'<span class="tag pri" style="height:28px;padding:0 13px">{t} ✕</span>' for t in
                             ["繁殖期发现", "高盐度环境", "近岸浅水", "河口咸淡水交汇区", "春夏季观测"])
                   + '</div>'
                   + '<div style="margin-top:14px;display:flex;gap:9px">'
                   + btn("全部采用", "pri") + btn("＋ 手动添加标签") + btn("重新生成标签") + '</div>'
                   + '<div class="hr"></div>'
                   + '<div class="mini" style="line-height:1.9">生成依据：<br>'
                     '· 观测时间 2026-10-08 落在该物种记录的繁殖高峰（3–6 月）之外，'
                     '但盐度 30.2 ‰ 高于该生态系统常年均值（26.8 ‰），故生成「高盐度环境」标签。</div>')
            + '<div style="height:13px"></div>'
            + card("⚠ 异常检测", note(
                "检测到 <b>1</b> 条可能的分布冲突：<br>"
                "关联物种 <b>绿海龟（Chelonia mydas）</b> 的主要分布记录集中在<b>热带 / 亚热带</b>海域"
                "（历史观测点平均纬度 18.2°N），而本次观测点位于 <b>21.18°N</b>，"
                "超出其历史分布纬度范围约 3°。请核实物种鉴定是否准确。", title="分布冲突提示")
                + '<div style="height:11px"></div>'
                + '<div class="grid2">' + field("处理方式", "标记为待核实（保留记录）", "sel", req=True)
                + field("核实说明", "现场照片已复核，背甲形态与绿海龟一致，可能为偶发北移个体。", "area") + '</div>'
                + '<div style="margin-top:12px;display:flex;gap:9px">'
                + btn("标记为需核实", "pri") + btn("确认为正常记录") + btn("忽略本次提示") + btn("上报管理员") + '</div>',
                tag="1 条")
            + '<div style="height:13px"></div>'
            + card("异常检测规则", table(
                ["规则编号", "规则说明", "触发条件", "处理建议", "状态"],
                [["AI-EX-01", "物种分布纬度冲突", "观测纬度超出物种历史分布纬度 ±2°", "核实鉴定或标记待核实", '<span class="tag ok">已启用</span>'],
                 ["AI-EX-02", "环境参数超出生态系统常年区间", "水温 / 盐度偏离均值 ±30%", "提示用户复核环境数据", '<span class="tag ok">已启用</span>'],
                 ["AI-EX-03", "季节与繁殖期冲突", "记录到繁殖行为但不在该物种繁殖期", "提示人工确认", '<span class="tag ok">已启用</span>'],
                 ["AI-EX-04", "深海物种出现在浅水区", "深海物种出现在水深 < 50 m 的观测点", "核实生态系统归属", '<span class="tag warn">试运行</span>']]),
                pad=False)
            + '</div><div style="width:392px;flex:0 0 392px">'
            + card("本次检测摘要", dl_list([("参与检测规则", "4 条"), ("生成标签", "5 个"),
                                          ("触发异常", "1 条"), ("检测耗时", "2.8 s"),
                                          ("检测时间", "2026-10-08 11:05")], "108px 1fr"))
            + card("物种分布纬度对照", '<div class="chartbox" style="border:none;padding:0">'
                   + '<div class="cs" style="margin-bottom:10px">绿海龟历史观测点纬度分布</div>'
                   + hbar_chart([("15°N", 4, "#0891b2"), ("16°N", 7, "#0891b2"),
                                 ("17°N", 9, "#0891b2"), ("18°N", 11, "#0891b2"),
                                 ("19°N", 6, "#0891b2"), ("20°N", 2, "#d97706"),
                                 ("21°N", 1, "#dc2626")], w=336)
                   + '<div class="mini" style="margin-top:9px;line-height:1.8">'
                     '<span style="color:#dc2626">■</span> 21°N 为本条记录（异常偏高）<br>'
                     '<span style="color:#d97706">■</span> 20°N 为历史最北记录<br>'
                     '历史分布集中于 15°–19°N</div></div>')
            + card("功能说明", note("本功能为选做项。在创建观测记录（模块三）时，系统根据地点、时间、"
                                   "生态系统等字段调用大模型生成自动标签，并检测观测数据与物种分布、"
                                   "环境参数的明显冲突，提示用户核实，从而提升数据质量。", blue=True))
            + '</div></div>')
    return ("MB-AI-6", "观测智能标签与异常检测", shell("ai", "智能服务 / 观测智能标签与异常检测",
            "观测记录智能标签与异常检测", "MB-AI-6",
            actions=btn("检测规则配置") + btn("保存", "pri"), body=body))


def pages():
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6()]
