# -*- coding: utf-8 -*-
"""模块一：用户与权限管理 —— 原型页面定义（MB-USER-*）。"""

from wire_kit import *  # noqa: F401,F403


def _p1():
    """MB-USER-1 用户登录。"""
    body = f"""
    <h2>用户登录</h2>
    <div class="st">海洋生物多样性信息管理系统 · 统一身份入口</div>
    <div class="fld"><label class="req">用户名 / 邮箱</label>
      <div class="ipt">zhanghn@gdou.edu.cn</div></div>
    <div class="fld"><label class="req">密码</label>
      <div class="ipt">••••••••••<span class="car" style="font-size:11px">👁</span></div></div>
    <div class="fld"><label>验证码</label>
      <div style="display:flex;gap:10px;align-items:center">
        <div class="ipt" style="flex:1">8F2K</div>
        <div style="width:96px;height:40px;border:1px solid var(--line-2);border-radius:5px;
             background:repeating-linear-gradient(45deg,#e0f2f7,#e0f2f7 6px,#cbe9f2 6px,#cbe9f2 12px);
             display:flex;align-items:center;justify-content:center;font-weight:700;letter-spacing:3px;
             color:#0e7490;font-size:17px;font-style:italic">8F2K</div>
        <span class="mini" style="white-space:nowrap">看不清？换一张</span>
      </div></div>
    <div class="fg"><label style="display:flex;align-items:center;gap:6px">{ck(True)} 记住我（7 天）</label>
      <a href="#">忘记密码？</a></div>
    {btn("登 录", "pri", sm=False)}
    <div class="note blue" style="margin-top:18px">
      <b>演示账号：</b>管理员 admin / 科研人员 zhanghn / 学生 liyx / 公众 guest</div>
    """
    return ("MB-USER-1", "用户登录", shell_plain("MB-USER-1", "用户登录", body +
            '<div style="text-align:center;font-size:12px;color:var(--ink-3);margin-top:14px">'
            '还没有账号？<a href="#" style="color:var(--primary);text-decoration:none">申请注册</a></div>'))


def _p2():
    """MB-USER-2 用户注册申请。"""
    body = f"""
    <h2>用户注册申请</h2>
    <div class="st">公众与学生账号需经管理员审核后方可登录使用</div>
    <div class="fld"><label class="req">申请角色</label>
      <div class="role">
        <div class="r on"><b>学生</b><span>可查询学习物种信息、参与课程实践</span></div>
        <div class="r"><b>公众</b><span>仅可访问公开物种信息与科普内容</span></div>
      </div>
      <div class="hint" style="margin-top:6px">科研人员 / 教师 账号由管理员直接创建，不在此申请。</div></div>
    <div class="fld"><label class="req">用户名</label><div class="ipt">liyuxin</div></div>
    <div class="fld"><label class="req">真实姓名</label><div class="ipt">李雨欣</div></div>
    <div class="fld"><label class="req">电子邮箱</label>
      <div class="ipt">liyuxin@stu.gdou.edu.cn</div></div>
    <div class="fld"><label class="req">手机号码</label><div class="ipt">138****6721</div></div>
    <div class="fld"><label>所在学院 / 单位</label>
      <div class="ipt sel"><span>水产学院</span><span class="car">▼</span></div></div>
    <div class="fld"><label class="req">申请理由</label>
      <div class="ta" style="min-height:56px">参与《海洋生物学》课程实践，需要查询近海鱼类的分类与分布数据。</div></div>
    <div class="fld"><label class="req">密码</label>
      <div class="ipt">••••••••<span class="car" style="font-size:11px">👁</span></div>
      <div class="hint">8–20 位，须同时包含字母与数字</div></div>
    <div class="fld"><label class="req">确认密码</label><div class="ipt">••••••••</div>
      <div class="errmsg">两次输入的密码不一致</div></div>
    <div class="fg"><label style="display:flex;align-items:center;gap:6px">{ck(True)} 我已阅读并同意《数据使用与隐私条款》</label></div>
    {btn("提交申请", "pri", sm=False)}
    """
    return ("MB-USER-2", "用户注册申请", shell_plain("MB-USER-2", "用户注册申请", body +
            '<div style="text-align:center;font-size:12px;color:var(--ink-3);margin-top:12px">'
            '已有账号？<a href="#" style="color:var(--primary);text-decoration:none">返回登录</a></div>'))


