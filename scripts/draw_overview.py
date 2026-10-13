import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Circle
from pathlib import Path
plt.rcParams['font.family']='DejaVu Sans'
fig,ax=plt.subplots(figsize=(16,8),dpi=160);fig.patch.set_facecolor('#f3f5fa');ax.set_facecolor('#f3f5fa');ax.set_xlim(0,1600);ax.set_ylim(0,800);ax.axis('off')
ink='#182842';muted='#63748c';blue='#476be4';teal='#179c95';orange='#d78645'
def txt(x,y,s,size=14,color=ink,weight='normal',ha='left'):ax.text(x,y,s,fontsize=size,color=color,weight=weight,ha=ha,va='center')
def box(x,y,w,h,fc='white',ec='#dbe2ef',rad=20):ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={rad}',facecolor=fc,edgecolor=ec,lw=1.2))
def arrow(x,y,X,Y,c=muted):ax.add_patch(FancyArrowPatch((x,y),(X,Y),arrowstyle='-|>',mutation_scale=18,lw=2,color=c))
# Header
txt(70,741,'ROBOT LEARNING LAB',12,blue,'bold')
txt(70,681,'Learning to manipulate from offline experience',26,ink,'bold')
txt(70,629,'Goal-conditioned offline reinforcement learning · OGBench Cube Single & Double',14,muted)
# Three stages
for x,n,title,color in [(70,'01','OFFLINE EXPERIENCE',blue),(580,'02','GOAL-CONDITIONED LEARNING',teal),(1090,'03','EVALUATE & EXPLORE',orange)]:
 box(x,224,440,342);txt(x+26,528,n,13,color,'bold');txt(x+66,528,title,12,ink,'bold')
arrow(518,393,572,393);arrow(1028,393,1082,393)
# Data glyph
for i in range(3):
 box(98+i*15,423-i*17,115,52,'#edf1ff','#c6d1f6',9)
 for j in range(4):ax.plot([115+i*15+j*21,124+i*15+j*21],[444-i*17,444-i*17],color=blue,lw=3)
txt(263,459,'Recorded transitions',15,ink,'bold');txt(263,426,'states · actions · goals',12,muted)
txt(98,345,'Cube Single + Cube Double',17,ink,'bold')
txt(98,308,'1M training transitions per dataset',12,muted)
txt(98,274,'Training uses fixed offline datasets',12,blue)
# Algorithms
for y,label,detail in [(451,'GCBC','Imitation baseline'),(379,'GCIQL','Value learning + policy extraction'),(307,'HIQL','Hierarchical subgoals + low-level policy')]:
 box(608,y-25,384,54,'#eef8f6','#d2eae4',10);txt(625,y,label,13,teal,'bold');txt(720,y,detail,9,ink)
# Schematic robot/cubes
ax.plot([1138,1182,1220,1280],[424,473,450,458],color=ink,lw=9,solid_capstyle='round')
for x,y in [(1138,424),(1182,473),(1220,450)]:ax.add_patch(Circle((x,y),9,color=blue))
ax.plot([1269,1280,1291],[447,458,447],color=ink,lw=3)
ax.plot([1124,1160],[416,416],color=ink,lw=6)
for x,y,c in [(1323,424,teal),(1412,424,orange)]:
 ax.add_patch(Polygon([(x,y),(x+28,y+12),(x+55,y),(x+27,y-12)],facecolor=c,alpha=.6))
 ax.add_patch(Polygon([(x,y),(x+27,y-12),(x+27,y-43),(x,y-31)],facecolor=c))
 ax.add_patch(Polygon([(x+27,y-12),(x+55,y),(x+55,y-31),(x+27,y-43)],facecolor=c,alpha=.8))
txt(1118,342,'Fixed simulator evaluation',16,ink,'bold');txt(1118,305,'Success rates · curves · ablations',12,muted);txt(1118,269,'Interactive recorded-trajectory replay',11,orange)
# Protocol strip
box(70,104,1460,84,'#e9eef8','#e9eef8',15)
for x,b,s in [(101,'18 core runs','2 datasets × 3 methods × 3 seeds'),(625,'4,500 core episodes','5 tasks × 50 starts per run'),(1120,'Traceable evidence','Weights · episode logs · replay data')]:txt(x,157,b,16,ink,'bold');txt(x,127,s,11,muted)
txt(70,58,'Schematic overview · Short CPU-budget simulation study · Algorithms adapted from pinned OGBench implementations',10,muted)
plt.subplots_adjust(left=0,right=1,top=1,bottom=0)
root=Path(__file__).resolve().parents[1] / 'docs' / 'assets'
root.mkdir(parents=True, exist_ok=True)
fig.savefig(root/'project-overview.png',dpi=160,facecolor=fig.get_facecolor())
fig.savefig(root/'project-overview.svg',facecolor=fig.get_facecolor())
