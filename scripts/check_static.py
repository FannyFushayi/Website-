from pathlib import Path
from lxml import html
from urllib.parse import urlsplit,unquote
import json,subprocess,re
R=Path(__file__).resolve().parents[1]
issues=[];external=set();copy_changes=[]
for p in R.glob('*.html'):
    doc=html.document_fromstring(p.read_text(encoding='utf-8'))
    if p.name!='test.html':
        for query,label in [('//h1','one H1'),('//main','one main'),('//nav[@data-shared="navigation"]','shared navigation'),('//footer[@data-shared="footer"]','shared footer'),('//meta[@name="description"]','description'),('//link[@rel="canonical"]','canonical'),('//meta[@property="og:title"]','OG title')]:
            if len(doc.xpath(query))!=1:issues.append([p.name,label,len(doc.xpath(query))])
    ids=doc.xpath('//*[@id]/@id')
    if len(ids)!=len(set(ids)):issues.append([p.name,'duplicate IDs'])
    for el in doc.xpath('//*[@href or @src]'):
        for attr in ['href','src']:
            value=el.get(attr)
            if not value:continue
            parts=urlsplit(value)
            if parts.scheme in ['https','http']:
                if attr=='href' and el.tag=='a':external.add(value)
                continue
            if parts.scheme or parts.netloc:continue
            path=unquote(parts.path).lstrip('/')
            target=R/path if path else p
            if path:
                if not target.is_file():issues.append([p.name,'missing asset',value]);continue
                # Windows exists() ignores case; verify the actual spelling too.
                current=R
                for segment in Path(path).parts:
                    if segment not in [x.name for x in current.iterdir()]:issues.append([p.name,'case mismatch',value]);break
                    current=current/segment
            if parts.fragment and target.suffix=='.html':
                other=doc if target==p else html.document_fromstring(target.read_text(encoding='utf-8'))
                if not other.xpath('//*[@id=$v or @name=$v]',v=unquote(parts.fragment)):issues.append([p.name,'missing anchor',value])
    # Compare substantive paragraph text with the repository baseline.
    result=subprocess.run(['git','show','HEAD:'+p.name],cwd=R,capture_output=True)
    if result.returncode==0:
        old=html.document_fromstring(result.stdout.decode('utf-8'))
        def paragraphs(d):return [' '.join(e.text_content().split()) for e in d.xpath('//p') if len(' '.join(e.text_content().split()))>60]
        before=paragraphs(old);after=paragraphs(doc)
        missing=[x for x in before if x not in after]
        if missing:copy_changes.append({'file':p.name,'changed_or_removed_paragraphs':missing})
report={'issues':issues,'external_links':sorted(external),'copy_changes_for_review':copy_changes}
(R/'qa'/'static-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Static issues:',len(issues),'External links:',len(external),'Pages with copy changes:',len(copy_changes))
for issue in issues:print(issue)