def _p3():
    """MB-USER-3 注册申请审核列表。"""
    rows = [
        [ck(), "SQ20261008001", "李雨欣", '<span class="tag info">学生</span>', "水产学院",
         "2026-10-08 09:12", '<span class="tag warn"><i class="dot"></i>待审核</span>',
         '<span class="lnks"><span class="lk">审核</span><span class="lk p">详情</span></span>'],
        [ck(), "SQ20261008002", "陈志远", '<span class="tag info">学生</span>', "海洋与气象学院",
         "2026-10-08 08:47", '<span class="tag warn"><i class="dot"></i>待审核</span>',
         '<span class="lnks"><span class="lk">审核</span><span class="lk p">详情</span></span>'],
        [ck(), "SQ20261007015", "黄伟明", '<span class="tag">公众</span>', "湛江市霞山区（社会公众）",
         "2026-10-07 21:03", '<span class="tag warn"><i class="dot"></i>待审核</span>',
         '<span class="lnks"><span class="lk">审核</span><span class="lk p">详情</span></span>'],
        [ck(), "SQ20261007011", "苏文静", '<span class="tag info">学生</span>', "水产学院",
         "2026-10-07 15:38", '<span class="tag ok"><i class="dot"></i>已通过</span>',
         '<span class="lnks"><span class="lk p">审核</span><span class="lk">详情</span></span>'],
        [ck(), "SQ20261006009", "吴俊杰", '<span class="tag">公众</span>', "个体经营者",
         "2026-10-06 19:22", '<span class="tag err"><i class="dot"></i>已驳回</span>',
         '<span class="lnks"><span class="lk p">审核</span><span class="lk">详情</span></span>'],
        [ck(), "SQ20261006004", "林嘉怡", '<span class="tag info">学生</span>', "海洋与气象学院",
         "2026-10-06 10:05", '<span class="tag ok"><i class="dot"></i>已通过</span>',
         '<span class="lnks"><span class="lk p">审核</span><span class="lk">详情</span></span>'],
    ]
    body = (filters(
        [("申请人 / 用户名", "text", "请输入姓名或用户名"),
         ("申请角色", "sel", "全部"),
         ("审核状态", "sel", "待审核"),
         ("申请时间", "date", "2026-10-01 ~ 2026-10-08")],
        btn("查询", "pri") + btn("重置"))
        + card("", table(
            ["<span class='ck'></span>", "申请编号", "申请人", "申请角色", "所在单位 / 学院",
             "申请时间", "审核状态", "操作"], rows)
            + '<div style="padding:0 16px 12px">'
            + btn("批量通过", "pri") + " " + btn("批量驳回", "dg") + " " + btn("导出列表")
            + "&nbsp;&nbsp;<span class='mini'>已选中 3 项</span></div>" + pager("共 46 条记录"), pad=False))
    return ("MB-USER-3", "注册申请审核", shell("user", "用户与权限管理 / 注册申请审核",
            "注册申请审核", "MB-USER-3",
            actions=btn("刷新列表") + btn("审核规则说明"), body=body, badge="3"))


