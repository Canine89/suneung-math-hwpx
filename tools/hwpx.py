"""HWPX(OWPML) 저수준 빌더.

header.xml의 글꼴/글자모양/문단모양/테두리 정의를 레지스트리로 관리하고,
section0.xml에 들어갈 문단·표·수식·그림·글상자 XML 조각을 만든다.
단위: HWPUNIT (1pt = 100).
"""
from xml.sax.saxutils import escape
import itertools

PT = 100
MM = 7200 / 25.4  # 1mm = 283.46 HWPUNIT

NS = ('xmlns:ha="http://www.hancom.co.kr/hwpml/2011/app" '
      'xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph" '
      'xmlns:hp10="http://www.hancom.co.kr/hwpml/2016/paragraph" '
      'xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section" '
      'xmlns:hc="http://www.hancom.co.kr/hwpml/2011/core" '
      'xmlns:hh="http://www.hancom.co.kr/hwpml/2011/head" '
      'xmlns:hhs="http://www.hancom.co.kr/hwpml/2011/history" '
      'xmlns:hm="http://www.hancom.co.kr/hwpml/2011/master-page" '
      'xmlns:hpf="http://www.hancom.co.kr/schema/2011/hpf" '
      'xmlns:dc="http://purl.org/dc/elements/1.1/" '
      'xmlns:opf="http://www.idpf.org/2007/opf/" '
      'xmlns:ooxmlchart="http://www.hancom.co.kr/hwpml/2016/ooxmlchart" '
      'xmlns:hwpunitchar="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar" '
      'xmlns:epub="http://www.idpf.org/2007/ops" '
      'xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"')

LANGS = ["HANGUL", "LATIN", "HANJA", "JAPANESE", "OTHER", "SYMBOL", "USER"]
LANG_ATTR = ["hangul", "latin", "hanja", "japanese", "other", "symbol", "user"]

_ids = itertools.count(1100000001)


def uid():
    return next(_ids)


def h(v):
    return int(round(v))


