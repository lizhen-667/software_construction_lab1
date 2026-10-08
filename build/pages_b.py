# -*- coding: utf-8 -*-
"""模块二：物种信息管理 —— 原型页面定义（MB-SPEC-*）。"""

from wire_kit import *  # noqa: F401,F403

PROT = {"极危": "err", "濒危": "err", "易危": "warn", "近危": "info", "无危": "ok", "数据缺乏": ""}


def lvl(name):
    return f'<span class="tag {PROT.get(name, "")}">{name}</span>'


def _p1():
    """MB-SPEC-1 物种信息列表（多条件组合检索）。"""
    rows = [
        [ck(), '<div class="thumb">🐬</div>', '<span class="lk">中华白海豚</span>',
         '<i style="color:var(--ink-3)">Sousa chinensis</i>', "脊索动物门 / 哺乳纲 / 鲸偶蹄目",
         lvl("易危"), "珠江口、湛江港、雷州湾", "2026-10-08 08:55",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<div class="thumb">🐢</div>', '<span class="lk">绿海龟</span>',
         '<i style="color:var(--ink-3)">Chelonia mydas</i>', "脊索动物门 / 爬行纲 / 龟鳖目",
         lvl("濒危"), "西沙群岛、南澎列岛", "2026-10-07 19:22",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<div class="thumb">🐠</div>', '<span class="lk">大黄鱼</span>',
         '<i style="color:var(--ink-3)">Larimichthys crocea</i>', "脊索动物门 / 硬骨鱼纲 / 鲈形目",
         lvl("极危"), "东海、南海北部近海", "2026-10-07 15:38",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<div class="thumb">🪸</div>', '<span class="lk">鹿角珊瑚</span>',
         '<i style="color:var(--ink-3)">Acropora cervicornis</i>', "刺胞动物门 / 珊瑚纲 / 石珊瑚目",
         lvl("极危"), "徐闻珊瑚礁自然保护区", "2026-10-06 11:04",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<div class="thumb">🌿</div>', '<span class="lk">秋茄（红树林）</span>',
         '<i style="color:var(--ink-3)">Kandelia obovata</i>', "被子植物门 / 双子叶植物纲 / 桃金娘目",
         lvl("近危"), "湛江红树林国家级自然保护区", "2026-10-05 09:47",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
        [ck(), '<div class="thumb">🦞</div>', '<span class="lk">锦绣龙虾</span>',
         '<i style="color:var(--ink-3)">Panulirus ornatus</i>', "节肢动物门 / 软甲纲 / 十足目",
         lvl("数据缺乏"), "硇洲岛、涠洲岛周边礁区", "2026-10-04 16:12",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span><span class="lk p">删除</span></span>'],
    ]
    body = (filters(
        [("中文名 / 学名", "text", "请输入物种名称"),
         ("门", "sel", "脊索动物门"),
         ("纲", "sel", "全部"),
         ("保护等级", "sel", "全部"),
         ("濒危状态", "sel", "全部"),
         ("分布区域", "text", "输入地名或经纬度范围")],
        btn("检索", "pri") + btn("重置") + btn("高级检索"))
        + card("", table(
            ["<span class='ck'></span>", "图", "中文名", "学名", "分类阶元（门/纲/目）",
             "保护等级", "分布区域", "更新时间", "操作"], rows)
            + '<div style="padding:0 16px 12px">'
            + btn("新增物种", "pri") + " " + btn("批量删除", "dg") + " " + btn("导出结果")
            + "&nbsp;&nbsp;<span class='mini'>已选中 6 项</span></div>" + pager("共 1,286 条记录"), pad=False))
    return ("MB-SPEC-1", "物种信息列表", shell("spec", "物种信息管理 / 物种信息列表",
            "物种信息列表", "MB-SPEC-1",
            actions=btn("新增物种", "pri") + btn("导入物种数据"), body=body))


def _p2():
    """MB-SPEC-2 新增物种信息（第一步：分类与基本信息）。"""
    body = (steps(["基本信息与分类", "形态习性与分布", "多媒体与参考文献"], 1)
            + card("", form_title("1", "物种标识") + '<div class="grid3">'
                   + field("中文名", "中华白海豚", req=True)
                   + field("学名（拉丁名）", "Sousa chinensis", req=True, hint="属名 + 种加词，斜体")
                   + field("命名人与年份", "Osbeck, 1765")
                   + field("中文别名", "白海豚、太平洋驼海豚", span=True)
                   + field("英文名", "Indo-Pacific Humpback Dolphin")
                   + field("俗名（地方名）", "白忌、海猪")
                   + field("物种编号", "SPEC-2026-0187", hint="系统自动生成，保存后生效")
                   + '</div><div class="hr"></div>' + form_title("2", "分类阶元") + '<div class="grid3">'
                   + field("门", "脊索动物门 Chordata", "sel", req=True)
                   + field("纲", "哺乳纲 Mammalia", "sel", req=True)
                   + field("目", "鲸偶蹄目 Cetartiodactyla", "sel", req=True)
                   + field("科", "海豚科 Delphinidae", "sel", req=True)
                   + field("属", "驼海豚属 Sousa", "sel", req=True)
                   + field("种", "中华白海豚 S. chinensis", "sel", req=True) + '</div>'
                   + '<div style="margin-top:12px">'
                   + note("若对分类阶元不确定，可在「形态习性与分布」一步中使用「AI 智能补全」，"
                          "由系统调用大模型依据中文名 / 学名自动填充分类信息，填充后仍需人工确认。", blue=True)
                   + '</div>')
            + '<div style="height:13px"></div>'
            + card("", form_title("3", "保护与公开属性") + '<div class="grid3">'
                   + field("保护等级", "国家一级保护动物", "sel", req=True)
                   + field("IUCN 濒危等级", "易危 VU", "sel", req=True)
                   + field("CITES 附录", "附录 I", "sel")
                   + field("中国物种红色名录", "易危 VU", "sel")
                   + field("是否对公众公开", "公开（仅基本信息）", "sel",
                           hint="公众可见范围：分类、形态、分布概览")
                   + field("数据来源", "野外调查 / 文献整理", "sel") + '</div>')
            + '<div style="height:15px"></div><div style="display:flex;gap:9px">'
            + btn("保存草稿") + btn("下一步：形态习性与分布", "pri") + btn("取消") + '</div>')
    return ("MB-SPEC-2", "新增物种信息（基本信息）", shell("spec", "物种信息管理 / 新增物种信息",
            "新增物种信息", "MB-SPEC-2", sub="第 1 步 / 共 3 步", body=body))


def _p3():
    """MB-SPEC-3 新增物种信息（第二步：形态、习性、分布、多媒体）。"""
    body = (steps(["基本信息与分类", "形态习性与分布", "多媒体与参考文献"], 2)
            + card("", form_title("4", "形态特征与生活习性")
                   + '<div style="margin-bottom:11px;display:flex;gap:8px;align-items:center">'
                   + btn("🤖 AI 智能补全形态与习性", "pri")
                   + '<span class="mini">依据学名 Sousa chinensis 调用大模型生成初稿，生成结果需人工校对</span></div>'
                   + '<div class="grid2">'
                   + field("形态特征", "体呈纺锤形，成体体长 2.0–2.5 m。吻突较长而尖，背鳍位于体中部略后，"
                           "呈三角形。幼体体色灰黑，随年龄增长逐渐变浅，成体多为粉白色，故称「中华白海豚」。", "area", req=True)
                   + field("生活习性", "近岸性，多活动于河口、港湾及浅海水域，水深一般小于 20 m。以鲻鱼、"
                           "黄姑鱼、虾类等为食。群体活动，常见 3–10 头小群。性成熟约 9–10 龄，妊娠期约 10–11 个月。", "area", req=True)
                   + field("繁殖习性", "繁殖高峰多在春夏季（3–6 月），每胎 1 仔，哺乳期约 1.5 年。", "area")
                   + field("栖息环境", "河口咸淡水交汇区、红树林外缘浅水区、港口航道附近", "area") + '</div>')
            + '<div style="height:13px"></div>'
            + card("", form_title("5", "分布区域") + '<div class="grid3">'
                   + field("分布范围描述", "珠江口、湛江港、雷州湾、北部湾北部", span=True)
                   + field("经度范围", "109.5°E ~ 114.2°E")
                   + field("纬度范围", "20.1°N ~ 23.4°N")
                   + field("中心分布点", "110.41°E, 21.19°N") + '</div>'
                   + '<div style="margin-top:13px">'
                   + mapbox(980, 250, pins=[(180, 130, "#0e7490"), (330, 105, "#0e7490"), (430, 150, "#0891b2"),
                                            (600, 88, "#0891b2"), (760, 120, "#0e7490")],
                            land=[(90, 60, 260, 150, -6), (470, 40, 300, 130, 4), (700, 150, 220, 100, -3)],
                            scale="Leaflet | 点击地图可增删分布点 | 50 km")
                   + '<div class="mini" style="margin-top:7px">共标记 5 个分布点。点击地图可新增分布点，'
                     '拖动标记可调整位置；分布点数据将同步供模块四「物种分布地图」渲染使用。</div></div>')
            + '<div style="height:15px"></div><div style="display:flex;gap:9px">'
            + btn("上一步") + btn("保存草稿") + btn("下一步：多媒体与参考文献", "pri") + btn("取消") + '</div>')
    return ("MB-SPEC-3", "新增物种信息（形态与分布）", shell("spec", "物种信息管理 / 新增物种信息",
            "新增物种信息", "MB-SPEC-3", sub="第 2 步 / 共 3 步", body=body))


def _p4():
    """MB-SPEC-4 物种详情页面。"""
    body = ('<div class="cols"><div style="flex:1">'
            + card("", """
          <div style="display:flex;gap:18px">
            <div style="width:168px;flex:0 0 168px">
              <div style="width:168px;height:132px;border-radius:8px;background:var(--primary-l);
                   border:1px solid #bae6fd;display:flex;align-items:center;justify-content:center;font-size:52px">🐬</div>
              <div style="display:flex;gap:6px;margin-top:7px">
                <div style="width:52px;height:38px;border-radius:5px;background:var(--primary-l);border:1px solid #bae6fd;display:flex;align-items:center;justify-content:center;font-size:19px">🐬</div>
                <div style="width:52px;height:38px;border-radius:5px;background:#f1f5f9;border:1px solid var(--line-2);display:flex;align-items:center;justify-content:center;font-size:19px">📷</div>
                <div style="width:52px;height:38px;border-radius:5px;background:#f1f5f9;border:1px solid var(--line-2);display:flex;align-items:center;justify-content:center;font-size:19px">📷</div>
              </div>
            </div>
            <div style="flex:1">
              <div style="display:flex;align-items:baseline;gap:11px">
                <span style="font-size:22px;font-weight:700">中华白海豚</span>
                <span style="font-size:14px;color:var(--ink-3);font-style:italic">Sousa chinensis (Osbeck, 1765)</span>
              </div>
              <div class="chips" style="margin-top:9px">
    """ + lvl("易危") + ' <span class="tag err">国家一级保护</span>'
            + ' <span class="tag">CITES 附录 I</span> <span class="tag pri">公开</span></div>'
            + kv([("门", "脊索动物门 Chordata"), ("纲", "哺乳纲 Mammalia"),
                  ("目", "鲸偶蹄目 Cetartiodactyla"), ("科", "海豚科 Delphinidae"),
                  ("属", "驼海豚属 Sousa"), ("物种编号", "SPEC-2026-0187"),
                  ("收录人", "张海宁　·　2026-10-08 08:55"), ("数据版本", "v1.3（最近更新 2026-10-08）")])
            + '</div></div>')
            + '<div style="height:13px"></div>'
            + card("", tabs(["形态与习性", "分布与栖息地", "多媒体资料（5）", "参考文献（12）", "关联观测记录（8）"]) + """
          <div style="font-size:12.5px;line-height:1.95;color:var(--ink-2)">
            <p style="margin-bottom:11px"><b style="color:var(--ink)">形态特征：</b>体呈纺锤形，成体体长 2.0–2.5 m，体重 150–230 kg。吻突较长而尖，背鳍位于体中部略后，呈三角形。幼体体色灰黑，随年龄增长逐渐变浅，成体多为粉白色，故称「中华白海豚」。</p>
            <p style="margin-bottom:11px"><b style="color:var(--ink)">生活习性：</b>近岸性，多活动于河口、港湾及浅海水域，水深一般小于 20 m。以鲻鱼、黄姑鱼、虾类等为食。群体活动，常见 3–10 头小群，偶见 20 头以上大群。</p>
            <p><b style="color:var(--ink)">繁殖习性：</b>繁殖高峰多在春夏季（3–6 月），每胎 1 仔，哺乳期约 1.5 年，性成熟约 9–10 龄。</p>
          </div>
          <div class="hr"></div>
          <div class="chips"><span class="tag pri">🤖 形态与习性描述可经「智能服务 → 多语言支持」一键翻译为英文</span></div>
    """) + '</div><div style="width:326px;flex:0 0 326px">'
            + card("分布概览", mapbox(294, 186, pins=[
                (60, 96, "#0e7490"), (120, 76, "#0e7490"), (152, 112, "#0891b2"),
                (204, 62, "#0891b2"), (252, 88, "#0e7490")],
                land=[(30, 46, 110, 74, -6), (150, 34, 110, 60, 4)], scale="示意 · 5 个分布点"))
            + card("最新观测记录", """
          <div class="tl">
            <div class="it"><span class="d"></span><div class="c">
              <b>湛江港航道外侧</b>　估算 6 头
              <div class="tm">2026-10-08 · 张海宁 · 水温 26.4 ℃</div></div></div>
            <div class="it"><span class="d"></span><div class="c">
              <b>雷州湾东部浅水区</b>　估算 3 头
              <div class="tm">2026-09-21 · 王庆林 · 水温 28.1 ℃</div></div></div>
            <div class="it"><span class="d g"></span><div class="c">
              <b>硇洲岛西侧</b>　估算 2 头
              <div class="tm">2026-08-30 · 张海宁 · 水温 29.7 ℃</div></div></div>
          </div>
          <div style="margin-top:11px">""" + btn("查看全部 8 条观测记录") + '</div>') + '</div></div>')
    return ("MB-SPEC-4", "物种详情页面", shell("spec", "物种信息管理 / 物种详情",
            "物种详情 — 中华白海豚", "MB-SPEC-4",
            actions=btn("编辑", "pri") + btn("删除", "dg") + btn("导出物种卡片"), body=body))


def _p5():
    """MB-SPEC-5 编辑物种信息。"""
    body = ('<div class="cols"><div style="flex:1">'
            + card("编辑物种信息 — SPEC-2026-0187 中华白海豚", form_title("1", "可修改字段") + '<div class="grid2">'
                   + field("中文名", "中华白海豚", req=True)
                   + field("学名", "Sousa chinensis", req=True)
                   + field("保护等级", "国家一级保护动物", "sel", req=True)
                   + field("IUCN 濒危等级", "易危 VU", "sel", req=True)
                   + field("分布范围描述", "珠江口、湛江港、雷州湾、北部湾北部、硇洲岛周边海域", span=True)
                   + field("形态特征", "体呈纺锤形，成体体长 2.0–2.5 m，体重 150–230 kg。吻突较长而尖，"
                           "背鳍呈三角形，位于体中部略后。成体体色多为粉白色。", "area", span=True)
                   + field("生活习性", "近岸性，活动于河口与港湾浅水区。以鲻鱼、黄姑鱼、虾类为食。"
                           "群体活动，常见 3–10 头小群。", "area", span=True) + '</div>'
                   + '<div class="hr"></div>'
                   + field("本次修改说明", "补充硇洲岛周边分布点，修正成体体长区间上限。", "area", req=True, span=True)
                   + '<div style="display:flex;gap:9px;margin-top:14px">'
                   + btn("保存并提交审核", "pri") + btn("取消") + btn("查看历史版本") + '</div>')
            + '</div><div style="width:330px;flex:0 0 330px">'
            + card("版本与变更记录", """
          <div class="tl">
            <div class="it"><span class="d"></span><div class="c">
              <b>v1.3</b>（当前编辑中）<div class="tm">张海宁 · 待保存</div></div></div>
            <div class="it"><span class="d"></span><div class="c">
              <b>v1.2</b>　补充繁殖习性与参考文献 3 篇
              <div class="tm">王庆林 · 2026-09-30 14:20</div></div></div>
            <div class="it"><span class="d g"></span><div class="c">
              <b>v1.1</b>　更新 IUCN 等级为易危 VU
              <div class="tm">张海宁 · 2026-09-12 10:05</div></div></div>
            <div class="it"><span class="d g"></span><div class="c">
              <b>v1.0</b>　初始版本创建
              <div class="tm">张海宁 · 2026-08-28 09:31</div></div></div>
          </div>
    """)
            + card("关联影响提示", note("该物种已被 <b>8 条观测记录</b> 关联引用。修改中文名或分类阶元不会影响"
                                    "已有观测记录，但修改后的名称将在这些记录中同步显示。", blue=True))
            + '</div></div>')
    return ("MB-SPEC-5", "编辑物种信息", shell("spec", "物种信息管理 / 编辑物种信息",
            "编辑物种信息", "MB-SPEC-5", actions=btn("保存草稿"), body=body))


def _p6():
    """MB-SPEC-6 删除物种（确认与操作日志）。"""
    rows = [
        [ck(), '<div class="thumb">🐠</div>', '<span class="lk">大黄鱼</span>',
         '<i style="color:var(--ink-3)">Larimichthys crocea</i>', "脊索动物门 / 硬骨鱼纲 / 鲈形目",
         lvl("极危"), "东海、南海北部近海", "2026-10-07 15:38",
         '<span class="lnks"><span class="lk">详情</span><span class="lk p">操作中…</span></span>'],
        [ck(), '<div class="thumb">🪸</div>', '<span class="lk">鹿角珊瑚</span>',
         '<i style="color:var(--ink-3)">Acropora cervicornis</i>', "刺胞动物门 / 珊瑚纲 / 石珊瑚目",
         lvl("极危"), "徐闻珊瑚礁自然保护区", "2026-10-06 11:04",
         '<span class="lnks"><span class="lk">详情</span><span class="lk">编辑</span></span>'],
    ]
    dlg = dialog("确认删除物种信息", """
      <div style="display:flex;gap:11px;align-items:flex-start;margin-bottom:16px">
        <span style="font-size:26px;line-height:1">⚠️</span>
        <div style="font-size:13px;line-height:1.8">
          即将删除物种 <b>大黄鱼（Larimichthys crocea，SPEC-2026-0183）</b>，该操作
          <b style="color:var(--err)">不可撤销</b>。
        </div>
      </div>
    """ + note("该物种已被 <b>14 条观测记录</b> 关联引用。删除后这些观测记录中的物种关联将被置空，"
               "可能导致统计数据不完整。<br>建议先解除关联，或改为将状态标记为「已废弃」。", title="影响评估")
        + '<div style="height:14px"></div><div class="grid2">'
        + field("操作类型", "软删除（保留历史，标记为已废弃）", "sel", req=True,
                hint="软删除后公众不可见，管理员可恢复")
        + field("删除原因", "分类修正，本条目与 SPEC-2026-0190 重复", "area", req=True, span=True) + '</div>'
        + '<div style="margin-top:12px">'
        + note("本次删除操作将记入用户活动日志，记录操作人（张海宁）、时间、对象与原因，供管理员追溯审计。", blue=True)
        + '</div>', footer=btn("取消") + btn("确认删除", "pri"))
    body = card("", table(
        ["<span class='ck'></span>", "图", "中文名", "学名", "分类阶元（门/纲/目）",
         "保护等级", "分布区域", "更新时间", "操作"], rows) + dlg, pad=False)
    return ("MB-SPEC-6", "删除物种信息", shell("spec", "物种信息管理 / 物种信息列表",
            "物种信息列表", "MB-SPEC-6", actions=btn("新增物种", "pri"), body=body))


def _p7():
    """MB-SPEC-7 高级检索结果。"""
    def hit(t):
        return f'<span style="background:#fef08a;padding:0 2px">{t}</span>'

    body = (card("高级检索条件", '<div class="grid3">'
                 + field("中文名包含", "海豚")
                 + field("学名包含", "Sousa")
                 + field("分类阶元", "脊索动物门 → 哺乳纲 → 鲸偶蹄目", "sel")
                 + field("保护等级", "国家一级保护动物", "sel")
                 + field("IUCN 等级", "易危 VU", "sel")
                 + field("分布区域", "湛江、雷州湾、珠江口", "sel")
                 + field("经度范围", "110.0 ~ 114.5")
                 + field("纬度范围", "20.0 ~ 23.5")
                 + field("收录时间", "2026-01-01 ~ 2026-10-08", "date")
                 + field("收录人", "张海宁", "sel", span=True) + '</div>'
                 + '<div style="margin-top:14px;display:flex;gap:9px;align-items:center">'
                 + btn("执行检索", "pri") + btn("重置条件") + btn("保存为常用检索")
                 + '<span class="mini" style="margin-left:auto">匹配到 '
                 + '<b style="color:var(--primary);font-size:14px">3</b> 条记录，用时 0.42 s</span></div>')
            + '<div style="height:13px"></div>'
            + card("检索结果", '<div class="cols"><div style="flex:1">'
                   + '<div style="border:1px solid var(--line);border-radius:8px;padding:13px 15px;margin-bottom:11px">'
                   + '<div style="display:flex;align-items:baseline;gap:10px">'
                   + f'<span style="font-size:15.5px;font-weight:600">{hit("中华白海豚")}</span>'
                   + '<span style="font-size:12px;color:var(--ink-3);font-style:italic">Sousa chinensis</span>'
                   + '<span class="tag err" style="margin-left:auto">国家一级保护</span></div>'
                   + '<div class="dl" style="grid-template-columns:92px 1fr;margin-top:9px">'
                   + '<dt>分类阶元</dt><dd>脊索动物门 / 哺乳纲 / 鲸偶蹄目 / 海豚科 / 驼海豚属</dd>'
                   + f'<dt>分布区域</dt><dd>珠江口、{hit("湛江")}港、{hit("雷州湾")}、北部湾北部</dd>'
                   + '<dt>关联观测</dt><dd><span class="lk">8 条观测记录</span>（最近：2026-10-08 湛江港航道外侧）</dd></div></div>'
                   + '<div style="border:1px solid var(--line);border-radius:8px;padding:13px 15px;margin-bottom:11px">'
                   + '<div style="display:flex;align-items:baseline;gap:10px">'
                   + '<span style="font-size:15.5px;font-weight:600">太平洋驼海豚</span>'
                   + '<span style="font-size:12px;color:var(--ink-3);font-style:italic">Sousa plumbea</span>'
                   + '<span class="tag" style="margin-left:auto">数据缺乏</span></div>'
                   + '<div class="dl" style="grid-template-columns:92px 1fr;margin-top:9px">'
                   + '<dt>分类阶元</dt><dd>脊索动物门 / 哺乳纲 / 鲸偶蹄目 / 海豚科 / 驼海豚属</dd>'
                   + '<dt>分布区域</dt><dd>印度洋沿岸（校内暂无本地分布记录）</dd>'
                   + '<dt>关联观测</dt><dd>0 条观测记录</dd></div></div>'
                   + '<div style="border:1px solid var(--line);border-radius:8px;padding:13px 15px">'
                   + '<div style="display:flex;align-items:baseline;gap:10px">'
                   + f'<span style="font-size:15.5px;font-weight:600">{hit("海豚")}科 — 宽吻海豚</span>'
                   + '<span style="font-size:12px;color:var(--ink-3);font-style:italic">Tursiops truncatus</span>'
                   + '<span class="tag ok" style="margin-left:auto">无危</span></div>'
                   + '<div class="dl" style="grid-template-columns:92px 1fr;margin-top:9px">'
                   + '<dt>分类阶元</dt><dd>脊索动物门 / 哺乳纲 / 鲸偶蹄目 / 海豚科 / 宽吻海豚属</dd>'
                   + f'<dt>分布区域</dt><dd>南海北部、{hit("湛江")}近海</dd>'
                   + '<dt>关联观测</dt><dd><span class="lk">5 条观测记录</span>（最近：2026-09-18 硇洲岛东南）</dd></div></div>'
                   + pager("共 3 条记录", 1, 1) + '</div>'
                   + '<div style="width:284px;flex:0 0 284px">'
                   + card("结果统计", '<div class="mini" style="margin-bottom:9px">按保护等级</div>'
                          + bars([("国家一级保护", 1, 33), ("极危 CR", 0, 2), ("易危 VU", 1, 33), ("无危 LC", 1, 33)])
                          + '<div class="hr"></div><div class="mini" style="margin-bottom:9px">按门类</div>'
                          + bars([("脊索动物门", 3, 100), ("刺胞动物门", 0, 2)])
                          + '<div style="margin-top:14px">' + btn("导出检索结果", "pri") + '</div>')
                   + '</div></div>'))
    return ("MB-SPEC-7", "物种高级检索", shell("spec", "物种信息管理 / 高级检索",
            "物种高级检索结果", "MB-SPEC-7",
            actions=btn("导出结果", "pri") + btn("另存为检索方案"), body=body))


def pages():
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6(), _p7()]