def _p4():
    """MB-USER-4 注册申请审核处理（弹窗）。"""
    rows = [
        [ck(), "SQ20261008001", "李雨欣", '<span class="tag info">学生</span>', "水产学院",
         "2026-10-08 09:12", '<span class="tag warn"><i class="dot"></i>待审核</span>',
         '<span class="lnks"><span class="lk">审核</span><span class="lk p">详情</span></span>'],
        [ck(), "SQ20261008002", "陈志远", '<span class="tag info">学生</span>', "海洋与气象学院",
         "2026-10-08 08:47", '<span class="tag warn"><i class="dot"></i>待审核</span>',
         '<span class="lnks"><span class="lk">审核</span><span class="lk p">详情</span></span>'],
        [ck(), "SQ20261007015", "黄伟明", '<span class="tag">公众</span>', "湛江市霞山区（社会公众）",
         "2026-10-07 21:03", '<span class="tag warn"><i class="dot"></i>待审核</span>',
         '<span class="lnks"><span class="lk">审核</span><span class="lk p">详情</span></span>'],
    ]
    dlg = dialog("审核注册申请 — SQ20261008001", f"""
      {card("申请人信息", dl_list([
        ("用户名", "liyuxin"), ("真实姓名", "李雨欣"),
        ("申请角色", '<span class="tag info">学生</span>'),
        ("电子邮箱", "liyuxin@stu.gdou.edu.cn"),
        ("手机号码", "138****6721"),
        ("所在学院", "水产学院（海洋渔业科学与技术 2024 级）"),
        ("申请时间", "2026-10-08 09:12"),
        ("申请理由", "参与《海洋生物学》课程实践，需要查询近海鱼类的分类与分布数据。"),
      ]), tag="只读")}
      <div style="height:13px"></div>
      {card("审核处理", form_title("1", "审核结论") + """
        <div class="chips" style="margin-bottom:14px">
          <span class="tag ok" style="height:30px;padding:0 15px">✓ 通过申请</span>
          <span class="tag err" style="height:30px;padding:0 15px">✕ 驳回申请</span>
        </div>
      """ + '<div class="grid2">' + field("授予角色", "学生", "sel", req=True, hint="通过时生效，可多选角色")
              + field("账号有效期", "2029-06-30", "date", hint="默认至毕业年份，公众账号不限期")
              + field("审核意见", "材料属实，同意开通学生账号。", "area", span=True) + '</div>'
              + note("审核通过后，系统将按固定模板向申请人邮箱发送《账号开通通知》，并在用户活动日志中记录本次审核操作（操作人、时间、IP）。", blue=True))}
    """, footer=btn("取消") + btn("确认提交", "pri"), wide=True)
    body = table(["<span class='ck'></span>", "申请编号", "申请人", "申请角色", "所在单位 / 学院",
                  "申请时间", "审核状态", "操作"], rows) + dlg
    return ("MB-USER-4", "注册申请审核处理", shell("user", "用户与权限管理 / 注册申请审核",
            "注册申请审核", "MB-USER-4",
            actions=btn("刷新列表"), body=card("", body, pad=False), badge="3"))


