"""User-authorized exact coordinate guide ONLY, not final deliverable."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

root = Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'serif','mathtext.fontset':'stix'})
fig, ax = plt.subplots(figsize=(8,4.8),dpi=200)
ax.set_xlim(-.55,9.35)
ax.set_ylim(-3.9,3.9)
ax.axis('off')
k=3*np.sqrt(2)/2
points=np.array([[1,k],[3,k],[5,-k],[7,-k]])
ax.add_patch(Polygon(points[[0,1,3,2]],closed=True,facecolor='#D9D9D9',edgecolor='black',linewidth=1.1))
x=np.linspace(0,8,2001)
ax.plot(x,3*np.sin(np.pi*x/4),color='black',linewidth=1.2)
for yy, label in [(k,r'$y=k$'),(-k,r'$y=-k$')]:
    ax.plot([-.3,8.5],[yy,yy],color='black',linewidth=.9)
    ax.text(8.55, yy+.08,label,fontsize=20,va='bottom')
ax.annotate('',xy=(8.65,0),xytext=(-.3,0),arrowprops={'arrowstyle':'-|>','color':'black','lw':.9,'mutation_scale':14})
ax.annotate('',xy=(0,3.6),xytext=(0,-3.55),arrowprops={'arrowstyle':'-|>','color':'black','lw':.9,'mutation_scale':14})
ax.scatter(points[:,0],points[:,1],s=45,c='black',zorder=5)
for (xx,yy),name in zip(points,'ABCD'):
    ax.text(xx,yy+(.23 if yy>0 else -.25),name,ha='center',va='bottom' if yy>0 else 'top',fontsize=21,fontstyle='normal')
ax.text(-.1,-.14,'O',fontsize=21,ha='right',va='top')
ax.text(8.64,-.15,r'$x$',fontsize=21,va='top')
ax.text(-.13,3.55,r'$y$',fontsize=21,ha='right')
fig.savefig(root/'raw/fig_c10_guide.png',dpi=200,facecolor='white',bbox_inches='tight',pad_inches=.08)
plt.close(fig)
