from pathlib import Path
import re, json
from urllib.parse import unquote, urlsplit
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
def text(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()

def audit():
    inventory, broken, claims = [], [], []
    for p in sorted(ROOT.glob('*.html')):
        s = p.read_text(encoding='utf-8')
        inventory.append({'file':p.name, 'title':text(' '.join(re.findall(r'<title>(.*?)</title>',s,re.S))), 'headings':[text(x) for x in re.findall(r'<h[12][^>]*>(.*?)</h[12]>',s,re.S)], 'inline_styles':len(re.findall(r'<style',s)), 'scripts':len(re.findall(r'<script',s)), 'bytes':p.stat().st_size})
        doc=html.document_fromstring(s)
        references=[(attr,el.get(attr)) for el in doc.xpath('//*[@href or @src]') for attr in ['href','src'] if el.get(attr)]
        for attr, value in references:
            url=urlsplit(value)
            if url.scheme or url.netloc or not url.path: continue
            target=ROOT / unquote(url.path).lstrip('/')
            if not target.exists(): broken.append({'file':p.name,'attribute':attr,'target':value})
        body=re.sub(r'<(style|script)\b.*?</\1>', '', s, flags=re.S)
        for line in body.splitlines():
            if re.search(r'\d+(?:\.\d+)?\s*%|\b(?:accuracy|lifespan|improvement|efficiency)\b',text(line),re.I):
                claims.append({'file':p.name,'claim':text(line)[:500]})
    return {'pages':inventory,'broken_local_references':broken,'quantitative_claims_for_review':claims}
if __name__=='__main__':
    output=ROOT/'site-audit.json'
    output.write_text(json.dumps(audit(),ensure_ascii=False,indent=2),encoding='utf-8')
    print('Audit written:',output.name)
