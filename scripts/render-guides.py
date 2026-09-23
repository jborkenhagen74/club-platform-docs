#!/usr/bin/env python3
"""Render the two German Markdown guides; Python 3.9+, reportlab 4.x.

Small deliberately bounded Markdown renderer: headings, paragraphs, lists,
fenced code and pipe tables. Markdown remains the editable source.
"""
from pathlib import Path
import hashlib
import html
import os
import re
import textwrap
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
    Spacer, PageBreak, Table, TableStyle, XPreformatted, KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
FONT = Path(os.environ.get('DOCS_FONT_DIR', '/usr/share/fonts/truetype/dejavu'))
for name, file in [('Body', 'DejaVuSans.ttf'), ('Body-Bold', 'DejaVuSans-Bold.ttf'),
                   ('Mono', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT / file)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Body-Bold', italic='Body', boldItalic='Body-Bold')
S = getSampleStyleSheet()
S.add(ParagraphStyle(name='Text', fontName='Body', fontSize=9, leading=13,
    spaceAfter=6, splitLongWords=True, allowWidows=0, allowOrphans=0))
S.add(ParagraphStyle(name='TitleGuide', fontName='Body-Bold', fontSize=26,
    leading=33, textColor=colors.HexColor('#173b49'), spaceAfter=22))
S.add(ParagraphStyle(name='H2Guide', fontName='Body-Bold', fontSize=14,
    leading=19, textColor=colors.HexColor('#173b49'), spaceBefore=17,
    spaceAfter=9, keepWithNext=True))
S.add(ParagraphStyle(name='H3Guide', parent=S['H2Guide'], fontSize=10.5,
    leading=15, spaceBefore=11, spaceAfter=6))
S.add(ParagraphStyle(name='CodeGuide', fontName='Mono', fontSize=7.1,
    leading=10, backColor=colors.HexColor('#f0f4f5'), borderPadding=7,
    leftIndent=7, rightIndent=7, spaceBefore=4, spaceAfter=12))
S.add(ParagraphStyle(name='Cell', parent=S['Text'], fontSize=8, leading=11.5, spaceAfter=0))
S.add(ParagraphStyle(name='BulletGuide', parent=S['Text'], leftIndent=15,
    firstLineIndent=-10, spaceAfter=5))
S.add(ParagraphStyle(name='TOCGuide', parent=S['Text'], leading=18, fontSize=9))

def inline(value):
    # Links retain their descriptive label in print; web links remain clickable.
    bits = re.split(r'(`[^`]+`|\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*)', value)
    result = []
    for bit in bits:
        if bit.startswith('`') and bit.endswith('`'):
            # Allow long paths to wrap as text, retaining a subdued code color.
            result.append('<font color="#245c70">' + html.escape(bit[1:-1]) + '</font>')
        elif bit.startswith('**') and bit.endswith('**'):
            result.append('<b>' + html.escape(bit[2:-2]) + '</b>')
        elif re.fullmatch(r'\[[^\]]+\]\([^)]+\)', bit):
            label, dest = re.match(r'\[([^\]]+)\]\(([^)]+)\)', bit).groups()
            if dest.startswith(('https://', 'http://')):
                result.append('<a href="' + html.escape(dest, quote=True) + '" color="#245c70">' + html.escape(label) + '</a>')
            else:
                result.append(html.escape(label))
        else:
            result.append(html.escape(bit))
    return ''.join(result)

class Guide(BaseDocTemplate):
    def __init__(self, path, short_title, digest, feature=False):
        super().__init__(str(path), pagesize=A4, rightMargin=43, leftMargin=43,
            topMargin=53, bottomMargin=46, title=short_title,
            author='Bunker Development', subject='Club Platform Training 1.2.0 | 23.09.2026' if feature else 'Club Platform 1.0.0 | 21.09.2026')
        self.feature = feature
        self.short_title = short_title
        self.digest = digest
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='guide', frames=[frame], onPage=self.decorate))
    def decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Body', 7)
        canvas.setFillColor(colors.HexColor('#526571'))
        canvas.drawString(43, A4[1]-31, 'BUNKER DEVELOPMENT  /  CLUB PLATFORM')
        canvas.drawRightString(A4[0]-43, A4[1]-31, 'Feature-Dokumentation · 23.09.2026' if self.feature else 'Dokumentation · 21.09.2026')
        canvas.setStrokeColor(colors.HexColor('#c9d7db'))
        canvas.line(43, 35, A4[0]-43, 35)
        canvas.drawString(43, 23, self.short_title + ' · MD ' + self.digest[:10])
        canvas.drawRightString(A4[0]-43, 23, str(doc.page))
        canvas.restoreState()
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == 'H2Guide':
            label = flowable.getPlainText()
            key = 'h-' + hashlib.sha256(label.encode()).hexdigest()[:12]
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(label, key, 0, False)
            self.notify('TOCEntry', (0, label, self.page, key))