class Header:
    """header.xml 레지스트리. 같은 속성은 같은 id를 재사용한다."""

    def __init__(self):
        self.fonts = []          # (name, type)
        self.char_prs = []       # dict
        self.para_prs = []       # dict
        self.border_fills = []   # dict
        self.tab_prs = []        # tuple of positions
        self._cache = {}
        # 기본값: borderFill 1(없음), 2(없음+채움없음) — charPr/pageBorderFill이 참조
        self.border_fill()
        self.border_fill(fill="none")
        self.tab_pr(())
        self.char_pr()   # id 0
        self.para_pr()   # id 0

    # ---- 글꼴 ----
    def font(self, name):
        for i, (n, _) in enumerate(self.fonts):
            if n == name:
                return i
        ftype = "TTF" if name in ("굴림체", "HYhwpEQ", "함초롬바탕", "함초롬돋움") else "HFT"
        self.fonts.append((name, ftype))
        return len(self.fonts) - 1

    def _reg(self, kind, store, item):
        key = (kind, tuple(sorted(item.items())))
        if key not in self._cache:
            store.append(item)
            self._cache[key] = len(store) - 1
        return self._cache[key]

    # ---- 글자 모양 ----
    def char_pr(self, font="신명 중명조", latin=None, size=11.2, bold=False, color="#000000",
                ratio=100, spacing=0, symbol=None):
        item = dict(font=font, latin=latin or font, symbol=symbol or latin or font, size=size,
                    bold=bold, color=color, ratio=ratio, spacing=spacing)
        for name in (item["font"], item["latin"], item["symbol"]):
            self.font(name)  # 글꼴 표는 fontfaces 보다 먼저 완성되어 있어야 한다
        return self._reg("char", self.char_prs, item)

    # ---- 문단 모양 ----
    def para_pr(self, align="JUSTIFY", left=0, right=0, indent=0, prev=0, next=0,
                line_type="PERCENT", line=160, tabs=(), keep_next=False, snap=0):
        item = dict(align=align, left=h(left), right=h(right), indent=h(indent), prev=h(prev),
                    next=h(next), line_type=line_type, line=h(line), tab=self.tab_pr(tuple(tabs)),
                    keep_next=keep_next, snap=snap)
        return self._reg("para", self.para_prs, item)

    def tab_pr(self, positions):
        if positions in self.tab_prs:
            return self.tab_prs.index(positions)
        self.tab_prs.append(positions)
        return len(self.tab_prs) - 1

    # ---- 테두리/배경 ----
    def border_fill(self, left="NONE", right="NONE", top="NONE", bottom="NONE",
                    width="0.12 mm", widths=None, fill=None, slash=False, color="#000000"):
        w = widths or {}
        item = dict(left=left, right=right, top=top, bottom=bottom,
                    wl=w.get("left", width), wr=w.get("right", width),
                    wt=w.get("top", width), wb=w.get("bottom", width),
                    fill=fill, slash=slash, color=color)
        return self._reg("bf", self.border_fills, item) + 1  # borderFill id는 1부터

    def box(self, width="0.12 mm", fill=None):
        return self.border_fill("SOLID", "SOLID", "SOLID", "SOLID", width=width, fill=fill)

    # ---- XML ----
    def xml(self, sec_cnt=1):
        o = ['<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>',
             f'<hh:head {NS} version="1.5" secCnt="{sec_cnt}">',
             '<hh:beginNum page="1" footnote="1" endnote="1" pic="1" tbl="1" equation="1"/>',
             '<hh:refList>', f'<hh:fontfaces itemCnt="{len(LANGS)}">']
        for lang in LANGS:
            o.append(f'<hh:fontface lang="{lang}" fontCnt="{len(self.fonts)}">')
            for i, (n, t) in enumerate(self.fonts):
                o.append(f'<hh:font id="{i}" face="{escape(n)}" type="{t}" isEmbedded="0">'
                         '<hh:typeInfo familyType="FCAT_GOTHIC" weight="6" proportion="4" contrast="0" '
                         'strokeVariation="1" armStyle="1" letterform="1" midline="1" xHeight="1"/></hh:font>')
            o.append('</hh:fontface>')
        o.append('</hh:fontfaces>')

        o.append(f'<hh:borderFills itemCnt="{len(self.border_fills)}">')
        for i, b in enumerate(self.border_fills):
            sl = 'CENTER' if b["slash"] else 'NONE'
            o.append(f'<hh:borderFill id="{i+1}" threeD="0" shadow="0" centerLine="NONE" breakCellSeparateLine="0">'
                     f'<hh:slash type="{sl}" Crooked="0" isCounter="0"/>'
                     '<hh:backSlash type="NONE" Crooked="0" isCounter="0"/>'
                     f'<hh:leftBorder type="{b["left"]}" width="{b["wl"]}" color="{b["color"]}"/>'
                     f'<hh:rightBorder type="{b["right"]}" width="{b["wr"]}" color="{b["color"]}"/>'
                     f'<hh:topBorder type="{b["top"]}" width="{b["wt"]}" color="{b["color"]}"/>'
                     f'<hh:bottomBorder type="{b["bottom"]}" width="{b["wb"]}" color="{b["color"]}"/>'
                     '<hh:diagonal type="SOLID" width="0.12 mm" color="#000000"/>')
            if b["fill"]:
                o.append(f'<hc:fillBrush><hc:winBrush faceColor="{b["fill"]}" hatchColor="#999999" alpha="0"/></hc:fillBrush>')
            o.append('</hh:borderFill>')
        o.append('</hh:borderFills>')

        o.append(f'<hh:charProperties itemCnt="{len(self.char_prs)}">')
        for i, c in enumerate(self.char_prs):
            fh, fl, fs = self.font(c["font"]), self.font(c["latin"]), self.font(c["symbol"])
            ids = [fh, fl, fh, fh, fl, fs, fl]
            refs = " ".join(f'{a}="{v}"' for a, v in zip(LANG_ATTR, ids))
            rat = " ".join(f'{a}="{c["ratio"]}"' for a in LANG_ATTR)
            spc = " ".join(f'{a}="{c["spacing"]}"' for a in LANG_ATTR)
            hund = " ".join(f'{a}="100"' for a in LANG_ATTR)
            zero = " ".join(f'{a}="0"' for a in LANG_ATTR)
            o.append(f'<hh:charPr id="{i}" height="{h(c["size"]*PT)}" textColor="{c["color"]}" shadeColor="none" '
                     'useFontSpace="0" useKerning="0" symMark="NONE" borderFillIDRef="2">'
                     f'<hh:fontRef {refs}/><hh:ratio {rat}/><hh:spacing {spc}/>'
                     f'<hh:relSz {hund}/><hh:offset {zero}/>'
                     + ('<hh:bold/>' if c["bold"] else '') +
                     '<hh:underline type="NONE" shape="SOLID" color="#000000"/>'
                     '<hh:strikeout shape="NONE" color="#000000"/><hh:outline type="NONE"/>'
                     '<hh:shadow type="NONE" color="#C0C0C0" offsetX="10" offsetY="10"/></hh:charPr>')
        o.append('</hh:charProperties>')

        o.append(f'<hh:tabProperties itemCnt="{len(self.tab_prs)}">')
        for i, tp in enumerate(self.tab_prs):
            if not tp:
                o.append(f'<hh:tabPr id="{i}" autoTabLeft="0" autoTabRight="0"/>')
                continue
            o.append(f'<hh:tabPr id="{i}" autoTabLeft="0" autoTabRight="0">')
            for pos in tp:
                kind = "LEFT"
                if isinstance(pos, tuple):
                    pos, kind = pos
                o.append('<hp:switch><hp:case hp:required-namespace="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar">'
                         f'<hh:tabItem pos="{h(pos)}" type="{kind}" leader="NONE" unit="HWPUNIT"/></hp:case>'
                         f'<hp:default><hh:tabItem pos="{h(pos)*2}" type="{kind}" leader="NONE"/></hp:default></hp:switch>')
            o.append('</hh:tabPr>')
        o.append('</hh:tabProperties>')

        o.append('<hh:numberings itemCnt="0"/>')
        o.append(f'<hh:paraProperties itemCnt="{len(self.para_prs)}">')
        for i, p in enumerate(self.para_prs):
            margin = (f'<hh:margin><hc:intent value="{p["indent"]}" unit="HWPUNIT"/>'
                      f'<hc:left value="{p["left"]}" unit="HWPUNIT"/><hc:right value="{p["right"]}" unit="HWPUNIT"/>'
                      f'<hc:prev value="{p["prev"]}" unit="HWPUNIT"/><hc:next value="{p["next"]}" unit="HWPUNIT"/></hh:margin>'
                      f'<hh:lineSpacing type="{p["line_type"]}" value="{p["line"]}" unit="HWPUNIT"/>')
            o.append(f'<hh:paraPr id="{i}" tabPrIDRef="{p["tab"]}" condense="0" fontLineHeight="0" snapToGrid="{p["snap"]}" '
                     'suppressLineNumbers="0" checked="0" textDir="LTR">'
                     f'<hh:align horizontal="{p["align"]}" vertical="BASELINE"/>'
                     '<hh:heading type="NONE" idRef="0" level="0"/>'
                     '<hh:breakSetting breakLatinWord="KEEP_WORD" breakNonLatinWord="BREAK_WORD" widowOrphan="0" '
                     f'keepWithNext="{1 if p["keep_next"] else 0}" keepLines="0" pageBreakBefore="0" lineWrap="BREAK"/>'
                     '<hh:autoSpacing eAsianEng="0" eAsianNum="0"/>'
                     '<hp:switch><hp:case hp:required-namespace="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar">'
                     + margin + '</hp:case><hp:default>' + margin + '</hp:default></hp:switch>'
                     '<hh:border borderFillIDRef="2" offsetLeft="0" offsetRight="0" offsetTop="0" offsetBottom="0" '
                     'connect="0" ignoreMargin="0"/></hh:paraPr>')
        o.append('</hh:paraProperties>')
        o.append('<hh:styles itemCnt="1"><hh:style id="0" type="PARA" name="바탕글" engName="Normal" '
                 'paraPrIDRef="0" charPrIDRef="0" nextStyleIDRef="0" langID="1042" lockForm="0"/></hh:styles>')
        o.append('</hh:refList>')
        o.append('<hh:compatibleDocument targetProgram="HWP201X"><hh:layoutCompatibility/></hh:compatibleDocument>')
        o.append('<hh:docOption><hh:linkinfo path="" pageInherit="0" footnoteInherit="0"/></hh:docOption>')
        o.append('<hh:trackchageConfig flags="56"/></hh:head>')
        return "".join(o)


