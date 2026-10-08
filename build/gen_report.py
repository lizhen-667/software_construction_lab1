# -*- coding: utf-8 -*-
"""生成《海洋生物多样性信息管理系统 系统原型》报告（.md 与 .docx）。

文档结构对齐样例《企业薪酬管理系统-系统原型.doc》：
    封面 → 变更记录 → 系统主要角色 → 总体业务流程 →
    各业务模块（用例编号 + [角色] + 逐条事件流 + 原型页面绘制说明）

原型界面图不插入图片，改为在每个 [pic] 位置给出「原型绘制说明」，供手绘使用。

用法：  python build/gen_report.py
"""

import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx import Document                                  # noqa: E402
from docx.enum.section import WD_SECTION                   # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT             # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK    # noqa: E402
from docx.oxml import OxmlElement                          # noqa: E402
from docx.oxml.ns import qn                                # noqa: E402
from docx.shared import Cm, Pt, RGBColor                   # noqa: E402

import report_spec_a                                        # noqa: E402
import report_spec_b                                        # noqa: E402
import report_spec_c                                        # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = "海洋生物多样性信息管理系统-系统原型"

SONG, HEI = "宋体", "黑体"
BODY_PT = 12.0          # 小四号
CAP_PT = 10.5           # 五号
LINE = 1.25             # 1.25 倍行距


# ==========================================================================
# Markdown
# ==========================================================================
def md_of(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == "title":
            out.append("# " + b[1])
        elif k in ("h2", "h3", "h4"):
            out.append({"h2": "## ", "h3": "### ", "h4": "#### "}[k] + b[1])
        elif k == "p":
            out.append(b[1])
        elif k == "pc":
            out.append('<p style="text-align:center;text-indent:0">' + b[1] + "</p>")
        elif k == "pcbig":
            out.append('<p style="text-align:center;text-indent:0;font-size:15pt">'
                       "<b>" + b[1] + "</b></p>")
        elif k == "bullet":
            out.append("- " + b[1])
        elif k == "step":
            out.append("　　" + b[1])
        elif k == "sub":
            out.append("　　" + b[1])
        elif k == "table":
            _, cap, head, rows = b[:4]
            if cap:
                out.append(f'<p class="cap-t">{cap}</p>')
                out.append("")
            if head:
                out.append("| " + " | ".join(head) + " |")
                out.append("|" + "---|" * len(head))
            for r in rows:
                out.append("| " + " | ".join(str(c).replace("|", "／") for c in r) + " |")
        elif k == "draw":
            cap, desc = b[1], b[2]
            img = b[3] if len(b) > 3 else ""
            if img:
                out.append("")
                out.append(f"![{cap}](build/{img})")
                out.append("")
            out.append(f"> **{cap}**")
            out.append(">")
            out.append(f"> **布局**：{desc['layout']}")
            out.append(">")
            out.append("> **绘制要素**：")
            out.append(">")
            for e in desc["items"]:
                out.append("> - " + e)
            if desc.get("tips"):
                out.append(">")
                out.append("> **绘制提示**：" + desc["tips"])
            out.append("")
        elif k == "pb":
            out.append('<div style="page-break-after: always"></div>')
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ==========================================================================
# Word 辅助
# ==========================================================================
def _font(run, ea=SONG, size=BODY_PT, bold=False, color=None):
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    rPr = run._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rPr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi"):
        rf.set(qn(a), ea)
    rf.set(qn("w:eastAsia"), ea)


def _indent(par, chars=200, left_chars=0):
    pPr = par._p.get_or_add_pPr()
    ind = pPr.find(qn("w:ind"))
    if ind is None:
        ind = OxmlElement("w:ind")
        pPr.append(ind)
    if chars:
        ind.set(qn("w:firstLineChars"), str(chars))
        ind.set(qn("w:firstLine"), str(int(chars * BODY_PT * 20 / 100)))
    if left_chars:
        ind.set(qn("w:leftChars"), str(left_chars))
        ind.set(qn("w:left"), str(int(left_chars * BODY_PT * 20 / 100)))


def _spacing(par, before=0, after=0, line=LINE):
    pf = par.paragraph_format
    pf.line_spacing = line
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)