def flowables(text, width):
    lines = text.splitlines()
    story = []
    i = 1
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('```'):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                raw = lines[i].expandtabs(4)
                code.extend(textwrap.wrap(raw, width=109, replace_whitespace=False,
                    drop_whitespace=False, subsequent_indent='    ') or [''])
                i += 1
            story.append(KeepTogether([XPreformatted(html.escape('\n'.join(code)), S['CodeGuide'])]))
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', x.replace(' ', '')) for x in cells):
                    rows.append(cells)
                i += 1
            count = len(rows[0])
            if any(len(row) != count for row in rows):
                raise ValueError('Inconsistent Markdown table')
            ratios = [0.30, 0.70] if count == 2 else [0.23, 0.53, 0.24]
            if count != len(ratios):
                ratios = [1/count]*count
            data = [[Paragraph(('<b>'+inline(v)+'</b>') if n == 0 else inline(v), S['Cell'])
                for v in row] for n, row in enumerate(rows)]
            table = Table(data, colWidths=[width*r for r in ratios], repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dcebee')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f7f8')]),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 7),
                ('RIGHTPADDING', (0,0), (-1,-1), 7),
                ('TOPPADDING', (0,0), (-1,-1), 7),
                ('BOTTOMPADDING', (0,0), (-1,-1), 7),
                ('LINEBELOW', (0,0), (-1,0), .6, colors.HexColor('#adc5cd'))]))
            story.extend([table, Spacer(1, 10)])
            continue
        if line.startswith('## '):
            story.append(Paragraph(inline(line[3:]), S['H2Guide']))
        elif line.startswith('### '):
            story.append(Paragraph(inline(line[4:]), S['H3Guide']))
        elif re.match(r'^(\d+\. |[-*] )', line):
            story.append(Paragraph(inline(line), S['BulletGuide']))
        else:
            parts = [line]
            while i+1 < len(lines) and lines[i+1].strip() and not re.match(r'^(#|\||```|\d+\. |[-*] )', lines[i+1]):
                i += 1
                parts.append(lines[i])
            story.append(Paragraph(inline(' '.join(parts)), S['Text']))
        i += 1
    return story

GUIDES = [
    ('build-und-installer', 'Club-Platform-Build-und-Installer-DE', 'Builds und Installer'),
    ('module-entwicklung-ohne-core', 'Club-Platform-Modulentwicklung-DE', 'Modulentwicklung ohne Core'),
    ('training-wearables-ai', 'Club-Platform-Training-Wearables-KI-DE', 'Training, Wearables und lokale KI')]

def main():
    import sys
    out = ROOT/'docs/pdf'
    out.mkdir(exist_ok=True)
    for source, target, title in GUIDES:
        if len(sys.argv)>1 and source not in sys.argv[1:]:
            continue
        path = ROOT/'docs/de'/f'{source}.md'
        raw = path.read_bytes()
        text = raw.decode('utf-8')
        doc = Guide(out/f'{target}.pdf', title, hashlib.sha256(raw).hexdigest(), source=='training-wearables-ai')
        toc = TableOfContents()
        toc.levelStyles = [S['TOCGuide']]
        story = [Spacer(1, 45), Paragraph('Club Platform', S['H3Guide']),
            Paragraph(title, S['TitleGuide']),
            Paragraph('Detaillierte Anleitung · Deutsch<br/>' + ('Feature-Stand · Training 1.3.0 · 23.09.2026' if source=='training-wearables-ai' else 'Version 1.0.0 Pilot · ABI V3 · Stand 21.09.2026'), S['Text']),
            Spacer(1, 18), Paragraph('Bunker Development', S['H3Guide']),
            Paragraph('Diese PDF wird aus der Markdown-Dokumentation erzeugt. Für das Kopieren längerer Befehle die verlinkte Markdown-Fassung verwenden; lange Codezeilen können im Druck umbrechen. Relative Verweise beziehen sich auf das öffentliche Doku-Repository.', S['Text']),
            Paragraph('<a href="https://github.com/jborkenhagen74/club-platform-docs/blob/'+('feature/training-wearable-import' if source=='training-wearables-ai' else 'main')+'/docs/de/'+source+'.md" color="#245c70">Markdown-Fassung im Doku-Repository öffnen</a>', S['Text']),
            Spacer(1, 20), Paragraph('Inhalt', S['H3Guide']), toc, PageBreak()]
        story.extend(flowables(text, doc.width))
        doc.multiBuild(story)
        print(out/f'{target}.pdf')

if __name__ == '__main__':
    main()
