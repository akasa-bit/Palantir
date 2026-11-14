import json,time,urllib.request,urllib.parse,os
exec(open('fetch.py').read().split("F='")[0])  # reuse Q
out={}
if os.path.exists('cr.json'): out=json.load(open('cr.json'))
for cat,qs in Q.items():
  for q in qs:
    key=cat+'|'+q
    if key in out: continue
    for a in range(5):
      try:
        u='https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':q,'rows':150,'select':'DOI,title,author,issued,container-title,type,is-referenced-by-count,abstract,publisher'})
        out[key]=json.load(urllib.request.urlopen(u,timeout=60))['message']['items'];print(key,len(out[key]),flush=True);break
      except Exception as e: print('retry',key,e,flush=True);time.sleep(4*(a+1))
    json.dump(out,open('cr.json','w'))
