"""Coordinate-accurate reference guides only. Final assets must use image_gen."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Arc
ROOT=Path(__file__).resolve().parent
RAW=ROOT/'raw'
RAW.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'serif','mathtext.fontset':'stix','font.size':18})
def setup(limits,equal=False):
    fig,ax=plt.subplots(figsize=(8,5.5),dpi=200)
    ax.set_xlim(*limits[:2]);ax.set_ylim(*limits[2:]);ax.axis('off')
    if equal: ax.set_aspect('equal')
    return fig,ax
def line(ax,x,y,dashed=False):ax.plot(x,y,color='black',lw=1.2,ls=(0,(4,4)) if dashed else '-')
def text(ax,x,y,s,**kw):ax.text(x,y,s,**kw)
def dot(ax,x,y):ax.scatter([x],[y],s=42,c='black',zorder=5)
def axes(ax,xmax,ymax,xmin=0,ymin=0):
    ax.annotate('',xy=(xmax,0),xytext=(xmin,0),arrowprops={'arrowstyle':'-|>','lw':1,'color':'black'})
    ax.annotate('',xy=(0,ymax),xytext=(0,ymin),arrowprops={'arrowstyle':'-|>','lw':1,'color':'black'})
    text(ax,xmax,-.12,r'$x$',va='top');text(ax,-.08,ymax,r'$y$',ha='right')
    text(ax,-.08,-.12,'O',ha='right',va='top')
def save(fig,id):fig.savefig(RAW/(id+'_guide.png'),bbox_inches='tight',pad_inches=.08,facecolor='white');plt.close(fig)
fig,ax=setup((-.35,3.85,-1.7,5.7));axes(ax,3.62,5.55,-.15,-1.4)
x=np.linspace(-.15,np.pi+.25,1600);line(ax,x,3*np.cos(2*x)+2)
line(ax,[-.15,3.55],[2,2],True);line(ax,[np.pi/4]*2,[0,2],True)
text(ax,np.pi/4,-.23,r'$\frac{\pi}{4}$',ha='center',va='top');text(ax,3.57,2.04,r'$y=2$');text(ax,3.12,4.45,r'$y=f(x)$');save(fig,'fig_c09')
fig,ax=setup((-.55,5.5,-.5,5.2));axes(ax,4.85,5,-.3,-.25)
x=np.linspace(0,4,1000);curve=-x*x+4*x;m=4-np.cbrt(16);cross=4-m
ax.fill_between(x,0,np.minimum(curve,m*x),color='#BFBFBF');xx=np.linspace(0,cross,600);ax.fill_between(xx,m*xx,-xx*xx+4*xx,color='#D9D9D9')
line(ax,x,curve);line(ax,[0,3.2],[0,m*3.2]);text(ax,3.65,2.55,r'$y=-x^2+4x$');text(ax,3.18,4.82,r'$y=mx$');text(ax,4,-.2,'4',ha='center',va='top');save(fig,'fig_c10')
fig,ax=setup((-1.1,18,-2.3,4.8));axes(ax,15.5,4.5,-.6,-1.9)
x=np.linspace(.25,14,1200);line(ax,x,np.log2(x));x=np.linspace(4.1,14,1200);line(ax,x,np.log2(x-4))
ax.add_patch(Polygon([[8,3],[8,2],[12,3]],color='#D9D9D9'));line(ax,[8,8],[-.5,4]);line(ax,[8,12,8],[3,3,2])
for xx,yy,n,dx,dy in [(8,3,'A',-.65,.16),(8,2,'B',-.65,-.25),(12,3,'C',.1,.18)]:dot(ax,xx,yy);text(ax,xx+dx,yy+dy,n)
text(ax,8,4.15,r'$x=k$',ha='center');text(ax,14.1,3.83,r'$y=\log_2 x$');text(ax,14.1,3.05,r'$y=\log_2(x-4)$');save(fig,'fig_c13')
fig,ax=setup((-.65,7,-3,4.65),True);ax.add_patch(Circle((3.162,.816),3.266,fill=False,ec='black',lw=1.2));line(ax,[1.581,0,6.325,1.581],[3.674,0,0,3.674])
for xx,yy,n,dx,dy in [(1.581,3.674,'A',-.26,.4),(0,0,'B',-.5,-.12),(6.325,0,'C',.25,-.12)]:dot(ax,xx,yy);text(ax,xx+dx,yy+dy,n)
save(fig,'fig_c14')
fig,ax=setup((-.45,5.3,-1.2,1.95));axes(ax,4.85,1.8,-.3,-1.05)
x=np.linspace(.35,4.2,1000);line(ax,x,np.log(x));line(ax,[-.3,4.2],[-.3/np.e,4.2/np.e])
x=np.linspace(0,1,300);ax.fill_between(x,0,x/np.e,color='#D9D9D9');x=np.linspace(1,np.e,500);ax.fill_between(x,np.log(x),x/np.e,color='#D9D9D9')
dot(ax,np.e,1);line(ax,[np.e]*2,[0,1],True);text(ax,np.e,-.13,r'$e$',ha='center',va='top');text(ax,1,-.13,'1',ha='center',va='top');text(ax,4.18,1.23,r'$y=\ln x$');save(fig,'fig_m27')
fig,ax=setup((-.2,1.22,-.16,1.2),True);O=np.array([0.,0.]);A=np.array([1.,0.]);B=np.array([0.,1.]);P=np.array([np.sqrt(3)/2,.5]);Q=np.array([0.,.5]);R=np.array([.75,np.sqrt(3)/4]);t=np.linspace(0,np.pi/2,500)
line(ax,np.cos(t),np.sin(t));line(ax,[0,1],[0,0]);line(ax,[0,0],[0,1]);
t=np.linspace(0,np.pi/6,200);ax.add_patch(Polygon(np.vstack([A,np.column_stack([np.cos(t),np.sin(t)]),P]),color='#D9D9D9'));ax.add_patch(Polygon([P,Q,R],color='#BFBFBF'))
for u,v in [(O,P),(P,Q),(A,R),(Q,R),(P,A)]:line(ax,[u[0],v[0]],[u[1],v[1]])
line(ax,[0,.035,.035],[.465,.465,.5]);u=P/np.linalg.norm(P);v=np.array([.5,-np.sqrt(3)/2]);corner=R+.035*u+.035*v;line(ax,[*(R+.035*u)[0:1],corner[0],(R+.035*v)[0]],[(R+.035*u)[1],corner[1],(R+.035*v)[1]])
ax.add_patch(Arc((0,0),.3,.3,theta1=0,theta2=30,lw=1));text(ax,.17,.035,r'$\theta$')
for pt,n,offset in [(O,'O',(-.085,-.08)),(A,'A',(.035,-.065)),(B,'B',(-.065,.04)),(P,'P',(.035,.035)),(Q,'Q',(-.095,-.015)),(R,'R',(-.03,-.11))]:dot(ax,*pt);text(ax,*(pt+offset),n)
save(fig,'fig_m29')
fig,ax=setup((-5,5,-3.5,3.6),True);axes(ax,4.8,3.35,-4.7,-3.15);t=np.linspace(0,2*np.pi,1000);line(ax,4*np.cos(t),np.sqrt(7)*np.sin(t));P=(4/3,np.sqrt(7*(1-(1/3)**2)))
for f,n in [(3,'F'),(-3,"F′")]:line(ax,[f,P[0]],[0,P[1]]);dot(ax,f,0);text(ax,f,-.18,n,ha='center',va='top')
dot(ax,*P);text(ax,P[0]+.14,P[1]+.12,'P');save(fig,'fig_g26')
fig,ax=setup((-.6,4.3,-.6,4.3),True)
pts={'A':np.array([0.,2.5]),'B':np.array([2.5,2.5]),'C':np.array([3.7,3.7]),'D':np.array([1.2,3.7]),'E':np.array([0.,0.]),'F':np.array([2.5,0.]),'G':np.array([3.7,1.2]),'H':np.array([1.2,1.2])}
for pair in ['AB','BC','CD','DA','AE','BF','CG','EF','FG','GH','HE','DH','AG','EG']:
    u,v=[pts[n] for n in pair];line(ax,[u[0],v[0]],[u[1],v[1]],pair in ['GH','HE','DH','EG'])
for n,p in pts.items():
    offset={'A':(-.25,.05),'B':(.06,.07),'C':(.1,.04),'D':(-.16,.13),'E':(-.25,-.12),'F':(.05,-.22),'G':(.12,-.03),'H':(-.2,-.19)}[n];text(ax,*(p+offset),n)
save(fig,'fig_g28')
