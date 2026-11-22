import json
d=json.load(open('data/refs_raw.json'));o={}
for b,rows in d.items():
    L=[]
    for sps,tg in rows:
        flat=[x for t in tg for x in t]
        for s in sps:L.append(s+[flat])
    o[b]=L
open('data/refs.json','w').write(json.dumps(o,separators=(',',':')))