# ---------------------------------------------------------------- 조각 XML

def t(text):
    """텍스트 (탭 문자는 hp:tab으로)."""
    parts = text.split("\t")
    out = escape(parts[0])
    for p in parts[1:]:
        out += '<hp:tab width="4000" leader="0" type="1"/>' + escape(p)
    return f"<hp:t>{out}</hp:t>"


def run(char_id, inner):
    return f'<hp:run charPrIDRef="{char_id}">{inner}</hp:run>'


def para(para_id, runs, page_break=False, col_break=False):
    return (f'<hp:p id="0" paraPrIDRef="{para_id}" styleIDRef="0" pageBreak="{1 if page_break else 0}" '
            f'columnBreak="{1 if col_break else 0}" merged="0">{"".join(runs)}</hp:p>')


def pos_xml(inline=True, vrel="PARA", hrel="COLUMN", voff=0, hoff=0, halign="LEFT", valign="TOP",
            flow=True, overlap=False):
    return (f'<hp:pos treatAsChar="{1 if inline else 0}" affectLSpacing="0" flowWithText="{1 if flow else 0}" '
            f'allowOverlap="{1 if overlap else 0}" holdAnchorAndSO="0" vertRelTo="{vrel}" horzRelTo="{hrel}" '
            f'vertAlign="{valign}" horzAlign="{halign}" vertOffset="{h(voff)}" horzOffset="{h(hoff)}"/>')