def _p5():
    """MB-USER-5 用户管理列表。"""
    rows = [
        [ck(), "admin", "系统管理员", '<span class="tag pri">管理员</span>', "网络与教育技术中心",
         '<span class="tag ok">正常</span>', "2026-10-08 09:40",
         '<span class="lnks"><span class="lk">编辑</span><span class="lk">角色</span><span class="lk p">停用</span></span>'],
        [ck(True), "zhanghn", "张海宁", '<span class="tag info">科研人员/教师</span>', "水产学院",
         '<span class="tag ok">正常</span>', "2026-10-08 08:55",
         '<span class="lnks"><span class="lk">编辑</span><span class="lk">角色</span><span class="lk p">停用</span></span>'],
        [ck(True), "liyx", "李雨欣", '<span class="tag">学生</span>', "水产学院",
         '<span class="tag ok">正常</span>', "2026-10-07 22:10",
         '<span class="lnks"><span class="lk">编辑</span><span class="lk">角色</span><span class="lk p">停用</span></span>'],
        [ck(), "wangql", "王庆林", '<span class="tag info">科研人员/教师</span>', "海洋与气象学院",
         '<span class="tag ok">正常</span>', "2026-10-07 16:31",
         '<span class="lnks"><span class="lk">编辑</span><span class="lk">角色</span><span class="lk p">停用</span></span>'],
        [ck(), "guest01", "公众访客（演示）", '<span class="tag">公众</span>', "—",
         '<span class="tag warn">已停用</span>', "2026-09-28 11:07",
         '<span class="lnks"><span class="lk">编辑</span><span class="lk">角色</span><span class="lk">启用</span></span>'],
        [ck(), "chenzy", "陈志远", '<span class="tag">学生</span>', "海洋与气象学院",
         '<span class="tag ok">正常</span>', "2026-10-06 20:14",
         '<span class="lnks"><span class="lk">编辑</span><span class="lk">角色</span><span class="lk p">停用</span></span>'],
    ]
    body = (filters(
        [("用户名 / 姓名", "text", "请输入用户名或姓名"),
         ("角色", "sel", "全部"),
         ("账号状态", "sel", "全部"),
         ("所属单位", "sel", "全部")],
        btn("查询", "pri") + btn("重置"))
        + card("", table(
            ["<span class='ck'></span>", "用户名", "姓名", "角色", "所属单位 / 学院",
             "账号状态", "最近登录", "操作"], rows)
            + '<div style="padding:0 16px 12px">'
            + btn("新建用户", "pri") + " " + btn("批量停用", "dg") + " " + btn("导出列表")
            + "&nbsp;&nbsp;<span class='mini'>已选中 2 项</span></div>" + pager("共 213 条记录"), pad=False))
    return ("MB-USER-5", "用户管理", shell("user", "用户与权限管理 / 用户管理",
            "用户管理", "MB-USER-5",
            actions=btn("新建用户", "pri") + btn("导入用户"), body=body))


def _p6():
    """MB-USER-6 用户角色分配（弹窗）。"""
    rows = [
        [ck(), "admin", "系统管理员", '<span class="tag pri">管理员</span>', "网络与教育技术中心",
         '<span class="tag ok">正常</span>', "2026-10-08 09:40",
         '<span class="lnks"><span class="lk">编辑</span><span class="lk">角色</span></span>'],
        [ck(True), "zhanghn", "张海宁", '<span class="tag info">科研人员/教师</span>', "水产学院",
         '<span class="tag ok">正常</span>', "2026-10-08 08:55",
         '<span class="lnks"><span class="lk">编辑</span><span class="lk">角色</span></span>'],
        [ck(True), "liyx", "李雨欣", '<span class="tag">学生</span>', "水产学院",
         '<span class="tag ok">正常</span>', "2026-10-07 22:10",
         '<span class="lnks"><span class="lk">编辑</span><span class="lk">角色</span></span>'],
    ]
    dlg = dialog("分配角色 — 已选中 2 个用户", note(
        "系统采用 RBAC（基于角色的访问控制）模型。为用户分配角色后，该用户即继承该角色所定义的全部功能与数据权限；"
        "清除旧角色并重新赋予后立即生效，用户需重新登录。", title="权限说明", blue=True) + """
      <div style="height:14px"></div>
      <div style="font-size:13px;font-weight:600;margin-bottom:10px">可选角色（可多选）</div>
      <table class="tb">
        <thead><tr><th style="width:36px"></th><th>角色名称</th><th>角色标识</th><th>权限范围</th></tr></thead>
        <tbody>
          <tr><td>""" + ck(True) + """</td><td>科研人员 / 教师</td><td class="mono">ROLE_RESEARCHER</td>
              <td><span class="tag">物种：增删改查</span> <span class="tag">观测：增删改查</span> <span class="tag">可视化：查看导出</span></td></tr>
          <tr><td>""" + ck() + """</td><td>学生</td><td class="mono">ROLE_STUDENT</td>
              <td><span class="tag">物种：查看</span> <span class="tag">观测：查看</span> <span class="tag">可视化：查看</span></td></tr>
          <tr><td>""" + ck() + """</td><td>公众</td><td class="mono">ROLE_PUBLIC</td>
              <td><span class="tag">仅公开物种信息</span></td></tr>
          <tr><td>""" + ck() + """</td><td>管理员</td><td class="mono">ROLE_ADMIN</td>
              <td><span class="tag err">全部功能（含用户管理、数据备份）</span></td></tr>
        </tbody>
      </table>
      <div style="height:13px"></div>
    """ + field("变更原因", "新增观测小组教师账号权限", "area", span=True),
        footer=btn("取消") + btn("清除旧角色并重新赋予", "pri"), wide=True)
    body = table(["<span class='ck'></span>", "用户名", "姓名", "角色", "所属单位 / 学院",
                  "账号状态", "最近登录", "操作"], rows) + dlg
    return ("MB-USER-6", "用户角色分配", shell("user", "用户与权限管理 / 用户管理",
            "用户管理", "MB-USER-6", actions=btn("批量分配角色", "pri") + btn("刷新"),
            body=card("", body, pad=False)))