def png_size(path):
    """读取 PNG 的像素宽高（仅解析文件头，不加载图像库）。"""
    with open(path, "rb") as fh:
        head = fh.read(24)
    return struct.unpack(">II", head[16:24])


def _shade(el, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    el.append(shd)


def _para(doc, text, ea=SONG, size=BODY_PT, bold=False, indent=0, align=None,
          before=0, after=0, left=0, color=None):
    p = doc.add_paragraph()
    _spacing(p, before, after)
    if align is not None:
        p.alignment = align
    if indent or left:
        _indent(p, indent, left)
    if text:
        _font(p.add_run(text), ea, size, bold, color)
    return p


def _rich(doc, parts, ea=SONG, size=BODY_PT, indent=0, left=0, before=0, after=0):
    """parts: [(text, bold)]"""
    p = doc.add_paragraph()
    _spacing(p, before, after)
    if indent or left:
        _indent(p, indent, left)
    for t, b in parts:
        _font(p.add_run(t), ea, size, b)
    return p


# ==========================================================================
# Word 渲染
# ==========================================================================
def build_docx(blocks, path):
    doc = Document()

    st = doc.styles["Normal"]
    st.font.name = SONG
    st.font.size = Pt(BODY_PT)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), SONG)
    st.paragraph_format.line_spacing = LINE
    st.paragraph_format.space_after = Pt(0)

    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(2.0)
    sec.left_margin = sec.right_margin = Cm(1.7)

    # 页码
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _font(footer.add_run("第 "), SONG, CAP_PT)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    footer._p.append(fld)
    _font(footer.add_run(" 页　共 "), SONG, CAP_PT)
    fld2 = OxmlElement("w:fldSimple")
    fld2.set(qn("w:instr"), "NUMPAGES")
    footer._p.append(fld2)
    _font(footer.add_run(" 页"), SONG, CAP_PT)

    for b in blocks:
        k = b[0]

        if k == "title":
            _para(doc, b[1], HEI, 16, align=WD_ALIGN_PARAGRAPH.CENTER, after=4)

        elif k == "h2":
            _para(doc, b[1], HEI, BODY_PT, before=12, after=6)

        elif k == "h3":
            _para(doc, b[1], HEI, BODY_PT, before=10, after=4)

        elif k == "h4":
            _para(doc, b[1], HEI, BODY_PT, before=8, after=3)

        elif k == "p":
            _para(doc, b[1], SONG, BODY_PT, indent=200, after=3)

        elif k == "pc":
            _para(doc, b[1], HEI, BODY_PT, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)

        elif k == "pcbig":
            _para(doc, b[1], HEI, 15, align=WD_ALIGN_PARAGRAPH.CENTER, after=4)

        elif k == "bullet":
            _rich(doc, [("· ", False), (b[1], False)], indent=0, left=200, after=3)

        elif k == "step":
            _para(doc, b[1], SONG, BODY_PT, indent=0, left=200, after=2)

        elif k == "sub":
            _para(doc, b[1], SONG, BODY_PT, indent=0, left=400, after=2)

        elif k == "table":
            _, cap, head, rows = b[:4]
            if cap:
                _para(doc, cap, HEI, CAP_PT, align=WD_ALIGN_PARAGRAPH.CENTER, before=6, after=2)
            ncols = len(head) if head else len(rows[0])
            if head:
                t = doc.add_table(rows=1, cols=ncols)
                for i, h in enumerate(head):
                    c = t.rows[0].cells[i]
                    c.text = ""
                    pp = c.paragraphs[0]
                    pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    _spacing(pp, 1, 1, 1.0)
                    _font(pp.add_run(str(h)), HEI, CAP_PT, bold=True)
                    _shade(c._tc.get_or_add_tcPr(), "EEF2F5")
                body_rows = [t.add_row().cells for _ in rows]
            else:
                t = doc.add_table(rows=len(rows), cols=ncols)
                body_rows = [r.cells for r in t.rows]
            t.style = "Table Grid"
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            for cells, r in zip(body_rows, rows):
                for i, v in enumerate(r):
                    cells[i].text = ""
                    pp = cells[i].paragraphs[0]
                    _spacing(pp, 1, 1, 1.0)
                    _font(pp.add_run(str(v)), SONG, CAP_PT)

            # 可选：合并单元格（仅 Word；Markdown 无法表达合并）
            for row_idx, (c0, c1) in (b[4] if len(b) > 4 else []):
                if row_idx < len(body_rows):
                    merged = body_rows[row_idx][c0].merge(body_rows[row_idx][c1])
                    for extra in merged.paragraphs[1:]:      # 去掉合并带来的空段落
                        extra._p.getparent().remove(extra._p)
            _para(doc, "", SONG, 6, after=4)

        elif k == "draw":
            cap, desc = b[1], b[2]
            img = b[3] if len(b) > 3 else ""
            if img:
                pw, ph = png_size(os.path.join(HERE, img))
                box_w, box_h = Cm(16.5), Cm(22.5)
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                _spacing(p, 8, 4)
                run = p.add_run()
                if pw / ph > 16.5 / 22.5:
                    run.add_picture(os.path.join(HERE, img), width=box_w)
                else:
                    run.add_picture(os.path.join(HERE, img), height=box_h)
            t = doc.add_table(rows=1, cols=1)
            t.style = "Table Grid"
            cell = t.rows[0].cells[0]
            _shade(cell._tc.get_or_add_tcPr(), "F2FAFC")

            p = cell.paragraphs[0]
            _spacing(p, 3, 2, 1.15)
            _font(p.add_run(cap), HEI, BODY_PT, bold=True, color="0E7490")

            p = cell.add_paragraph()
            _spacing(p, 2, 2, 1.15)
            _font(p.add_run("布局："), HEI, CAP_PT, bold=True)
            _font(p.add_run(desc["layout"]), SONG, CAP_PT)

            p = cell.add_paragraph()
            _spacing(p, 2, 1, 1.15)
            _font(p.add_run("绘制要素："), HEI, CAP_PT, bold=True)
            for e in desc["items"]:
                pe = cell.add_paragraph()
                _spacing(pe, 0, 0, 1.15)
                _indent(pe, 0, 100)
                _font(pe.add_run("· " + e), SONG, CAP_PT)

            if desc.get("tips"):
                p = cell.add_paragraph()
                _spacing(p, 2, 2, 1.15)
                _font(p.add_run("绘制提示："), HEI, CAP_PT, bold=True)
                _font(p.add_run(desc["tips"]), SONG, CAP_PT)
            _para(doc, "", SONG, 6, after=4)

        elif k == "pb":
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.save(path)


def main():
    blocks = report_spec_a.blocks() + report_spec_b.blocks() + report_spec_c.blocks()

    md_path = os.path.join(ROOT, BASE + ".md")
    docx_path = os.path.join(ROOT, BASE + ".docx")

    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(md_of(blocks))
    build_docx(blocks, docx_path)

    kinds = {}
    for b in blocks:
        kinds[b[0]] = kinds.get(b[0], 0) + 1
    print(f"区块统计：{kinds}")
    print(f"Markdown → {md_path}")
    print(f"Word     → {docx_path}  ({os.path.getsize(docx_path):,} B)")
    print(f"绘制说明共 {kinds.get('draw', 0)} 处，表格 {kinds.get('table', 0)} 个")


if __name__ == "__main__":
    main()
