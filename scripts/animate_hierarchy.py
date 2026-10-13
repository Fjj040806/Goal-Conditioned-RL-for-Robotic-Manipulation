"""Conceptual HIQL animation; scripted geometry, not a trained-policy rollout.
Requires matplotlib, numpy and Pillow. Produces README GIF and poster.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, FancyArrowPatch
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]/'docs'/'assets'
ROOT.mkdir(parents=True,exist_ok=True)
ink='#1a2b45'; muted='#66768e'; teal='#149b96';blue='#5472e5';orange='#e19a55'
fig,ax=plt.subplots(figsize=(10,5.8),dpi=100)
frames=[]
# Side-view waypoints: approach, grasp, lift, transfer, place, release.
points=np.array([[3.0,2.8],[3.0,1.13],[3.0,1.13],[3.0,2.8],[6.6,2.8],[6.6,1.13],[6.6,2.8]])
labels=['APPROACH','GRASP','LIFT','TRANSFER','PLACE','RELEASE']
for i in range(120):
 ax.clear();ax.set_xlim(0,10);ax.set_ylim(0,5.8);ax.axis('off');fig.patch.set_facecolor('#f3f5fa')
 stage=min(i//20,5);t=(i%20)/19;t=t*t*(3-2*t);p=points[stage]*(1-t)+points[stage+1]*t
 def text(x,y,s,size=12,c=ink,bold=False):ax.text(x,y,s,fontsize=size,color=c,weight='bold' if bold else 'normal',va='center')
 def box(x,y,w,h,fc,ec=None):ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.1',fc=fc,ec=ec or fc))
 text(.4,5.43,'HIQL: a distant goal becomes a sequence of reachable subgoals',17,ink,True)
 text(.4,5.06,'High-level policy chooses where to go; low-level policy chooses the next action.',11,muted)
 box(.4,4.12,9.2,.58,'#e5ebfb')
 text(.6,4.42,'FINAL GOAL',10,blue,True);text(2.1,4.42,'Place the cube at the target',12)
 text(6.42,4.42,'SUBGOAL',10,teal,True);text(7.65,4.42,labels[stage],11,teal,True)
 # Workbench
 ax.plot([.5,8.0],[.7,.7],color='#bdc8d9',lw=4);text(.6,.43,'Recorded experience → learned goal-conditioned policies',10,muted)
 ax.add_patch(Rectangle((6.3,.78),.6,.65,fill=False,ec=blue,lw=2,ls='--'))
 text(6.1,1.64,'Target object pose',10,blue)
 # subgoal trace
 ax.plot([3,3,6.6,6.6],[1.13,2.8,2.8,1.13],ls=':',color='#acbebc',lw=2)
 q=points[stage+1];ax.add_patch(Circle(q,.19,fc='none',ec=teal,lw=2))
 text(q[0]-.65,q[1]+.42,'Current subgoal',10,teal)
 # Arm planar inverse kinematics (schematic, not UR5 kinematics)
 base=np.array([1.2,.86]);d=p-base;L1=2.85;L2=2.85
 cos2=np.clip((np.dot(d,d)-L1*L1-L2*L2)/(2*L1*L2),-1,1)
 th2=-np.arccos(cos2);th1=np.arctan2(d[1],d[0])-np.arctan2(L2*np.sin(th2),L1+L2*np.cos(th2))
 elbow=base+L1*np.array([np.cos(th1),np.sin(th1)])
 ax.plot([base[0],elbow[0],p[0]],[base[1],elbow[1],p[1]],color=ink,lw=11,solid_capstyle='round')
 for v in [base,elbow]:ax.add_patch(Circle(v,.105,fc=blue,ec='white',lw=1))
 ax.add_patch(Rectangle((.9,.73),.6,.12,fc=ink))
 closed=stage in [2,3,4] or (stage==1 and t>.5)
 spread=.12 if closed else .25
 ax.plot([p[0]-spread,p[0]-spread,p[0]+spread,p[0]+spread],[p[1]-.24,p[1],p[1],p[1]-.24],color=ink,lw=2)
 if stage<2:cube=np.array([3.,.93])
 elif stage<5:cube=p+np.array([0,-.2])
 else:cube=np.array([6.6,.93])
 ax.add_patch(Rectangle((cube[0]-.16,cube[1]-.16),.32,.32,fc=orange,ec='#b5783f',lw=1))
 # small low-level command arrow at tool
 v=q-p
 if np.linalg.norm(v)>.1:
  v=v/np.linalg.norm(v)*.44
  ax.add_patch(FancyArrowPatch(p+np.array([.3,0]),p+np.array([.3,0])+v,arrowstyle='-|>',mutation_scale=14,color=orange,lw=2))
 # right inset
 box(8.15,1.04,1.42,2.65,'white','#d8e0eb')
 text(8.32,3.41,'LOW LEVEL',10,orange,True)
 for j,s in enumerate(['Observe state','+ subgoal','↓','Small action','↓','Observe again']):text(8.3,3.02-j*.27,s,9,muted)
 for j in range(6):
  x=.65+j*1.43;box(x,.05,1.25,.18,teal if j==stage else '#d7e0eb')
 text(.4,-.25,'',8)
 # explicit honesty label in top margin of bottom area
 text(.65,3.85,'SCRIPTED PRINCIPLE DEMO · not a trained-policy rollout',9,muted)
 fig.subplots_adjust(0,0,1,1);fig.canvas.draw()
 img=Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:,:,:3]).convert('P',palette=Image.Palette.ADAPTIVE,colors=128)
 frames.append(img)
frames[65].convert('RGB').save(ROOT/'hiql-principle-poster.png')
frames[0].save(ROOT/'hiql-principle.gif',save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=True)
print(ROOT/'hiql-principle.gif')
