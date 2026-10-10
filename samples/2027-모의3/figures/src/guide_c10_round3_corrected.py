"""Corrected reference guide only, m=4-cuberoot(32)."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'serif','mathtext.fontset':'stix','font.size':18})
root=Path(__file__).resolve().parent
fig,ax=plt.subplots(figsize=(8,5.5),dpi=200)
ax.set_xlim(-.55,5.5);ax.set_ylim(-.5,5.2);ax.axis('off')
for end,start in [((4.85,0),(-.3,0)),((0,5),(0,-.25))]:
    ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'-|>','lw':1,'color':'black'})
x=np.linspace(0,4,1600);f=-x*x+4*x;m=4-np.cbrt(32);cross=4-m
ax.fill_between(x,0,np.minimum(f,m*x),color='#BFBFBF')
xx=np.linspace(0,cross,1000);ax.fill_between(xx,m*xx,-xx*xx+4*xx,color='#D9D9D9')
ax.plot(x,f,color='black',lw=1.2)
ax.plot([0,3.8],[0,3.8*m],color='black',lw=1.2)
for xx,yy,s in [(2.35,4.15,r'$y=-x^2+4x$'),(3.83,3.8*m+.08,r'$y=mx$'),(4,-.2,'4'),(-.1,-.12,'O'),(4.85,-.12,r'$x$'),(-.08,5,r'$y$')]:
    ax.text(xx,yy,s,ha='center' if s=='4' else 'right' if s in ['O',r'$y$'] else 'left',va='top' if s in ['4','O',r'$x$'] else 'bottom')
fig.savefig(root/'raw/fig_c10_round3_corrected_guide.png',bbox_inches='tight',pad_inches=.08,facecolor='white')
print('m=',m,'intersection=',cross,m*cross)