def equation(script, base_unit=1100, width=2000, height=1300):
    return (f'<hp:equation id="{uid()}" zOrder="0" numberingType="EQUATION" textWrap="TOP_AND_BOTTOM" '
            'textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" version="Equation Version 60" baseLine="85" '
            f'textColor="#000000" baseUnit="{base_unit}" lineMode="CHAR" font="HYhwpEQ">'
            f'<hp:sz width="{width}" widthRelTo="ABSOLUTE" height="{height}" heightRelTo="ABSOLUTE" protect="0"/>'
            + pos_xml(True, hrel="PARA") +
            '<hp:outMargin left="56" right="56" top="0" bottom="0"/>'
            f'<hp:shapeComment>수식입니다.</hp:shapeComment><hp:script>{escape(script)}</hp:script></hp:equation>')


def sublist(paras, valign="TOP", width=0, height=0):
    return (f'<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="{valign}" '
            f'linkListIDRef="0" linkListNextIDRef="0" textWidth="{h(width)}" textHeight="{h(height)}" '
            f'hasTextRef="0" hasNumRef="0">{"".join(paras)}</hp:subList>')


def table(rows, col_widths, row_heights, border_fill, cell_fills=None, inline=True, pos=None,
          in_margin=(510, 510, 141, 141), out_margin=(0, 0, 0, 0), valign="CENTER", wrap="TOP_AND_BOTTOM",
          z=0):
    """rows: [[paragraph-xml-list per cell]]. cell_fills: [[borderFill id]] (없으면 border_fill)."""
    W, H = sum(col_widths), sum(row_heights)
    l, r, tp, b = in_margin
    o = [f'<hp:tbl id="{uid()}" zOrder="{z}" numberingType="TABLE" textWrap="{wrap}" textFlow="BOTH_SIDES" '
         f'lock="0" dropcapstyle="None" pageBreak="NONE" repeatHeader="0" rowCnt="{len(rows)}" '
         f'colCnt="{len(col_widths)}" cellSpacing="0" borderFillIDRef="{border_fill}" noAdjust="1">',
         f'<hp:sz width="{h(W)}" widthRelTo="ABSOLUTE" height="{h(H)}" heightRelTo="ABSOLUTE" protect="0"/>',
         pos or pos_xml(inline),
         '<hp:outMargin left="{}" right="{}" top="{}" bottom="{}"/>'.format(*[h(v) for v in out_margin]),
         f'<hp:inMargin left="{l}" right="{r}" top="{tp}" bottom="{b}"/>']
    for ri, row in enumerate(rows):
        o.append('<hp:tr>')
        for ci, cell in enumerate(row):
            bf = cell_fills[ri][ci] if cell_fills else border_fill
            va = valign[ri][ci] if isinstance(valign, list) else valign
            o.append(f'<hp:tc name="" header="0" hasMargin="1" protect="0" editable="0" dirty="0" borderFillIDRef="{bf}">'
                     + sublist(cell, va) +
                     f'<hp:cellAddr colAddr="{ci}" rowAddr="{ri}"/><hp:cellSpan colSpan="1" rowSpan="1"/>'
                     f'<hp:cellSz width="{h(col_widths[ci])}" height="{h(row_heights[ri])}"/>'
                     f'<hp:cellMargin left="{l}" right="{r}" top="{tp}" bottom="{b}"/></hp:tc>')
        o.append('</hp:tr>')
    o.append('</hp:tbl>')
    return "".join(o)


