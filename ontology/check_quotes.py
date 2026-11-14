"""記入した表の引用が、本文と一字一句合っているか照合する。
使い方: python3 check_quotes.py 本文.txt template/
本文.txt は1段落1行。表の「段落」は1から数えた行番号。"""
import csv,sys,os
text=[l.rstrip('\n') for l in open(sys.argv[1],encoding='utf-8') if l.strip()]
bad=n=0
for f in sorted(os.listdir(sys.argv[2])):
    if not f.endswith('.csv'): continue
    for r in csv.DictReader(open(os.path.join(sys.argv[2],f),encoding='utf-8-sig')):
        par=r.get('段落') or r.get('傍線部の段落'); q=r.get('引用') or r.get('傍線部の引用')
        if not q: 
            if any(v for k,v in r.items() if k!='ID'): print(f'× {f} {r["ID"]}: 引用がない'); bad+=1
            continue
        n+=1
        if not par or not par.isdigit() or not 1<=int(par)<=len(text): print(f'× {f} {r["ID"]}: 段落番号が不正'); bad+=1
        elif q not in text[int(par)-1]: print(f'× {f} {r["ID"]}: 段落{par}にこの引用はない「{q}」'); bad+=1
print(f'照合 {n}件 / 問題 {bad}件'); sys.exit(1 if bad else 0)
