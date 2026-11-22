import base64
def u(p,m):return f"data:{m};base64,"+base64.b64encode(open(p,'rb').read()).decode()
t=open("src/app.html",encoding="utf-8").read()
d=open("data/bible.json",encoding="utf-8").read().replace("\u2028","\\u2028").replace("\u2029","\\u2029")
r=open("data/refs.json",encoding="utf-8").read()
t=t.replace("/*HERO*/",u("img/hero-home.webp","image/webp")).replace("/*OTI*/",u("img/ot.webp","image/webp")).replace("/*NTI*/",u("img/nt.webp","image/webp")).replace("/*MARK*/",u("img/mark.png","image/png")).replace("/*FAV*/",u("img/fav.png","image/png")).replace("/*ICON*/",u("img/icon-192.png","image/png"))
open("dist/WordAliveBible.html","w",encoding="utf-8").write(t.replace("/*DATA*/",d).replace("/*REFS*/",r))