def rounded_box(paras, width, height, ratio=20, line_w=0.54, inline=True, pos=None):
    """둥근 모서리 사각형 글상자 (홀수형, 제 2 교시)."""
    W, H = h(width), h(height)
    return (f'<hp:rect id="{uid()}" zOrder="1" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" '
            f'lock="0" dropcapstyle="None" href="" groupLevel="0" instid="{uid()}" ratio="{ratio}">'
            f'<hp:offset x="0" y="0"/><hp:orgSz width="{W}" height="{H}"/><hp:curSz width="{W}" height="{H}"/>'
            '<hp:flip horizontal="0" vertical="0"/>'
            f'<hp:rotationInfo angle="0" centerX="{W//2}" centerY="{H//2}" rotateimage="1"/>'
            '<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
            '<hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
            '<hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
            f'<hp:lineShape color="#000000" width="{h(line_w*35.28)}" style="SOLID" endCap="FLAT" headStyle="NORMAL" '
            'tailStyle="NORMAL" headfill="1" tailfill="1" headSz="MEDIUM_MEDIUM" tailSz="MEDIUM_MEDIUM" '
            'outlineStyle="NORMAL" alpha="0"/>'
            '<hc:fillBrush><hc:winBrush faceColor="#FFFFFF" hatchColor="#000000" alpha="0"/></hc:fillBrush>'
            '<hp:shadow type="NONE" color="#B2B2B2" offsetX="0" offsetY="0" alpha="0"/>'
            f'<hp:drawText lastWidth="{W}" name="" editable="0">' + sublist(paras, "CENTER") +
            '<hp:textMargin left="0" right="0" top="0" bottom="0"/></hp:drawText>'
            f'<hc:pt0 x="0" y="0"/><hc:pt1 x="{W}" y="0"/><hc:pt2 x="{W}" y="{H}"/><hc:pt3 x="0" y="{H}"/>'
            f'<hp:sz width="{W}" widthRelTo="ABSOLUTE" height="{H}" heightRelTo="ABSOLUTE" protect="0"/>'
            + (pos or pos_xml(inline)) +
            '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:shapeComment>사각형입니다.</hp:shapeComment></hp:rect>')


def vline(x, y, height, width=0.85, z=10):
    """쪽 위치에 고정된 세로 막대(단 구분선). 원본처럼 검은 채움 사각형으로 그린다."""
    W, Hh = h(width * 100), h(height)
    return (f'<hp:rect id="{uid()}" zOrder="{z}" numberingType="PICTURE" textWrap="IN_FRONT_OF_TEXT" textFlow="BOTH_SIDES" '
            f'lock="0" dropcapstyle="None" href="" groupLevel="0" instid="{uid()}" ratio="0">'
            f'<hp:offset x="0" y="0"/><hp:orgSz width="{W}" height="{Hh}"/><hp:curSz width="{W}" height="{Hh}"/>'
            '<hp:flip horizontal="0" vertical="0"/>'
            f'<hp:rotationInfo angle="0" centerX="{W//2}" centerY="{Hh//2}" rotateimage="1"/>'
            '<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
            '<hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
            '<hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
            '<hp:lineShape color="#000000" width="0" style="NONE" endCap="FLAT" headStyle="NORMAL" '
            'tailStyle="NORMAL" headfill="1" tailfill="1" headSz="MEDIUM_MEDIUM" tailSz="MEDIUM_MEDIUM" '
            'outlineStyle="NORMAL" alpha="0"/>'
            '<hc:fillBrush><hc:winBrush faceColor="#000000" hatchColor="#000000" alpha="0"/></hc:fillBrush>'
            '<hp:shadow type="NONE" color="#B2B2B2" offsetX="0" offsetY="0" alpha="0"/>'
            f'<hc:pt0 x="0" y="0"/><hc:pt1 x="{W}" y="0"/><hc:pt2 x="{W}" y="{Hh}"/><hc:pt3 x="0" y="{Hh}"/>'
            f'<hp:sz width="{W}" widthRelTo="ABSOLUTE" height="{Hh}" heightRelTo="ABSOLUTE" protect="0"/>'
            + pos_xml(False, vrel="PAPER", hrel="PAPER", voff=y, hoff=x, flow=False, overlap=True) +
            '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:shapeComment>단 구분선</hp:shapeComment></hp:rect>')


