import json,re,collections,html
cr=json.load(open('cr.json')); cl=json.load(open('classics_raw.json'))
CATS={'A':('A_philosophy','哲学の存在論',40),'B':('B_definition','定義と基礎理論',45),'C':('C_method','構築の方法論',70),
'D':('D_language','記述言語と推論',55),'E':('E_upper','上位オントロジー',40),'F':('F_domain','分野別の応用',65),
'G':('G_learning','自動構築とLLM',60),'H':('H_integration','統合・対応付け・評価',60),'I':('I_enterprise','企業・ナレッジグラフ・デジタルツイン',65)}
assert sum(v[2] for v in CATS.values())==500
BADTYPE={'journal-issue','book-series','component','peer-review','other','dataset','report-component','standard','book-set'}
def norm(t): return re.sub(r'[^a-z0-9]','',t.lower())
def clean(t): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',t))).strip()
def rec(it,cat,classic=False):
  t=clean((it.get('title') or [''])[0]); y=(it.get('issued',{}).get('date-parts') or [[None]])[0][0]
  au=[(a.get('family') or a.get('name') or '').strip()+((' '+a['given']) if a.get('given') else '') for a in it.get('author',[])]
  return dict(cat=cat,title=t,year=y,authors=[a for a in au if a.strip()],venue=clean((it.get('container-title') or [''])[0]) or it.get('publisher',''),
    type=it.get('type'),cites=it.get('is-referenced-by-count',0),doi=it['DOI'],url='https://doi.org/'+it['DOI'],classic=classic)

RULES=[('A',r'^historical ontology$|metaphysic|realism|philosoph|process ontology|thing ontology'),('E',r'upper ontolog|foundational ontolog|top-level|\bbfo\b|basic formal ontology|dolce|\bufo\b|\bsumo\b|reference ontology'),
('G',r'learning|language model|\bllms?\b|gpt|extraction|population|generat|automatic|automated|text mining|neural|deep|embedding|machine learning'),
('H',r'matching|alignment|mapping|integrat|data access|evaluat|quality|pitfall|evolution|versioning|interoperab|merg'),
('D',r'\bowl\b|\brdf|description logic|reason|sparql|shacl|prot[eé]g[eé]|semantic web|ontology language|rules?\b'),
('I',r'enterprise|knowledge graph|digital twin|business|decision|organi[sz]ation|governance|military|intelligence|supply chain|operation|industry 4|smart factory'),
('C',r'methodolog|design pattern|engineering|development|modular|competency|collaborative|building|construct'),
('A',r'historical ontology|philosoph|realism|metaphysic|formal ontology|categor|reality|existence|being'),
('F',r'gene|biomedic|disease|clinical|health|medic|manufactur|geo|city|anatomy|protein|agricult|energy|building information|bim\b|product|legal|education')]
BAN=r'quantum|epistemolog|relational ontology|political ontology|social ontology|ontological security|ontological turn|research paradigm|qualitative|indigenous|theolog|heidegger|deleuze|ontological argument|music|literary|anthropolog'
def classify(t,fallback):
  tl=t.lower()
  for c,p in RULES:
    if re.search(p,tl): return c
  return fallback
pool={}; votes=collections.defaultdict(collections.Counter)
for k,v in cr.items():
  c=k[0]
  for it in v:
    t=clean((it.get('title') or [''])[0])
    if 'ontolog' not in t.lower() or re.search(BAN,t.lower()) or it.get('type') in BADTYPE or len(t)<8: continue
    r=rec(it,c)
    if not r['year'] or not r['authors'] or r['year']>2026: continue
    n=norm(t); votes[n][c]+=1
    if n not in pool or r['cites']>pool[n]['cites']: pool[n]=r
for n,r in pool.items(): r['cat']=classify(r['title'],votes[n].most_common(1)[0][0])
# classics (verified Crossref hits chosen by index)
PICK=[(0,0,'B'),(1,0,'B'),(2,0,'B'),(5,0,'B'),(6,1,'B'),(7,0,'A'),(11,0,'C'),(12,1,'C'),(13,1,'B'),(10,1,'D'),(14,0,'D'),(16,0,'D'),(17,1,'D'),(18,0,'D'),
 (19,0,'E'),(20,2,'E'),(22,0,'F'),(21,2,'F'),(23,0,'G'),(24,0,'H'),(24,2,'H'),(25,0,'H'),(28,0,'I'),(27,0,'I'),(29,1,'I')]
