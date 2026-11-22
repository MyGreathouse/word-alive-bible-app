import os,zipfile
os.makedirs('dist',exist_ok=True)
t=open('dist/WordAliveBible.html',encoding='utf-8').read()
head='<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<link rel="manifest" href="manifest.webmanifest">\n<meta name="theme-color" content="#0e1424">\n'
t=t.replace('<meta name="claude:viewport-fit-sides" content="cover">',head,1)
t=t.replace('applyMode();fromHash();',"applyMode();fromHash();if('serviceWorker' in navigator&&location.protocol.indexOf('http')===0)navigator.serviceWorker.register('sw.js').catch(function(){});",1)
z=zipfile.ZipFile('dist/WordAliveBible-deploy.zip','w',zipfile.ZIP_DEFLATED)
z.writestr('index.html',t)
for r,_,fs in os.walk('deploy'):
    for f in fs:
        p=os.path.join(r,f);z.write(p,os.path.relpath(p,'deploy'))
z.close()

# refresh the Cloudflare site folder
import shutil
shutil.rmtree('site',ignore_errors=True)
zipfile.ZipFile('dist/WordAliveBible-deploy.zip').extractall('site')
open('site/_headers','w').write('/index.html\n  Cache-Control: no-cache\n/sw.js\n  Cache-Control: no-cache\n/manifest.webmanifest\n  Cache-Control: no-cache\n/icons/*\n  Cache-Control: public, max-age=31536000, immutable\n')