def picture(bin_id, width, height, px_w, px_h):
    W, H = h(width), h(height)
    return (f'<hp:pic id="{uid()}" zOrder="0" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" '
            f'lock="0" dropcapstyle="None" href="" groupLevel="0" instid="{uid()}" reverse="0">'
            f'<hp:offset x="0" y="0"/><hp:orgSz width="{W}" height="{H}"/><hp:curSz width="{W}" height="{H}"/>'
            '<hp:flip horizontal="0" vertical="0"/>'
            f'<hp:rotationInfo angle="0" centerX="{W//2}" centerY="{H//2}" rotateimage="1"/>'
            '<hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
            '<hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>'
            '<hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo>'
            f'<hc:img binaryItemIDRef="{bin_id}" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/>'
            f'<hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="{W}" y="0"/><hc:pt2 x="{W}" y="{H}"/><hc:pt3 x="0" y="{H}"/></hp:imgRect>'
            '<hp:imgClip left="0" right="0" top="0" bottom="0"/><hp:inMargin left="0" right="0" top="0" bottom="0"/>'
            f'<hp:imgDim dimwidth="{px_w}" dimheight="{px_h}"/><hp:effects/>'
            f'<hp:sz width="{W}" widthRelTo="ABSOLUTE" height="{H}" heightRelTo="ABSOLUTE" protect="0"/>'
            + pos_xml(True) +
            '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:shapeComment>그림입니다.</hp:shapeComment></hp:pic>')


def header_ctrl(paras, width, height, kind="header"):
    return (f'<hp:ctrl><hp:{kind} id="{uid()}" applyPageType="BOTH">'
            + sublist(paras, "TOP", width, height) + f'</hp:{kind}></hp:ctrl>')


