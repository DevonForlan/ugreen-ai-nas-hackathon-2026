"""DOCX-first editable proposal candidate; native Word renders the matching PDF.

Uses the existing python-docx, pywin32 and PyMuPDF. No model or NAS invocation.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile
from xml.etree import ElementTree as ET

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import pymupdf as pdf

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'submission/round1/archiverescue'
SOURCE = BASE / 'ArchiveRescue_Proposal_VISUAL_V3.md'
DOCX = BASE / 'ArchiveRescue_Proposal_VISUAL_V3.docx'
PDF = BASE / 'ArchiveRescue_Proposal_VISUAL_V3.pdf'
TMP = ROOT / 'tmp/archiverescue-visual-v3'
EVIDENCE = ROOT / 'collaboration/test-results/ARCHIVERESCUE-PROPOSAL-VISUAL-V3-001.json'
PROTECTED = {
    'ArchiveRescue_Proposal.pdf': '360a372dc79459bb81cd744a8acc2f622e79893ffeb4b9ca2e1fdc7887b3c1fc',
    'ArchiveRescue_Proposal_VISUAL_V2.pdf': '625c1145c844a7024339d3da1c73956ed999a0df7c0487cfb78a0ae0f2c2f3ef',
    'ArchiveRescue_Pretest_Skill.zip': '732abef29c100b44d49e3cc0bb2ace4e7bc829d40c596bf5deb8b14851117d77',
    'skill/SKILL.md': '3819b43d6dae1e3c9fc84df14843c7a93f3a7955f169305e35f7474aa3d634f5',
}
GRID = {'page_width_pt':595.28, 'page_height_pt':841.89, 'margin_pt':42,
        'content_width_pt':511.28, 'spacing_pt':[4,8,12,16,24],
        'workflow_width_pt':116.57, 'connector_width_pt':15,
        'workflow_height_pt':104, 'padding_pt':9, 'stroke_pt':0.75,
        'panel_width_pt':162.43, 'panel_gap_pt':12, 'panel_height_pt':224,
        'font':'Arial', 'body_pt':11, 'question_pt':11, 'diagram_pt':10.5,
        'line_pt':15, 'diagram_line_pt':13.5, 'disclosure_pt':9}
PALETTE = {'ink':'243A3F','accent':'4A7575','line':'ABBDBB','cool':'EAF1F0',
           'warm':'F3EDE4','human':'E6D8C0','gray':'F1F3F3','white':'FFFFFF'}
NS = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def norm(s):
    s=re.sub(r'(?<=\S)-\s*\n\s*(?=\S)','-',s)
    return ' '.join(s.translate(str.maketrans({'“':'"','”':'"','’':"'",'—':'-'})).split())


def read_source():
    original=(BASE/'ArchiveRescue_Proposal.md').read_text(encoding='utf-8')
    source=SOURCE.read_text(encoding='utf-8')
    pattern=r'^## Q(\d+)\. (.*?)\n\n(.*?)(?=\n## |\Z)'
    qa=re.findall(pattern,source,re.M|re.S)
    assert qa==re.findall(pattern,original,re.M|re.S)
    assert [int(n) for n,q,a in qa]==list(range(1,11))
    design=json.loads(re.search(r'```json\n(.*?)\n```',source,re.S).group(1))
    disclosure=original.split('## Component and AI disclosure\n\n')[1].strip()
    return qa,design,disclosure


def property_(parent,tag,attrs):
    element=parent.find(qn(tag))
    if element is None:
        element=OxmlElement(tag);parent.append(element)
    for k,v in attrs.items():element.set(qn('w:'+k),str(v))
    return element


def para(parent,text='',style=None,bold=None,size=None,after=None,before=None,align=None):
    p=parent.add_paragraph(style=style) if hasattr(parent,'add_paragraph') else None
    run=p.add_run(text);run.bold=bold
    if size:run.font.size=Pt(size)
    p.paragraph_format.widow_control=True
    if after is not None:p.paragraph_format.space_after=Pt(after)
    if before is not None:p.paragraph_format.space_before=Pt(before)
    if align is not None:p.alignment=align
    return p


def configure(doc):
    section=doc.sections[0]
    section.page_width=Pt(GRID['page_width_pt']);section.page_height=Pt(GRID['page_height_pt'])
    for side in ['top_margin','bottom_margin','left_margin','right_margin']:
        setattr(section,side,Pt(GRID['margin_pt']))
    section.header_distance=Pt(16);section.footer_distance=Pt(19)
    for name,size,bold,after,line in [('Normal',11,False,8,15),('Title',28,True,2,33),
        ('Subtitle',12,False,4,16),('Heading 2',11,True,5,15),
        ('AR Meta',9,False,10,12),('AR Number',9.5,True,4,12),
        ('AR Diagram',10.5,False,0,13.5),('AR Small',9,False,0,12)]:
        if name not in doc.styles:
            from docx.enum.style import WD_STYLE_TYPE
            doc.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
        s=doc.styles[name];s.font.name='Arial';s.font.size=Pt(size);s.font.bold=bold
        fonts=s.element.get_or_add_rPr().find(qn('w:rFonts'))
        for key in list(fonts.attrib):
            if key.rsplit('}',1)[-1].lower().endswith('theme'):del fonts.attrib[key]
        for role in ['ascii','hAnsi','eastAsia','cs']:fonts.set(qn('w:'+role),'Arial')
        s.font.italic=False;s.font.underline=False
        style_pr=s.element.get_or_add_pPr()
        for child in list(style_pr):
            if child.tag==qn('w:pBdr'):style_pr.remove(child)
        property_(style_pr,'w:snapToGrid',{'val':0})
        for child in list(s.element.get_or_add_rPr()):
            if child.tag in {qn('w:spacing'),qn('w:kern')}:s.element.rPr.remove(child)
        s.font.color.rgb=RGBColor.from_string(PALETTE['ink'])
        s.paragraph_format.space_after=Pt(after);s.paragraph_format.space_before=Pt(0)
        s.paragraph_format.line_spacing=Pt(line)
        s.paragraph_format.keep_with_next=name in {'Title','Subtitle','Heading 2'}
    foot=section.footer.paragraphs[0];foot.style='AR Small'
    foot.paragraph_format.tab_stops.add_tab_stop(Pt(GRID['content_width_pt']-29))
    foot.add_run('ArchiveRescue / Visual V3 candidate\t')
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');foot._p.append(field)
    props=doc.core_properties
    props.author='';props.last_modified_by='';props.title='ArchiveRescue - Companion-Aware NAS Intake - Visual V3'
    props.subject='Round 1 proposal candidate';props.comments=''


def title(doc):
    para(doc,'ArchiveRescue','Title')
    para(doc,'Companion-Aware NAS Intake','Subtitle')
    p=para(doc,'Unleash Your Creativity / Round 1 Proposal / Visual V3 candidate','AR Meta')
    borders=property_(p._p.get_or_add_pPr(),'w:pBdr',{})
    property_(borders,'w:bottom',{'val':'single','sz':6,'color':PALETTE['line'],'space':6})


def question(doc,qa,n,body=True):
    number,q,a=qa[n-1]
    para(doc,f'Q{number}. {q}','Heading 2',before=10)
    if body:para(doc,a.strip())


def table(doc,widths,height=None):
    t=doc.add_table(rows=1,cols=len(widths));t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER
    property_(t._tbl.tblPr,'w:tblLayout',{'type':'fixed'})
    property_(t._tbl.tblPr,'w:tblW',{'w':round(sum(widths)*20),'type':'dxa'})
    for col,width in zip(t.columns,widths):col.width=Pt(width)
    row=t.rows[0]
    if height:row.height=Pt(height);row.height_rule=WD_ROW_HEIGHT_RULE.EXACTLY
    property_(row._tr.get_or_add_trPr(),'w:cantSplit',{})
    for cell,width in zip(row.cells,widths):
        cell.width=Pt(width);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
        cell.paragraphs[0].paragraph_format.space_after=Pt(0)
        cell.paragraphs[0].paragraph_format.line_spacing=Pt(1)
        cell.paragraphs[0].add_run().font.size=Pt(1)
    return t


def box(cell,fill,padding=9,border=True):
    pr=cell._tc.get_or_add_tcPr()
    property_(pr,'w:shd',{'fill':fill,'val':'clear'})
    margins=property_(pr,'w:tcMar',{})
    for side in ['top','left','bottom','right']:property_(margins,'w:'+side,{'w':round(padding*20),'type':'dxa'})
    edges=property_(pr,'w:tcBorders',{})
    for side in ['top','left','bottom','right']:
        property_(edges,'w:'+side,{'val':'single' if border else 'nil','sz':6,'color':PALETTE['line']})


def cell_start(cell,text,style,bold=False):
    p=cell.paragraphs[0];p.style=style
    p.paragraph_format.line_spacing=None
    p.paragraph_format.space_after=None
    p.add_run(text).bold=bold
    return p


def workflow(doc,design):
    for row_index in range(2):
        widths=[GRID['workflow_width_pt'] if i%2==0 else GRID['connector_width_pt'] for i in range(7)]
        t=table(doc,widths,GRID['workflow_height_pt'])
        for col,cell in enumerate(t.rows[0].cells):
            if col%2:
                box(cell,PALETTE['white'],0,False);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                p=cell_start(cell,chr(0x2192),'AR Diagram');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
                continue
            index=row_index*4+col//2
            fill=PALETTE['cool'] if index<4 else PALETTE['warm']
            if index==4:fill=PALETTE['human']
            box(cell,fill)
            cell_start(cell,f'{index+1:02d}','AR Number',True)
            para(cell,design['workflow'][index],'AR Diagram')
        if row_index==0:
            p=para(doc,'4 '+chr(0x2193)+' 5','AR Diagram',before=4,after=4,align=WD_ALIGN_PARAGRAPH.CENTER)
            p.paragraph_format.keep_with_next=True
    para(doc,design['cancellation'],'AR Diagram',before=8,after=0)


def panels(doc,design):
    t=table(doc,[GRID['panel_width_pt'],12,GRID['panel_width_pt'],12,GRID['panel_width_pt']],GRID['panel_height_pt'])
    for i,cell in enumerate(t.rows[0].cells):
        if i%2:box(cell,PALETTE['white'],0,False);continue
        case=design['cases'][i//2];box(cell,PALETTE['cool'] if i==0 else (PALETTE['warm'] if i==2 else PALETTE['gray']))
        # A shared four-row subgrid fixes title/condition/cue/outcome baselines.
        nested=cell.add_table(rows=5,cols=1);nested.autofit=False
        inner=GRID['panel_width_pt']-2*GRID['padding_pt']
        nested.columns[0].width=Pt(inner)
        property_(nested._tbl.tblPr,'w:tblW',{'w':round(inner*20),'type':'dxa'})
        for row in nested.rows:row.cells[0].width=Pt(inner)
        heights=[20,43,26,78,32]
        for row,height in zip(nested.rows,heights):
            row.height=Pt(height);row.height_rule=WD_ROW_HEIGHT_RULE.EXACTLY
            property_(row._tr.get_or_add_trPr(),'w:cantSplit',{})
            box(row.cells[0],PALETTE['cool'] if i==0 else (PALETTE['warm'] if i==2 else PALETTE['gray']),0,False)
        cell_start(nested.cell(0,0),case['title'],'AR Diagram',True)
        cell_start(nested.cell(1,0),case['condition'],'AR Diagram')
        cue=['=',chr(0x2260),chr(0x2298)][i//2]
        p=cell_start(nested.cell(2,0),cue,'AR Diagram',True)
        p.runs[-1].font.size=Pt(16)
        cell_start(nested.cell(3,0),case['outcome'],'AR Diagram')
        cell_start(nested.cell(4,0),case.get('extra',''),'AR Diagram',True)
        for p in cell.paragraphs:
            if not p.text:
                p.paragraph_format.line_spacing=Pt(1)
                p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(0)
                for run in p.runs:run.font.size=Pt(1)


def capabilities(doc,fragments):
    t=doc.add_table(rows=3,cols=1);t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER
    t.columns[0].width=Pt(GRID['content_width_pt'])
    property_(t._tbl.tblPr,'w:tblW',{'w':round(GRID['content_width_pt']*20),'type':'dxa'})
    for row,fragment in zip(t.rows,fragments):
        row.height=Pt(52);row.height_rule=WD_ROW_HEIGHT_RULE.EXACTLY
        property_(row._tr.get_or_add_trPr(),'w:cantSplit',{})
        cell=row.cells[0];cell.width=Pt(GRID['content_width_pt'])
        box(cell,PALETTE['gray']);cell_start(cell,fragment,'AR Diagram')


def build_docx(qa,design,disclosure):
    doc=Document();configure(doc);title(doc)
    for n in [1,2,3]:question(doc,qa,n)
    question(doc,qa,4,False);workflow(doc,design)
    doc.add_page_break();title(doc)
    headline=table(doc,[GRID['content_width_pt']],65)
    box(headline.cell(0,0),PALETTE['cool'],12)
    p=cell_start(headline.cell(0,0),design['takeaway'],'AR Diagram',True)
    p.runs[-1].font.size=Pt(21);p.paragraph_format.line_spacing=Pt(27)
    question(doc,qa,5)
    question(doc,qa,6,False)
    capabilities(doc,design['capability_fragments'])
    question(doc,qa,7,False)
    for s in design['technical_fragments']:para(doc,s)
    doc.add_page_break();title(doc)
    question(doc,qa,8)
    question(doc,qa,9,False);panels(doc,design)
    question(doc,qa,10)
    para(doc,'Component and AI disclosure','Heading 2',size=9,before=12)
    para(doc,disclosure,'AR Small')
    doc.save(DOCX)
    # The python-docx template's unused thumbnail is not a submission asset.
    import io
    buffer=io.BytesIO()
    with zipfile.ZipFile(DOCX) as original,zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as clean:
        for name in original.namelist():
            if name.startswith('docProps/thumbnail.'):continue
            data=original.read(name)
            if name=='_rels/.rels':
                node=ET.fromstring(data)
                for item in list(node):
                    if item.get('Type','').endswith('/metadata/thumbnail'):node.remove(item)
                data=ET.tostring(node,encoding='utf-8',xml_declaration=True)
            clean.writestr(name,data)
    DOCX.write_bytes(buffer.getvalue())


def word_worker(edit_test=False):
    import win32com.client
    import win32process
    app=None;document=None
    try:
        app=win32com.client.DispatchEx('Word.Application');app.Visible=False;app.DisplayAlerts=0;app.AutomationSecurity=3
        import win32api
        blank=app.Documents.Add()
        pid=win32process.GetWindowThreadProcessId(blank.ActiveWindow.Hwnd)[1]
        process=win32api.OpenProcess(0x1001,False,pid)
        created=win32process.GetProcessTimes(process)['CreationTime'].isoformat();process.Close()
        (TMP/'owned-word-process.json').write_text(json.dumps({'pid':pid,'created':created}),encoding='utf-8')
        blank.Close(False)
        target=DOCX
        if edit_test:
            target=TMP/'editable-probe.docx';target.write_bytes(DOCX.read_bytes())
        document=app.Documents.Open(str(target.resolve()),False,not edit_test,False)
        if edit_test:
            for old,new in [('Photographers and studios','Photographers and small studios'),
                            ('inspect metadata and hashes','inspect file metadata and hashes')]:
                target_range=document.Content
                search=target_range.Find;search.ClearFormatting();search.Text=old
                search.Forward=True;search.Wrap=0;search.MatchWildcards=False
                assert search.Execute() and target_range.Text==old,'Word edit probe failed'
                target_range.Text=new
            document.Tables(1).Cell(1,1).Shading.BackgroundPatternColor=0xE8F2F2
            document.Save()
        document.Repaginate()
        page_count=document.ComputeStatistics(2)
        output=TMP/'editable-probe.pdf' if edit_test else PDF
        document.ExportAsFixedFormat(str(output.resolve()),17,False,0,0,1,1,0,False,False,0,True,False,False)
        data={'application':'Microsoft Word','version':app.Version,'pages':page_count,
              'edit_probe':edit_test,'tables':document.Tables.Count,'inline_shapes':document.InlineShapes.Count,
              'floating_shapes':document.Shapes.Count}
        (TMP/('word-edit-probe.json' if edit_test else 'word-render.json')).write_text(json.dumps(data),encoding='utf-8')
        print(json.dumps(data))
    finally:
        if document is not None:document.Close(False)
        if app is not None:app.Quit(False)


def run_word(edit_test=False):
    cmd=[sys.executable,str(Path(__file__).resolve()),'--word-worker']
    if edit_test:cmd.append('--edit-probe')
    (TMP/'owned-word-process.json').unlink(missing_ok=True)
    try:
        p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=90)
    except subprocess.TimeoutExpired:
        # Only the isolated DispatchEx Word instance owned by this invocation.
        import win32api,win32process
        marker=TMP/'owned-word-process.json'
        if marker.exists():
            identity=json.loads(marker.read_text());owned=win32api.OpenProcess(0x1001,False,identity['pid'])
            try:
                if win32process.GetProcessTimes(owned)['CreationTime'].isoformat()==identity['created']:
                    win32api.TerminateProcess(owned,1)
            finally:owned.Close()
        raise RuntimeError('Owned Word render timed out; no other Word process touched')
    assert p.returncode==0,p.stderr
    print(p.stdout)


def docx_text(data):
    import io
    values=[]
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None
        assert not any(n.startswith(('word/media/','word/embeddings/')) or 'vbaProject' in n for n in z.namelist())
        for name in z.namelist():
            if name.endswith('.rels'):
                assert 'TargetMode="External"' not in z.read(name).decode('utf-8')
            if name.endswith('.xml'):
                node=ET.fromstring(z.read(name))
                assert not node.findall('.//w:vanish',NS)
                assert not node.findall('.//w:documentProtection',NS)
                if name.startswith('word/'):
                    for p in node.findall('.//w:p',NS):
                        values.append(''.join((e.text or '') if e.tag==qn('w:t') else
                            (' ' if e.tag in {qn('w:br'),qn('w:tab'),qn('w:cr')} else '') for e in p.iter()))
    return '\n'.join(values)


def inspect_docx(data,scanner):
    import io
    docx_text(data)
    findings=[]
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert len(z.infolist())<100 and sum(i.file_size for i in z.infolist())<10_000_000
        for item in z.infolist():
            name=item.filename
            assert name.endswith(('.xml','.rels')) and '..' not in Path(name).parts
            assert not name.startswith('/') and not item.flag_bits&1
            assert not re.search(r'(?i)devon|[A-Z]:\\|file://',z.read(name).decode('utf-8-sig'))
            findings.extend(scanner.scan_blob('ArchiveRescue_Proposal_VISUAL_V3.docx/'+name,z.read(name)))
        core=ET.fromstring(z.read('docProps/core.xml'))
        for element in core:
            if element.tag.rsplit('}',1)[-1] in {'creator','lastModifiedBy'}:assert not element.text
    return findings


def geometry(doc):
    def frames(page,kind):
        found=[]
        for path in page.get_drawings():
            r=path['rect']
            if not path.get('fill'):continue
            if kind=='workflow' and 110<r.width<120 and 90<r.height<130:found.append(r)
            if kind=='panel' and 160<r.width<164 and 200<r.height<250:found.append(r)
        return sorted(found,key=lambda r:(round(r.y0,1),r.x0))
    flow=frames(doc[0],'workflow');cases=frames(doc[2],'panel')
    assert len(flow)==8 and len(cases)==3
    assert max(r.width for r in flow)-min(r.width for r in flow)<0.5
    assert max(r.height for r in flow)-min(r.height for r in flow)<0.2
    for row in [flow[:4],flow[4:]]:
        assert max(r.y0 for r in row)-min(r.y0 for r in row)<0.2
    for a,b in zip(flow[:4],flow[4:]):assert abs(a.x0-b.x0)<0.2
    arrows=doc[0].search_for(chr(0x2192));assert len(arrows)==6
    for row in [flow[:4],flow[4:]]:
        actual=[a for a in arrows if row[0].y0<a.y0<row[0].y1]
        assert len(actual)==3
        actual.sort(key=lambda a:a.x0)
        for a,left,right in zip(actual,row,row[1:]):
            assert abs((a.x0+a.x1)/2-(left.x1+right.x0)/2)<1.5
        assert max(a.y0 for a in actual)-min(a.y0 for a in actual)<0.2
    for row in range(2):
        numbers=[doc[0].search_for(f'{i:02d}')[0] for i in range(row*4+1,row*4+5)]
        assert max(r.y0 for r in numbers)-min(r.y0 for r in numbers)<0.2
    assert max(r.width for r in cases)-min(r.width for r in cases)<0.2
    assert max(r.height for r in cases)-min(r.height for r in cases)<0.2
    assert max(r.y0 for r in cases)-min(r.y0 for r in cases)<0.2
    for block in doc[2].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            if not ''.join(s['text'] for s in line['spans']).strip():continue
            r=pdf.Rect(line['bbox'])
            for case in cases:
                if case.x0<r.x0<case.x1 and case.y0<r.y0<case.y1:
                    assert r.x0-case.x0>=8 and case.x1-r.x1>=8,('panel padding/overflow',r,case)
    serialize=lambda r:[round(r.x0,2),round(r.y0,2),round(r.width,2),round(r.height,2)]
    return {'workflow_frames_pt':[serialize(r) for r in flow],
            'panel_frames_pt':[serialize(r) for r in cases],
            'arrows_centered':True,'equal_number_baselines':True,'panel_text_padding_pass':True}


def validate(qa,design,disclosure):
    alpha=lambda s:len(re.findall('[A-Za-z0-9]+',s))
    canonical=' '.join(a for n,q,a in qa)
    flow=design['workflow']
    original_flow=' '.join([flow[0],flow[1],flow[2].removeprefix('Compare: '),
        flow[4].removeprefix('Human: '),*flow[5:],design['cancellation']])
    assert norm(original_flow)==norm(qa[3][2])
    assert norm(' '.join(design['capability_fragments']))==norm(qa[5][2])
    assert norm(' '.join(design['technical_fragments']))==norm(qa[6][2])
    assert norm(' '.join(' '.join(c[k] for k in ['title','condition','outcome']) for c in design['cases']))==norm(qa[8][2])
    extras=[design['takeaway'],'Compare:','Companion/conflict exception','Human:']
    extras += [c['extra'] for c in design['cases'] if c.get('extra')]
    nonlicense='Codex:'+disclosure.split('Codex:',1)[1].split('Sources:',1)[0]
    counts={'answers_whitespace':len(canonical.split()),'answers_alphanumeric':alpha(canonical),
            'added_diagram_whitespace':sum(len(s.split()) for s in extras),
            'added_diagram_alphanumeric':sum(alpha(s) for s in extras)}
    counts['all_substantive_whitespace']=counts['answers_whitespace']+counts['added_diagram_whitespace']
    counts['all_substantive_alphanumeric']=counts['answers_alphanumeric']+counts['added_diagram_alphanumeric']
    counts['strict_whitespace']=counts['all_substantive_whitespace']+len(nonlicense.split())
    counts['strict_alphanumeric']=counts['all_substantive_alphanumeric']+alpha(nonlicense)
    assert counts['strict_alphanumeric']<=500
    text_docx=docx_text(DOCX.read_bytes());flat_docx=norm(text_docx)
    assert not re.search(r'(?i)devon|C:\\|session log|[a-f0-9]{40}\b',text_docx)
    with pdf.open(PDF) as d:
        assert len(d)==3 and PDF.stat().st_size<=1_000_000
        assert not d.metadata.get('author')
        text_pdf='\n'.join(p.get_text() for p in d);flat_pdf=norm(text_pdf)
        assert not d.embfile_count() and not d.is_form_pdf and not d.get_ocgs()
        assert not re.search(r'(?i)devon|C:\\|session log|[a-f0-9]{40}\b',text_pdf)
        for n,q,a in qa:
            for flat in [flat_docx,flat_pdf]:
                assert norm(f'Q{n}. {q}') in flat,('question missing',n)
                if int(n) not in [4,6,7,9]:assert norm(a) in flat,('answer missing',n)
        fragments=design['workflow']+[design['cancellation'],design['takeaway'],disclosure]
        fragments+=design['capability_fragments']+design['technical_fragments']
        fragments+=[v for c in design['cases'] for v in c.values()]
        for s in fragments:
            assert norm(s) in flat_docx,('docx fragment missing',s)
            assert norm(s) in flat_pdf,('pdf fragment missing',s)
        measured=geometry(d)
        for page in d:
            assert not page.get_images()
            lines=[]
            for b in page.get_text('dict')['blocks']:
                for line in b.get('lines',[]):
                    if not ''.join(s['text'] for s in line['spans']).strip():continue
                    r=pdf.Rect(line['bbox']);assert r.x0>25 and r.y0>20 and r.x1<575 and r.y1<827
                    lines.append(r)
            for i,a in enumerate(lines):
                for b in lines[i+1:]:assert (a&b).is_empty or (a&b).get_area()<=1,('overlap',page.number+1,a,b)
            for scale in [1,1.5]:page.get_pixmap(matrix=pdf.Matrix(scale,scale)).save(TMP/f'page-{page.number+1}-{scale}.png')
    probe=Document(TMP/'editable-probe.docx')
    probe_text=docx_text((TMP/'editable-probe.docx').read_bytes())
    assert 'Photographers and small studios' in probe_text and 'inspect file metadata and hashes' in probe_text
    assert json.loads((TMP/'word-edit-probe.json').read_text())['pages']==3
    assert DOCX.stat().st_size<1_000_000
    with zipfile.ZipFile(DOCX) as z:
        xml=ET.fromstring(z.read('word/document.xml'))
        assert len(xml.findall('.//w:tbl',NS))>=7
        assert not xml.findall('.//w:drawing',NS) and not xml.findall('.//w:pict',NS)
        assert not xml.findall('.//w:documentProtection',NS)
    spec=importlib.util.spec_from_file_location('baseline_builder',ROOT/'scripts/build-archiverescue-round1.py')
    b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
    findings=b.scan_artifact('ArchiveRescue_Proposal.pdf',PDF.read_bytes())
    for p in [SOURCE,Path(__file__)]:findings+=b.scan_artifact(p.relative_to(ROOT).as_posix(),p.read_bytes())
    findings += [(DOCX.name,line,rule) for line,rule in b.scan_module().scan_text(text_docx)]
    findings += inspect_docx(DOCX.read_bytes(),b.scan_module())
    b.scan_module().show(4,findings);assert not findings
    result={'verdict':'VISUAL_V3_READY_FOR_USER_REVIEW','pdf_pages':3,'docx_pages':3,
            'pdf_bytes':PDF.stat().st_size,'docx_bytes':DOCX.stat().st_size,
            'pdf_sha256':sha(PDF.read_bytes()),'docx_sha256':sha(DOCX.read_bytes()),
            'word_render':json.loads((TMP/'word-render.json').read_text()),
            'edit_probe':json.loads((TMP/'word-edit-probe.json').read_text()),
            'counts':counts,'grid':GRID,'palette':PALETTE,'measured_geometry':measured,'secret_findings':0,
            'protected_sha256':{name:sha((BASE/name).read_bytes()) for name in PROTECTED}}
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True);EVIDENCE.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--word-worker',action='store_true');p.add_argument('--edit-probe',action='store_true');p.add_argument('--verify-only',action='store_true')
    args=p.parse_args();TMP.mkdir(parents=True,exist_ok=True)
    if args.word_worker:word_worker(args.edit_probe);return
    for name,expected in PROTECTED.items():assert sha((BASE/name).read_bytes())==expected
    qa,design,disclosure=read_source()
    if args.edit_probe:
        run_word(True)
    elif not args.verify_only:
        build_docx(qa,design,disclosure);run_word();run_word(True)
    validate(qa,design,disclosure)
    for name,expected in PROTECTED.items():assert sha((BASE/name).read_bytes())==expected


if __name__=='__main__':main()
