import re,glob,json,sys
B=json.load(open('data/bible.json'))
idx={x['s']:i for i,x in enumerate(B)}
def norm(n):return re.sub(r'[^a-z0-9]','',n.lower())
alias={norm(x['n']):i for i,x in enumerate(B)}
alias.update({'psalm':alias['psalms'],'songofsolomon':alias['songofsongs'],'song':alias['songofsongs'],'canticles':alias['songofsongs'],'revelations':alias['revelation']})
for k in list(alias):
    if k[0].isdigit() and k[0] in '123':pass
BOOKRE=re.compile(r'^((?:[123]\s*)?[A-Za-z][A-Za-z ]*?)\s+(\d.*)$')
nch=lambda b:len(B[b]['c'])
def nv(b,c):
    ch=B[b]['c'][c-1] if 1<=c<=nch(b) else []
    return max([v for v,_ in ch]+[0])
issues=[];out={};NOTES=[]
def parse_target(seg,prev,single,srcbook):
    """returns list of [b,c1,v1,c2,v2] (v=0 means whole chapter edge) and the book used"""
    seg=re.sub(r'\s+title\b','',seg.strip().rstrip('.'))
    if re.match(r'^(1 Esdras|Epimenides|Sirach|Ecclesiasticus|Wisdom|Prayer of Manasseh|Tobit|Judith|1 Maccabees|2 Maccabees|Baruch|1 Enoch|Enoch|Jubilees)\b',seg):
        NOTES.append(seg);return [],prev
    if not seg:return [],prev
    if norm(seg) in alias:
        b0=alias[norm(seg)];return [[b0,1,0,nch(b0),0]],b0
    m=BOOKRE.match(seg)
    b=prev;rest=seg
    if m:
        nm=norm(m.group(1))
        if nm in alias:b=alias[nm];rest=m.group(2)
        elif prev is None:
            issues.append(('book?',seg));return [],prev
    elif prev is None:
        issues.append(('book?',seg));return [],prev
    # handle "X to Y" with other book e.g. "1 Kings 17 to 2 Kings 2"
    res=[]
    m2=re.match(r'^(.*?)\s+to\s+((?:[123]\s*)?[A-Za-z][A-Za-z ]*?)\s+(\d.*)$',rest)
    if m2 and norm(m2.group(2)) in alias:
        b2=alias[norm(m2.group(2))]
        a=span(b,m2.group(1).strip(),single)
        z=span(b2,m2.group(3).strip(),single)
        if a and z:
            return [[b,a[0],a[1],nch(b),0],[b2,1,0,z[2],z[3]]] if b!=b2 else [[b,a[0],a[1],z[2],z[3]]],b2
    rest=re.sub(r'\s+(?:to)\s+',' to ',rest)
    # split on ' and ' between chapter-only refs and commas for verses
    pieces=re.split(r'\s+and\s+',rest)
    # "Jeremiah 47 and 48" or "Exodus 14 and 15"
    for p in pieces:
        for sub in splitcomma(p,single):
            s=span(b,sub,single)
            if s:res.append([b,s[0],s[1],s[2],s[3]])
            else:issues.append(('span?',B[b]['n'],sub))
    return res,b
def splitcomma(p,single):
    # first part has chapter:verse; later parts "11-12" verses (carry chapter)
    parts=[x.strip() for x in p.split(',') if x.strip()]
    out=[];ctx=None
    for x in parts:
        m=re.match(r'^(\d+):',x)
        if m:ctx=m.group(1);out.append(x)
        elif ctx and not ':' in x:out.append(ctx+':'+x)
        else:out.append(x)
    return out
def span(b,s,single):
    s=s.replace('–','-').replace('–','-').strip()
    s=re.sub(r'\s+to\s+','-',s)
    m=re.match(r'^(\d+):(\d+)(?:-(\d+):(\d+))?$',s)
    if m:
        c,v=int(m.group(1)),int(m.group(2))
        if m.group(3):return (c,v,int(m.group(3)),int(m.group(4)))
        return (c,v,c,v)
    m=re.match(r'^(\d+):(\d+)-(\d+)$',s)
    if m:return (int(m.group(1)),int(m.group(2)),int(m.group(1)),int(m.group(3)))
    m=re.match(r'^(\d+)-(\d+):(\d+)$',s)  # 1-2:3? treat chapters
    if m:return (int(m.group(1)),0,int(m.group(2)),int(m.group(3)))
    m=re.match(r'^(\d+)(?:-(\d+))?$',s)
    if m:
        a=int(m.group(1));z=int(m.group(2) or a)
        if single[b] if isinstance(single,dict) else False:
            return (1,a,1,z)
        return (a,0,z,0)
    return None
def srcspan(txt,single):
    t=txt.strip().replace('–','-').replace('–','-')
    m=re.match(r'^(\d+):(\d+)(?:\s*-\s*(\d+):(\d+))?$',t)
    if m:
        c,v=int(m.group(1)),int(m.group(2))
        if m.group(3):return (c,v,int(m.group(3)),int(m.group(4)))
        return (c,v,c,v)
    m=re.match(r'^(\d+):(\d+)\s*-\s*(\d+)$',t)
    if m:return (int(m.group(1)),int(m.group(2)),int(m.group(1)),int(m.group(3)))
    m=re.match(r'^(\d+)(?:\s*-\s*(\d+))?$',t)
    if m:
        a=int(m.group(1));z=int(m.group(2) or a)
        return (1,a,1,z)
    return None
def srcmulti(txt,single):
    res=[]
    txt=re.sub(r'\s*\(.*?\)','',txt)
    for seg in txt.split(';'):
        ctx=None
        for x in splitcomma(seg.strip(),single):
            x=re.sub(r'\s+to\s+','-',x)
            m=re.match(r'^(\d+):\d+-(\d+):(\d+)$',x)
            r=srcspan(x,single)
            if r:res.append(r)
    return res
single={i:(nch(i)==1) for i in range(66)}
nrows=0;ntarg=0
for f in sorted(glob.glob('appendix-b/*.md')):
    nm=re.sub(r'^(WABV )?','',f.split('/')[-1][:-3]);nm=nm.replace('WABV ','')
    b=alias.get(norm(nm))
    if b is None:issues.append(('file',f));continue
    t=open(f,encoding='utf-8').read();i=t.find('Appendix B')
    rows=[l for l in t[i:].split('\n') if l.startswith('|') and not re.match(r'\|\s*-',l)][1:]
    lst=[]
    for l in rows:
        cells=[c.strip() for c in l.strip().strip('|').split('|')]
        if len(cells)<2:continue
        sp=srcmulti(cells[0],single)
        if not sp:
            issues.append(('src?',nm,cells[0]));
            continue
        tg=[];prev=None;del NOTES[:]
        for seg in cells[1].split(';'):
            r,prev=parse_target(seg,prev,single,b)
            tg+=r
        nrows+=1;ntarg+=len(tg)
        lst.append([[list(x) for x in sp],tg,list(NOTES)])
    out[b]=lst
json.dump(out,open('data/refs_raw.json','w'),separators=(',',':'))
print('books',len(out),'rows',nrows,'targets',ntarg,'issues',len(issues))
from collections import Counter
for k,v in Counter(issues).most_common(40):print(v,k)
