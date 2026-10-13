"""Render a scripted 3D hierarchical-control illustration (not a policy rollout).
Dependencies: numpy, matplotlib, Pillow. Run from the project root.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]/'docs'/'assets';ROOT.mkdir(parents=True,exist_ok=True)
fig=plt.figure(figsize=(9.6,6),dpi=100,facecolor='#151b22')
ax=fig.add_axes([0,0,1,1],projection='3d',computed_zorder=False,facecolor='#151b22')
frames=[]
way=np.array([[.35,-.28,.48],[.35,-.28,.115],[.35,-.28,.115],[.35,-.28,.4],[.67,.25,.4],[.67,.25,.115],[.67,.25,.42]])
def cylinder(a,b,r,c):
 a=np.array(a);b=np.array(b);v=b-a;v=v/np.linalg.norm(v)
 u=np.cross(v,[0,0,1] if abs(v[2])<.9 else [0,1,0]);u=u/np.linalg.norm(u);w=np.cross(v,u)
 theta=np.linspace(0,2*np.pi,16);t=np.linspace(0,1,2)
 xyz=a[:,None,None]+(b-a)[:,None,None]*t[None,:,None]+r*(u[:,None,None]*np.cos(theta)[None,None,:]+w[:,None,None]*np.sin(theta)[None,None,:])
 ax.plot_surface(*xyz,color=c,shade=True,linewidth=0,antialiased=True)
def cube(pos,s,col,alpha=1):
 x,y,z=pos;vs=np.array([[x+dx*s/2,y+dy*s/2,z+dz*s/2] for dx,dy,dz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]])
 faces=[[vs[j] for j in idx] for idx in [[0,1,2,3],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]]
 ax.add_collection3d(Poly3DCollection(faces,facecolors=col,edgecolors='#20262d',linewidths=.5,alpha=alpha))
for i in range(96):
 ax.clear();ax.set_axis_off();ax.set_xlim(-.25,.95);ax.set_ylim(-.65,.65);ax.set_zlim(-.14,1);ax.set_box_aspect((1.2,1.3,1.14));ax.view_init(24,-48);ax.set_proj_type('ortho')
 st=min(i//16,5);u=(i%16)/15;t=u*u*(3-2*u);p=way[st]*(1-t)+way[st+1]*t
 # Solid desk and fine grid
 plane=[[-.2,-.62,0],[.92,-.62,0],[.92,.62,0],[-.2,.62,0]]
 ax.add_collection3d(Poly3DCollection([plane],facecolors='#343e49',edgecolors='#52606e',linewidths=1))
 for x in np.arange(-.2,.93,.1):ax.plot([x,x],[-.62,.62],[.001,.001],color='#49535e',alpha=.35,lw=.4)
 for y in np.arange(-.6,.63,.1):ax.plot([-.2,.92],[y,y],[.001,.001],color='#49535e',alpha=.35,lw=.4)
 # Target footprint and dashed vertical outline
 gx,gy=.67,.25;r=.056
 ax.plot([gx-r,gx+r,gx+r,gx-r,gx-r],[gy-r,gy-r,gy+r,gy+r,gy-r],[.004]*5,color='#94bec9',lw=1.6)
 for dx,dy in [(-r,-r),(r,-r),(r,r),(-r,r)]:ax.plot([gx+dx]*2,[gy+dy]*2,[.006,.104],color='#94bec9',ls=':',lw=.8)
 # Mechanically plausible articulated arm, schematic planar IK in target azimuth
 shoulder=np.array([-.07,0,.22]);d=p-shoulder;rho=np.linalg.norm(d[:2]);L1=.47;L2=.47
 wrist=p+np.array([0,0,.095]);dd=wrist-shoulder;rho=np.linalg.norm(dd[:2]);yaw=np.arctan2(dd[1],dd[0]);c=np.clip((rho*rho+dd[2]**2-L1*L1-L2*L2)/(2*L1*L2),-1,1)
 a2=-np.arccos(c);a1=np.arctan2(dd[2],rho)-np.arctan2(L2*np.sin(a2),L1+L2*np.cos(a2))
 elbow=shoulder+np.array([L1*np.cos(a1)*np.cos(yaw),L1*np.cos(a1)*np.sin(yaw),L1*np.sin(a1)])
 cylinder([-.07,0,0],[-.07,0,.09],.092,'#838e98');cylinder([-.07,0,.09],shoulder,.059,'#b5bcc2')
 cylinder(shoulder,elbow,.042,'#b9c0c5');cylinder(elbow,wrist,.035,'#a1acb4');cylinder(wrist,p,.033,'#737f89')
 for pos in [shoulder,elbow,wrist]:cylinder(pos-[0,.045,0],pos+[0,.045,0],.055,'#608a99')
 closed=(st in [2,3,4]) or (st==1 and t>.5);spread=.052 if closed else .084
 cylinder(p+[-spread,0,-.02],p+[spread,0,-.02],.014,'#424c55')
 for sign in [-1,1]:cylinder(p+[sign*spread,0,-.02],p+[sign*spread,0,-.088],.012,'#cad0d4')
 obj=np.array([.35,-.28,.05]) if st<2 else p-[0,0,.065] if st<5 else np.array([gx,gy,.05])
 cube(obj,.095,'#c8986c')
 # Transparent path; highlighted next geometric waypoint
 ax.plot(way[[1,3,4,5],0],way[[1,3,4,5],1],way[[1,3,4,5],2],color='#79a6a8',lw=1,ls=':',alpha=.7)
 q=way[st+1];ax.scatter(*q,s=48,facecolors='none',edgecolors='#9ac8c4',linewidths=1.3,depthshade=False)
 # Quiet annotations outside scene
 ax.text2D(.055,.925,'Hierarchical goal-conditioned control',transform=ax.transAxes,color='#e2e7eb',fontsize=15)
 ax.text2D(.055,.876,'Intermediate target  →  local motion  →  object goal',transform=ax.transAxes,color='#93a2ae',fontsize=10)
 phases=['Approach','Close gripper','Lift','Transfer','Lower','Release']
 ax.text2D(.055,.095,f'{st+1:02d} / 06   {phases[st]}',transform=ax.transAxes,color='#c4d3d9',fontsize=10)
 ax.text2D(.055,.052,'Scripted 3D illustration · not a trained-policy rollout',transform=ax.transAxes,color='#7f8d99',fontsize=8)
 fig.canvas.draw();im=Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:,:,:3]);frames.append(im.convert('P',palette=Image.Palette.ADAPTIVE,colors=128))
 if i==56:im.save(ROOT/'hiql-principle-poster.png')
frames[0].save(ROOT/'hiql-control-3d.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True)
print('Rendered 96 frames')
