"""Refresh static shared navigation, footer, metadata and article information.

Run with Python + lxml. No runtime dependencies or build step needed for hosting.
"""
from pathlib import Path
from lxml import html, etree
from urllib.parse import unquote, urlsplit, quote
import json, re, time
from PIL import Image
R=Path(__file__).resolve().parents[1]
catalog=json.loads((R/'writing-index.json').read_text(encoding='utf-8'))
lookup={p['url']:p for p in catalog}
NAV=[('index.html','Home'),('Projects.html','Projects'),('about.html','About'),('blog.html','Writing'),('Contact.html','Contact')]
PROJECTS={'project-hess.html','Project-PV.html','Project-MDPS.html','robot-car.html','Battery_Data_driven.html','emegence_anal.html','Financial.html','ML.html','BuildingAI.html','HNEI_and_ML_BD2.html','industrial-reject-control.html','edge-plc-data.html','industrial-digital-twin.html','plc-scada-upgrade.html'}
def fragment(s): return html.fragments_fromstring(s)[0]
def remove(el):
    if el.getparent() is not None: el.getparent().remove(el)
def text(el): return ' '.join(el.text_content().split())
def active(name):
    if name in PROJECTS: return 'Projects.html'
    if name in lookup: return 'blog.html'
    return name
for file in sorted(R.glob('*.html')):
    if file.name=='test.html':continue
    name=file.name; source=file.read_text(encoding='utf-8'); doc=html.document_fromstring(source)
    doc.set('lang','en');head=doc.find('head');body=doc.find('body')
    if head is None or body is None: continue
    # Remove only generated elements on rebuild.
    for el in doc.xpath('//*[@data-shared]'): remove(el)
    for el in head.xpath('./link[@rel="stylesheet" and (@href="/site.css" or @href="site.css")]'):remove(el)
    if not name in {'index.html','blog.html'}:
        for el in head.xpath('./link[contains(@href,"fonts.googleapis.com") and not(contains(@href,"Barlow"))]'):remove(el)
        for style in head.xpath('./style'):
            css=re.sub(r'@import\s+url\([^)]*\)\s*;','',style.text or '')
            css=re.sub(r'^\s*[0-9][^\n]*display=swap[\'\"]?\);','',css)
            style.text=css
    for el in body.xpath('.//html[not(.//text()[normalize-space()])]'): remove(el)
    for el in body.xpath('./nav | ./footer | .//div[@class="footer"]'): remove(el)
    for el in body.xpath('./a[@class="skip"]'):remove(el)
    # Existing page-specific interactions and diagrams stay in the document.
    landing=name in {'index.html','blog.html'}
    classes=set(body.get('class','').split());classes.add('site');classes.add('landing' if landing else 'inner-page')
    if name in lookup and name not in PROJECTS:classes.add('article-page')
    if name in PROJECTS:classes.add('case-study')
    body.set('class',' '.join(sorted(classes)))
    if not landing:
        mains=body.xpath('./main')
        if mains:
            main=mains[0];main.set('id','main')
            # Move standalone legacy title headers inside the reading layout.
            for el in list(body):
                if el.tag=='header':remove(el);main.insert(0,el)
        else:
            main=etree.Element('main',id='main')
            for el in list(body):
                if el.tag not in {'script','style'}:remove(el);main.append(el)
            body.insert(0,main)
        # Legacy pages sometimes have broad wrapper widths. Scope the reading body.
        main.set('class',' '.join(sorted(set(main.get('class','').split())|{'reading-layout'})))
        h1s=main.xpath('.//h1')
        for h in h1s[1:]:h.tag='h2'
        if not h1s:
            h=etree.Element('h1');h.text=text(head.find('title')) if head.find('title') is not None else name;main.insert(0,h)
        if name in lookup:
            p=lookup[name]
            clean=re.sub(r'<(script|style)\b.*?</\1>','',html.tostring(main,encoding='unicode'),flags=re.S)
            words=len(re.sub('<[^>]+>',' ',clean).split());minutes=max(1,round(words/220))
            info=fragment(f'<p data-shared="article-meta" class="article-meta">{p["category"]} · {minutes} min read <span> / <a href="blog.html">Back to Writing</a></span></p>')
            main.insert(0,info)
            idx=catalog.index(p);links='<a href="blog.html">All writing ↑</a>'
            if idx>0:prev=catalog[idx-1];links+=f'<a href="{prev["url"]}">← {prev["title"]}</a>'
            if idx<len(catalog)-1:nxt=catalog[idx+1];links+=f'<a href="{nxt["url"]}">{nxt["title"]} →</a>'
            main.append(fragment('<nav data-shared="article-pagination" class="article-pagination" aria-label="More writing">'+links+'</nav>'))
        elif name in PROJECTS:
            main.insert(0,fragment('<p data-shared="project-back" class="article-meta"><a href="Projects.html">← All projects</a></p>'))
    # Shared static shell works without JavaScript.
    nav=''.join(f'<a href="/{url}"'+(' aria-current="page"' if active(name)==url else '')+f'>{label}</a>' for url,label in NAV)
    body.insert(0,fragment('<a class="skip" data-shared="skip" href="#main">Skip to content</a>'))
    body.insert(1,fragment('<nav class="nav site-nav" data-shared="navigation" aria-label="Main navigation"><div class="nav-inner"><a class="brand" href="index.html">FANNY FUSHAYI</a><button class="menu" aria-controls="site-links" aria-expanded="false" type="button">Menu</button><div class="nav-links" id="site-links">'+nav+'</div></div></nav>'))
    body.append(fragment('<footer class="site-footer" data-shared="footer"><div class="shell footer-inner"><div><span>Fanny Fushayi</span><p>Engineering for the physical world.</p></div><nav aria-label="Footer navigation">'+nav+'</nav><div><a href="https://github.com/FannyFushayi">GitHub ↗</a> · <a href="https://www.linkedin.com/in/fanny-fushayi-529880235">LinkedIn ↗</a><p>© <span id="year">2026</span> Fanny Fushayi</p></div></div></footer>'))
    body.append(fragment('<script data-shared="script" src="/site.js" defer></script>'))
    # Metadata uses existing title and descriptive content, never fabricated dates.
    title=head.find('title')
    if title is None:title=etree.SubElement(head,'title');title.text=name.replace('.html','')+' | Fanny Fushayi'
    if 'Fanny' not in text(title):title.text=text(title)+' | Fanny Fushayi'
    descriptions=head.xpath('./meta[@name="description"]')
    if descriptions:description=descriptions[0].get('content','')
    else:
        paras=body.xpath('.//main//p[not(@class="article-meta") and not(@class="overline")]')
        description=next((text(p)[:160] for p in paras if len(text(p))>45),text(title))
        etree.SubElement(head,'meta',name='description',content=description)
    for el in head.xpath('./link[@rel="canonical"] | ./meta[starts-with(@property,"og:")] | ./meta[@name="twitter:card"]'):remove(el)
    url='https://fushayifanny.co.za/'+('' if name=='index.html' else quote(name))
    etree.SubElement(head,'link',rel='canonical',href=url)
    for key,val in [('og:title',text(title)),('og:description',description),('og:url',url),('og:type','article' if name in lookup else 'website'),('og:image','https://fushayifanny.co.za/Images/Photo.png')]:etree.SubElement(head,'meta',property=key,content=val)
    etree.SubElement(head,'meta',name='twitter:card',content='summary_large_image')
    if not head.xpath('./meta[@name="viewport"]'):etree.SubElement(head,'meta',name='viewport',content='width=device-width, initial-scale=1')
    if not head.xpath('./link[@rel="icon"]'):etree.SubElement(head,'link',rel='icon',href='/Images/favicon.ico')
    etree.SubElement(head,'link',rel='stylesheet',href='/site.css',attrib={'data-shared':'styles'})
    if not landing and not head.xpath('./link[contains(@href,"Barlow")]'):
        etree.SubElement(head,'link',rel='stylesheet',href='https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700&display=swap',attrib={'data-shared':'fonts'})
    # Fix exact-case local URLs for case-sensitive static hosting.
    for el in doc.xpath('//*[@href or @src]'):
        for attr in ['href','src']:
            value=el.get(attr)
            if not value:continue
            value=value.replace('\\','/');parts=urlsplit(value)
            if not parts.scheme and not parts.netloc and parts.path:
                path=unquote(parts.path).lstrip('/');target=R/path
                if target.exists():
                    current=R;segments=[]
                    for segment in Path(path).parts:
                        actual=next((f.name for f in current.iterdir() if f.name.lower()==segment.lower()),segment)
                        segments.append(actual);current=current/actual
                    corrected='/'.join(segments)
                    value=('/' if value.startswith('/') else '')+quote(corrected,safe='/')+('?' + parts.query if parts.query else '')+('#'+parts.fragment if parts.fragment else '')
            el.set(attr,value)
        if el.get('target')=='_blank':el.set('rel','noopener noreferrer')
    for img in doc.xpath('//img[@src]'):
        p=R/unquote(img.get('src')).lstrip('/')
        if p.exists():
            try:
                with Image.open(p) as im:w,h=im.size
                img.set('width',str(w));img.set('height',str(h));img.set('decoding','async')
            except Exception:pass
        if img.get('alt') is None:img.set('alt','')
        if not landing and img.get('loading') is None:img.set('loading','lazy')
    output=html.tostring(doc,encoding='unicode',method='html',doctype='<!doctype html>')
    output=output.replace('Saftey','Safety').replace('colaborative','collaborative').replace('MAze Navigating','Maze-Navigating').replace('href="index.html">FANNY','href="/index.html">FANNY')
    output='\n'.join(line.rstrip() for line in output.splitlines())+'\n'
    for attempt in range(5):
        try:
            file.write_text(output,encoding='utf-8',newline='\n');break
        except OSError:
            if attempt==4:raise
            time.sleep(.3)
print('Shared static templates refreshed.')