def _p7():
    """MB-USER-7 角色权限配置（RBAC）。"""
    rows = [
        ["模块一 用户与权限管理", "用户注册与审核", ck(False), ck(False), ck(False), ck(True), ck(True)],
        ["模块一 用户与权限管理", "查看用户列表", ck(False), ck(False), ck(False), ck(True), ck(True)],
        ["模块一 用户与权限管理", "角色分配 / 权限配置", ck(False), ck(False), ck(False), ck(False), ck(True)],
        ["模块二 物种信息管理", "查看物种信息", ck(True), ck(True), ck(True), ck(True), ck(True)],
        ["模块二 物种信息管理", "新增 / 编辑物种", ck(False), ck(True), ck(False), ck(True), ck(True)],
        ["模块二 物种信息管理", "删除物种（需审核）", ck(False), ck(False), ck(False), ck(True), ck(True)],
        ["模块三 生态系统与观测", "查看观测记录", ck(False), ck(True), ck(True), ck(True), ck(True)],
        ["模块三 生态系统与观测", "创建 / 编辑观测记录", ck(False), ck(True), ck(False), ck(True), ck(True)],
        ["模块三 生态系统与观测", "删除观测记录", ck(False), ck(False), ck(False), ck(True), ck(True)],
        ["模块四 数据可视化与报表", "查看看板与地图", ck(True), ck(True), ck(True), ck(True), ck(True)],
        ["模块四 数据可视化与报表", "导出报表", ck(False), ck(True), ck(True), ck(True), ck(True)],
        ["模块五 智能服务", "图像识别 / 智能问答", ck(True), ck(True), ck(True), ck(True), ck(True)],
    ]
    body = note("权限以「角色 × 功能点」矩阵方式配置，勾选即授予。管理员拥有全部权限且不可取消；"
                "公众仅可访问标记为「公开」的物种数据。修改保存后，系统刷新对应角色的权限缓存，并在活动日志中记录变更。",
                title="配置说明", blue=True) + '<div style="height:13px"></div>' + card("", table(
        ["功能模块", "功能点", "公众", "学生", "科研人员/教师", "管理员",
         "<span style='color:#b91c1c'>超级管理员</span>"], rows)
        + '<div style="padding:14px 16px;display:flex;gap:9px;align-items:center">'
        + btn("保存配置", "pri") + btn("恢复默认权限") + btn("新增功能点")
        + '<span class="mini" style="margin-left:auto">最后修改：admin · 2026-10-05 14:22</span></div>', pad=False)
    return ("MB-USER-7", "角色权限配置", shell("user", "用户与权限管理 / 角色权限配置",
            "角色权限配置（RBAC）", "MB-USER-7", actions=btn("查看变更记录"), body=body))