classics=[]
for qi,ii,c in PICK:
  r=rec(cl[qi][2][ii],c,True); classics.append(r); pool.pop(norm(r['title']),None)
# grey literature (URLs checked 200)
G=[('I','Ontology building: Overview','Palantir Technologies','https://www.palantir.com/docs/foundry/ontology/overview/'),
('I','Core concepts (Ontology)','Palantir Technologies','https://www.palantir.com/docs/foundry/ontology/core-concepts/'),
('I','Why create an Ontology?','Palantir Technologies','https://www.palantir.com/docs/foundry/ontology/why-ontology/'),
('I','Object types: Overview','Palantir Technologies','https://www.palantir.com/docs/foundry/object-link-types/object-types-overview/'),
('I','Link types: Overview','Palantir Technologies','https://www.palantir.com/docs/foundry/object-link-types/link-types-overview/'),
('I','Action types: Overview','Palantir Technologies','https://www.palantir.com/docs/foundry/action-types/overview/'),
('D','OWL 2 Web Ontology Language Document Overview (Second Edition)','W3C','https://www.w3.org/TR/owl2-overview/'),
('D','RDF 1.1 Concepts and Abstract Syntax','W3C','https://www.w3.org/TR/rdf11-concepts/'),
('D','Shapes Constraint Language (SHACL)','W3C','https://www.w3.org/TR/shacl/'),
('C','Ontology Development 101: A Guide to Creating Your First Ontology','Noy N.F., McGuinness D.L. (Stanford KSL)','https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html')]
YEAR={'Ontology Development 101: A Guide to Creating Your First Ontology':2001,'OWL 2 Web Ontology Language Document Overview (Second Edition)':2012,'RDF 1.1 Concepts and Abstract Syntax':2014,'Shapes Constraint Language (SHACL)':2017}
grey=[dict(cat=c,title=t,year=YEAR.get(t),authors=[a],venue='Web文書',type='web',cites=None,doi=None,url=u,classic=True) for c,t,a,u in G]
out=[]
for c,(_,lab,q) in CATS.items():
  fixed=[r for r in classics+grey if r['cat']==c]; need=q-len(fixed)
  cand=[r for r in pool.values() if r['cat']==c]
  go=0; chosen=[]
  def ok(r):
    global go
    if 'gene ontology' in r['title'].lower():
      if go>=6: return False
    return True
  byc=sorted(cand,key=lambda r:-r['cites'])
  rec_=sorted([r for r in cand if r['year']>=2021 and r['cites']>=5],key=lambda r:-r['cites']/max(1,2026.9-r['year']))
  nrec=round(need*0.3)
  for src,lim in ((byc,need-nrec),(rec_,need)):
    for r in src:
      if len(chosen)>=lim: break
      if r in chosen or not ok(r): continue
      if 'gene ontology' in r['title'].lower(): go+=1
      chosen.append(r)
  out+=fixed+chosen
have={norm(r['title']) for r in out}
rest=sorted([r for n,r in pool.items() if n not in have],key=lambda r:-r['cites'])
gc=sum('gene ontology' in r['title'].lower() for r in out)
for r in rest:
  if len(out)>=500: break
  if 'gene ontology' in r['title'].lower(): continue
  out.append(r)
order='ABCDEFGHI'; out.sort(key=lambda r:(order.index(r['cat']),not r['classic'],-(r['cites'] or 0)))
for i,r in enumerate(out): r['id']=i+1
json.dump(out,open('refs.json','w'),ensure_ascii=False)
print(len(out),len({norm(r['title']) for r in out}),collections.Counter(r['cat'] for r in out))
print('years',min(r['year'] for r in out if r['year']),max(r['year'] for r in out if r['year']),'recent>=2021',sum(1 for r in out if (r['year'] or 0)>=2021))
for c in CATS:
  rs=[r for r in out if r['cat']==c]; print('\n##',c,CATS[c][1])
  for r in rs[:4]+rs[-3:]: print(' ',r['cites'],r['year'],r['title'][:85])