def sec_pr(page_w, page_h, margins, col_gap, col_line="0.3 mm"):
    m = margins
    return ('<hp:secPr id="" textDirection="HORIZONTAL" spaceColumns="1134" tabStop="8000" tabStopVal="4000" '
            'tabStopUnit="HWPUNIT" outlineShapeIDRef="0" memoShapeIDRef="0" textVerticalWidthHead="0" masterPageCnt="0">'
            '<hp:grid lineGrid="0" charGrid="0" wonggojiFormat="0"/>'
            '<hp:startNum pageStartsOn="BOTH" page="0" pic="0" tbl="0" equation="0"/>'
            '<hp:visibility hideFirstHeader="0" hideFirstFooter="0" hideFirstMasterPage="0" border="SHOW_ALL" '
            'fill="SHOW_ALL" hideFirstPageNum="0" hideFirstEmptyLine="0" showLineNumber="0"/>'
            '<hp:lineNumberShape restartType="0" countBy="0" distance="0" startNumber="0"/>'
            f'<hp:pagePr landscape="WIDELY" width="{h(page_w)}" height="{h(page_h)}" gutterType="LEFT_ONLY">'
            f'<hp:margin header="{h(m["header"])}" footer="{h(m["footer"])}" gutter="0" left="{h(m["left"])}" '
            f'right="{h(m["right"])}" top="{h(m["top"])}" bottom="{h(m["bottom"])}"/></hp:pagePr>'
            '<hp:footNotePr><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" suffixChar=")" supscript="0"/>'
            '<hp:noteLine length="-1" type="SOLID" width="0.12 mm" color="#000000"/>'
            '<hp:noteSpacing betweenNotes="283" belowLine="567" aboveLine="850"/>'
            '<hp:numbering type="CONTINUOUS" newNum="1"/><hp:placement place="EACH_COLUMN" beneathText="0"/></hp:footNotePr>'
            '<hp:endNotePr><hp:autoNumFormat type="DIGIT" userChar="" prefixChar="" suffixChar=")" supscript="0"/>'
            '<hp:noteLine length="14692344" type="SOLID" width="0.12 mm" color="#000000"/>'
            '<hp:noteSpacing betweenNotes="0" belowLine="567" aboveLine="850"/>'
            '<hp:numbering type="CONTINUOUS" newNum="1"/><hp:placement place="END_OF_DOCUMENT" beneathText="0"/></hp:endNotePr>'
            '<hp:pageBorderFill type="BOTH" borderFillIDRef="1" textBorder="PAPER" headerInside="0" footerInside="0" fillArea="PAPER">'
            '<hp:offset left="1417" right="1417" top="1417" bottom="1417"/></hp:pageBorderFill>'
            '<hp:pageBorderFill type="EVEN" borderFillIDRef="1" textBorder="PAPER" headerInside="0" footerInside="0" fillArea="PAPER">'
            '<hp:offset left="1417" right="1417" top="1417" bottom="1417"/></hp:pageBorderFill>'
            '<hp:pageBorderFill type="ODD" borderFillIDRef="1" textBorder="PAPER" headerInside="0" footerInside="0" fillArea="PAPER">'
            '<hp:offset left="1417" right="1417" top="1417" bottom="1417"/></hp:pageBorderFill></hp:secPr>'
            f'<hp:ctrl><hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="2" sameSz="1" sameGap="{h(col_gap)}">'
            f'<hp:colLine type="NONE" width="{col_line}" color="#000000"/></hp:colPr></hp:ctrl>')


def section_xml(paragraphs):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
            f'<hs:sec {NS}>' + "".join(paragraphs) + '</hs:sec>')


def content_hpf(title, images):
    items = "".join(f'<opf:item id="{iid}" href="BinData/{fn}" media-type="image/png" isEmbeded="1"/>'
                    for iid, fn in images)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
            f'<opf:package {NS} version="" unique-identifier="" id="">'
            f'<opf:metadata><opf:title>{escape(title)}</opf:title><opf:language>ko</opf:language></opf:metadata>'
            '<opf:manifest><opf:item id="header" href="Contents/header.xml" media-type="application/xml"/>'
            '<opf:item id="section0" href="Contents/section0.xml" media-type="application/xml"/>'
            f'{items}<opf:item id="settings" href="settings.xml" media-type="application/xml"/></opf:manifest>'
            '<opf:spine><opf:itemref idref="header" linear="yes"/><opf:itemref idref="section0" linear="yes"/></opf:spine>'
            '</opf:package>')


VERSION_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><hv:HCFVersion '
               'xmlns:hv="http://www.hancom.co.kr/hwpml/2011/version" tagetApplication="WORDPROCESSOR" major="5" '
               'minor="1" micro="1" buildNumber="0" os="1" xmlVersion="1.5" application="Hancom Office Hangul" '
               'appVersion="13, 0, 0, 289 WIN32LEWindows_10"/>')
CONTAINER_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><ocf:container '
                 'xmlns:ocf="urn:oasis:names:tc:opendocument:xmlns:container" '
                 'xmlns:hpf="http://www.hancom.co.kr/schema/2011/hpf"><ocf:rootfiles>'
                 '<ocf:rootfile full-path="Contents/content.hpf" media-type="application/hwpml-package+xml"/>'
                 '</ocf:rootfiles></ocf:container>')
MANIFEST_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
                '<odf:manifest xmlns:odf="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"/>')
SETTINGS_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><ha:HWPApplicationSetting '
                'xmlns:ha="http://www.hancom.co.kr/hwpml/2011/app" '
                'xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0">'
                '<ha:CaretPosition listIDRef="0" paraIDRef="0" pos="0"/></ha:HWPApplicationSetting>')