def _p8():
    """MB-USER-8 用户活动日志。"""
    rows = [
        ["2026-10-08 09:40:12", "admin", '<span class="tag pri">管理员</span>',
         '<span class="tag info">审核通过</span>', "注册申请 SQ20261007011", "10.20.31.7",
         '<span class="tag ok">成功</span>'],
        ["2026-10-08 09:12:44", "liyuxin", '<span class="tag">公众</span>',
         '<span class="tag">提交申请</span>', "注册申请 SQ20261008001", "10.20.44.118",
         '<span class="tag ok">成功</span>'],
        ["2026-10-08 08:55:03", "zhanghn", '<span class="tag info">科研人员/教师</span>',
         '<span class="tag">新增</span>', "物种信息：中华白海豚 (Sousa chinensis)", "10.20.18.62",
         '<span class="tag ok">成功</span>'],
        ["2026-10-08 08:31:57", "wangql", '<span class="tag info">科研人员/教师</span>',
         '<span class="tag">导出</span>', "物种分布统计报表（Excel）", "10.20.18.95",
         '<span class="tag ok">成功</span>'],
        ["2026-10-07 22:10:31", "liyx", '<span class="tag">学生</span>',
         '<span class="tag err">越权访问</span>', "尝试删除物种信息 SPEC-2026-0187", "10.20.44.118",
         '<span class="tag err">已拦截</span>'],
        ["2026-10-07 16:31:08", "zhanghn", '<span class="tag info">科研人员/教师</span>',
         '<span class="tag">登录</span>', "系统登录", "10.20.18.62", '<span class="tag ok">成功</span>'],
        ["2026-10-07 16:30:41", "zhanghn", '<span class="tag info">科研人员/教师</span>',
         '<span class="tag err">登录失败</span>', "系统登录（密码错误 1/5）", "10.20.18.62",
         '<span class="tag err">失败</span>'],
    ]
    body = (filters(
        [("操作用户", "text", "请输入用户名"),
         ("操作类型", "sel", "全部"),
         ("操作时间", "date", "2026-10-01 ~ 2026-10-08"),
         ("执行结果", "sel", "全部")],
        btn("查询", "pri") + btn("重置") + btn("导出日志"))
        + card("", table(
            ["操作时间", "操作用户", "角色", "操作类型", "操作对象", "来源 IP", "执行结果"], rows, hl=4)
            + pager("共 8,412 条记录"), pad=False))
    return ("MB-USER-8", "用户活动日志", shell("user", "用户与权限管理 / 用户活动日志",
            "用户活动日志", "MB-USER-8",
            actions=btn("清理 90 天前日志") + btn("导出日志"), body=body))


