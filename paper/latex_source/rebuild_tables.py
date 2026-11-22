"""Rebuild all printed table cells from CSV, preserving the approved layout."""
from pathlib import Path
import csv,json,re
B=Path(__file__).resolve().parent
def esc(s):
 d={'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}'}
 s=''.join(d.get(c,c) for c in str(s))
 for a,b in {'–':'--','—':'---','−':'$-$','Δ':r'$\Delta$','ρ':r'$\rho$','₁':r'$_1$','²':r'$^2$','≥':r'$\geq$','≤':r'$\leq$','×':r'$\times$','†':r'$\dagger$'}.items():s=s.replace(a,b)
 return s
def val(s):
 if re.fullmatch(r'[+-]?\d+\.\d+(?:e[+-]?\d+)?',s):
  x=float(s)
  if 0<x<1e-8:return '<0.00000001'
  if 1e-8<=abs(x)<1e-4:return f'{x:.8f}'
  return f'{x:.4f}'
 return s
def main():
 count=0
 for p in sorted((B/'tables').glob('*.template.json')):
  spec=json.loads(p.read_text(encoding='utf8'));cp=p.with_name(p.name.replace('.template.json','.csv'));rows=list(csv.reader(cp.open(encoding='utf8')));out=spec['prefix']
  out+=' & '.join(r'\textbf{'+esc(s)+'}' for s in rows[0])+r'\\\midrule'+'\n'
  assert len(spec['citation_keys'])==len(rows)-1
  for row,key in zip(rows[1:],spec['citation_keys']):
   cells=[esc(val(s)) for s in row]
   if key:cells[0]=re.sub(r'^\[\d+\]',lambda m:r'\cite{'+key+'}',cells[0])
   out+='{}'+' & '.join(cells)+r'\\'+'\n'
  out+=spec['suffix'];cp.with_suffix('.tex').write_text(out,encoding='utf8');count+=1
 print(f'Rebuilt {count} tables from CSV; no experiments run.')
if __name__=='__main__':main()
