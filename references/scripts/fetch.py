import json,time,urllib.request,urllib.parse,sys,os
Q={
'A_philosophy':['formal ontology philosophy','ontology metaphysics categories','philosophical ontology information systems','applied ontology realism'],
'B_definition':['ontology specification conceptualization','what is an ontology knowledge sharing','ontologies principles methods applications','ontology knowledge representation'],
'C_method':['ontology engineering methodology','ontology development methodology','ontology design patterns','ontology development 101','collaborative ontology development','ontology modularization','competency questions ontology'],
'D_language':['OWL web ontology language','description logic ontology reasoning','semantic web RDF ontology','ontology reasoner','SHACL ontology constraints','Protege ontology editor'],
'E_upper':['upper ontology','foundational ontology DOLCE','basic formal ontology BFO','unified foundational ontology UFO','SUMO upper ontology'],
'F_domain':['gene ontology','biomedical ontology OBO','ontology manufacturing industry','ontology healthcare','geospatial ontology','ontology smart city','ontology engineering domain e-commerce product'],
'G_learning':['ontology learning from text','automatic ontology construction','large language models ontology','ontology generation LLM','ontology population information extraction'],
'H_integration':['ontology matching','ontology alignment','ontology evaluation','ontology-based data integration','ontology-based data access','ontology evolution versioning'],
'I_enterprise':['enterprise ontology','knowledge graph ontology','ontology digital twin','ontology decision support','ontology business process','ontology data governance semantic layer','ontology operational','ontology military intelligence'],
}
F='title,year,citationCount,externalIds,venue,authors,publicationTypes,abstract'
out={}
if os.path.exists('raw.json'): out=json.load(open('raw.json'))
for cat,qs in Q.items():
  for q in qs:
    key=cat+'|'+q
    if key in out: continue
    for attempt in range(8):
      try:
        u='https://api.semanticscholar.org/graph/v1/paper/search?'+urllib.parse.urlencode({'query':q,'limit':100,'fields':F})
        d=json.load(urllib.request.urlopen(u,timeout=40))
        out[key]=d.get('data',[]);print(key,len(out[key]),flush=True);break
      except Exception as e:
        print('retry',key,e,flush=True);time.sleep(5*(attempt+1))
    json.dump(out,open('raw.json','w'));time.sleep(1.5)