def _p9():
    """MB-USER-9 个人信息维护。"""
    body = card("个人资料", """
      <div class="cols">
        <div style="width:172px;text-align:center;flex:0 0 172px">
          <div style="width:104px;height:104px;border-radius:50%;background:var(--primary-l);
               border:1px solid #bae6fd;display:flex;align-items:center;justify-content:center;
               font-size:36px;margin:0 auto 11px">张</div>
          <div>""" + btn("更换头像", "sm") + """</div>
          <div class="mini" style="margin-top:7px">支持 JPG / PNG，≤ 2 MB</div>
        </div>
        <div style="flex:1">
          <div class="grid2">
    """ + field("用户名", "zhanghn", hint="用户名创建后不可修改")
        + field("真实姓名", "张海宁", req=True)
        + field("电子邮箱", "zhanghn@gdou.edu.cn", req=True)
        + field("手机号码", "139****2043", req=True)
        + field("所属学院", "水产学院", kind="sel")
        + field("职称 / 身份", "副教授", kind="sel")
        + field("研究方向", "海洋鱼类分类与生态", span=True)
        + field("个人简介", "主要从事南海北部近海鱼类多样性调查与分类学研究，主持省级项目 2 项，发表论文 20 余篇。",
                "area", span=True) + """
          </div>
          <div style="margin-top:16px;display:flex;gap:9px">""" + btn("保存修改", "pri") + btn("取消") + """</div>
        </div>
      </div>
    """) + card("账号安全", """
      <div class="dl" style="grid-template-columns:132px 1fr">
        <dt>登录密码</dt><dd>已设置 · 上次修改 2026-08-19 &nbsp;""" + btn("修改密码") + """</dd>
        <dt>绑定邮箱</dt><dd>zhanghn@gdou.edu.cn <span class="tag ok">已验证</span></dd>
        <dt>账号角色</dt><dd><span class="tag pri">科研人员 / 教师</span> <span class="tag">学生</span>
          <span class="mini">（角色由管理员分配，如需变更请联系管理员）</span></dd>
        <dt>最近登录</dt><dd>2026-10-08 08:55 · IP 10.20.18.62 · Chrome / Windows</dd>
      </div>
    """)
    return ("MB-USER-9", "个人信息维护", shell("user", "个人中心 / 个人信息维护",
            "个人信息维护", "MB-USER-9", actions=btn("查看我的操作记录"), body=body))


def _p10():
    """MB-USER-10 修改密码（弹窗）。"""
    form_html = """
      <div class="cols">
        <div style="flex:1">
          <div class="fld" style="margin-bottom:14px"><label class="req">当前密码</label>
            <div class="ipt" style="width:100%">••••••••••</div></div>
          <div class="fld" style="margin-bottom:6px"><label class="req">新密码</label>
            <div class="ipt" style="width:100%">••••••••••••</div></div>
          <div style="margin:9px 0 14px">
            <div class="mini" style="margin-bottom:6px">密码强度：
              <span style="color:var(--ok);font-weight:600">强</span></div>
            <div style="display:flex;gap:5px">
              <span style="flex:1;height:6px;border-radius:3px;background:var(--ok)"></span>
              <span style="flex:1;height:6px;border-radius:3px;background:var(--ok)"></span>
              <span style="flex:1;height:6px;border-radius:3px;background:var(--ok)"></span>
            </div>
          </div>
          <div class="fld"><label class="req">确认新密码</label>
            <div class="ipt" style="width:100%">••••••••••••</div></div>
        </div>
        <div style="width:230px;flex:0 0 230px">
    """ + note("密码规则：<br>· 长度 8–20 位<br>· 须包含大小写字母<br>· 须包含数字<br>· 不得与用户名相同<br>· 不得与前 3 次密码重复",
               title="安全要求") + """
        </div>
      </div>
    """
    dlg = dialog("修改密码", form_html, footer=btn("取消") + btn("确认修改", "pri"))
    body = card("个人资料", """
      <div class="grid2">
    """ + field("用户名", "zhanghn", hint="用户名创建后不可修改")
        + field("真实姓名", "张海宁")
        + field("电子邮箱", "zhanghn@gdou.edu.cn")
        + field("手机号码", "139****2043") + """
      </div>
      <div style="margin-top:16px">""" + btn("保存修改") + """</div>
    """) + card("账号安全", """
      <div class="dl" style="grid-template-columns:132px 1fr">
        <dt>登录密码</dt><dd>已设置 · 上次修改 2026-08-19 &nbsp;""" + btn("修改密码", "pri") + """</dd>
        <dt>绑定邮箱</dt><dd>zhanghn@gdou.edu.cn <span class="tag ok">已验证</span></dd>
      </div>
    """) + dlg
    return ("MB-USER-10", "修改密码", shell("user", "个人中心 / 修改密码",
            "修改密码", "MB-USER-10", body=body))


def pages():
    return [_p1(), _p2(), _p3(), _p4(), _p5(), _p6(), _p7(), _p8(), _p9(), _p10()]
