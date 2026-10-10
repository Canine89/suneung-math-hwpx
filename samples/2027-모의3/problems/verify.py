"""3회 문항의 정답을 계산으로 검증하고 exam.py 의 ans/보기와 대조한다."""
import os
import sys
from fractions import Fraction as Fr
from itertools import product
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exam  # noqa: E402

x, t, h, th, a, b, c, k = sp.symbols('x t h theta a b c k', real=True)
R, P, M, G = {}, {}, {}, {}

# ---------- 공통 ----------
R[1] = sp.nsimplify(sp.Rational(1, 4)**sp.Rational(-3, 2) * sp.Rational(1, 2))
R[2] = sp.limit((2*x**2 + 3*x)/(x**2 - 1), x, sp.oo)
r = [v for v in sp.solve(3*x**3 - 24, x) if v.is_real][0]
R[3] = 3*r + 3*r**2
f4 = x**2 - 3*x
R[4] = sp.diff((x + 1)*f4, x).subs(x, 2)
cs = sp.Rational(-1, 3)   # cos(pi+th) = -cos th = 1/3
R[5] = sp.sqrt(1 - cs**2)  # 2사분면 → sin > 0
R[6] = sp.integrate(sp.Abs(x - 1), (x, 0, 3))
R[7] = sp.simplify(sp.log(5, 3)*sp.log(9, 5))
f8 = x**3 - 2*x + 1
tan8 = sp.diff(f8, x).subs(x, 1)*(x - 1)
R[8] = sp.solve(sp.Eq(tan8, 3), x)
# 9: a cos bx + c, max 5, min -1, 첫 양의 교점(y=2) = pi/4
aa, cc = sp.solve([a + c - 5, -a + c + 1], [a, c]).values()
bb = sp.solve(sp.Eq((sp.pi/2)/b, sp.pi/4), b)[0]
R[9] = aa*bb*cc
m = sp.symbols('m', positive=True)
total = sp.integrate(-x**2 + 4*x, (x, 0, 4))
part = sp.integrate(-x**2 + 4*x - m*x, (x, 0, 4 - m))
msol = [v for v in sp.solve(sp.Eq(part, total/2), m) if v.is_real and 0 < v < 4]
R[10] = [sp.simplify((4 - v)**3) for v in msol]
import math
R[11] = [n for n in range(1, 200) if abs(sum(1/(math.sqrt(j + 1) + math.sqrt(j)) for j in range(1, n + 1)) - 4) < 1e-9]
x1, x2 = t**3 - 3*t**2, 3*t**2 - 9*t
ts = [v for v in sp.solve(sp.Eq(sp.diff(x1, t), sp.diff(x2, t)), t) if v > 0]
R[12] = sum(sp.Abs(x1.subs(t, v) - x2.subs(t, v)) for v in ts)
kk = sp.solve(sp.Eq(sp.log(k, 2) - sp.log(k - 4, 2), 1), k)[0]
A13 = (kk, sp.log(kk, 2)); B13 = (kk, sp.log(kk - 4, 2))
Cx = sp.solve(sp.Eq(sp.log(x - 4, 2), A13[1]), x)[0]
R[13] = sp.nsimplify(sp.Rational(1, 2)*(Cx - kk)*(A13[1] - B13[1]))
cosA = sp.Rational(1, 4); sinA = sp.sqrt(1 - cosA**2)
BC = sp.sqrt(16 + 36 - 2*4*6*cosA)
Rad = BC/(2*sinA)
R[14] = sp.simplify(sp.pi*Rad**2)
# 15: f = x^2 + px + q, h(t)=int_t^{t+2} f, min at t=1, h(1)=2/3
p, q = sp.symbols('p q')
f15 = x**2 + p*x + q
h15 = sp.integrate(f15, (x, t, t + 2))
s15 = sp.solve([sp.diff(h15, t).subs(t, 1), h15.subs(t, 1) - sp.Rational(2, 3)], [p, q], dict=True)
assert sp.diff(h15, t, 2) > 0
R[15] = [f15.subs(s).subs(x, 5) + h15.subs(s).subs(t, 0) for s in s15]
R[16] = [v for v in sp.solve(sp.Eq(x + 6, x**2), x) if v > 0]
R[17] = sp.integrate(3*x**2 + 2*x - 1, (x, 0, 2))
R[18] = 50 + 2*20 + 10
f19 = -x**3 + 3*x**2 + 9*x + 1
cand = [-2, 4] + [v for v in sp.solve(sp.diff(f19, x), x) if -2 <= v <= 4]
R[19] = max(f19.subs(x, v) for v in cand)
seq = [1]
while len(seq) < 20:
    v = seq[-1]; seq.append(v//2 if v % 2 == 0 else v + 5)
R[20] = sum(seq)
# 21: |3 sin x - 1| = k, [0, 2pi) 에서 서로 다른 실근 3개
def roots21(kv):
    # sin x = v 의 [0, 2pi) 해를 직접 구한다 (v = ±1 이면 하나)
    rs = set()
    for s in {kv, -kv}:
        v = (1 + s)/sp.Integer(3)
        if abs(v) > 1:
            continue
        r0 = sp.asin(v)
        for r1 in (r0, sp.pi - r0):
            rs.add(sp.simplify(r1 % (2*sp.pi)))
    return rs
ok21 = [(kv, roots21(kv)) for kv in [sp.Rational(n, 4) for n in range(0, 17)] if len(roots21(kv)) == 3]
R[21] = [(kv, sp.simplify(sum(rs)/sp.pi)) for kv, rs in ok21]
# 22: g = -f (x<a), f (x>=a), f = (x-a)^2 (x-b) 꼴. 조건으로 a, b 결정
A_, B_ = sp.symbols('A_ B_', real=True)
f22 = (x - A_)**2*(x - B_)
crit = sp.solve(sp.diff(f22, x), x)   # A_, (A_+2B_)/3
sol22 = []
for bsol in sp.solve(sp.Eq((A_ + 2*B_)/3, A_ + 2), B_):
    for asol in sp.solve(sp.Eq(-f22.subs(B_, bsol).subs(x, 0), 4), A_):   # a>0 이므로 g(0) = -f(0)
        if asol.is_real and asol > 0:
            sol22.append((asol, bsol.subs(A_, asol)))
g22 = lambda xv, A0, B0: (-f22 if xv < A0 else f22).subs({A_: A0, B_: B0, x: xv})
R[22] = [(s, g22(-2, *s) + g22(5, *s)) for s in sol22]

# ---------- 확률과 통계 ----------
P[23] = 3**4
P[24] = sp.binomial(5, 3)*2**3
P[25] = Fr(6, 8 + 6)
P[26] = 9*120*Fr(1, 3)*Fr(2, 3)
mm = 48 + 4   # (48-m)/4 = -1
P[27] = round(0.4772 - 0.1915, 4)
P[28] = Fr(sum(1 for t4 in product(range(1, 7), repeat=4) if (t4[0]*t4[1]*t4[2]*t4[3]) % 4 == 0), 6**4)
P[29] = sum(1 for a_, b_, c_ in product(range(13), repeat=3)
            if (d := 12 - a_ - b_ - c_) >= 0 and a_ >= 1 and b_ >= 2 and c_ % 2 == 0 and d % 2 == 0)
P[30] = sum(1 for f in product(range(1, 6), repeat=5) if f[0] + f[4] == 6 and f[0] < f[1] < f[2] and len(set(f)) == 3)

# ---------- 미적분 ----------
M[23] = sp.limit((sp.exp(2*x) - 1)/(3*x), x, 0)
M[24] = (sp.diff(sp.exp(2*t), t)/sp.diff(sp.exp(t) + t, t)).subs(t, 0)
nn = sp.symbols('nn', positive=True, integer=True)
M[25] = sp.limit((2**(nn + 1) + 3**nn)/(3**(nn + 1) - 2**nn), nn, sp.oo)
M[26] = sp.integrate(x*sp.cos(x), (x, 0, sp.pi/2))
M[27] = sp.simplify(sp.integrate(x/sp.E, (x, 0, sp.E)) - sp.integrate(sp.log(x), (x, 1, sp.E)))
# 28: (x^2+a)e^{-x} 감소 ⇔ x^2-2x+a >= 0 ⇔ a >= 1
f28 = (x**2 + 1)*sp.exp(-x)
assert sp.simplify(f28.subs(x, 2) - 5/sp.E**2) == 0
M[28] = sp.simplify(1/sp.diff(f28, x).subs(x, 2))
Pp = (sp.cos(th), sp.sin(th)); Qp = (0, sp.sin(th)); Rp = (sp.cos(th)**2, sp.cos(th)*sp.sin(th))
area = sp.Abs((Qp[0] - Pp[0])*(Rp[1] - Pp[1]) - (Rp[0] - Pp[0])*(Qp[1] - Pp[1]))/2
seg = (th - sp.sin(th))/2
area = ((Qp[0] - Pp[0])*(Rp[1] - Pp[1]) - (Rp[0] - Pp[0])*(Qp[1] - Pp[1]))/2  # 작은 theta 에서 양수
assert area.subs(th, 0.3) > 0
M[29] = 120*sp.limit((area + seg)/th**3, th, 0, '+')
tt = sp.symbols('tt', positive=True)
yt = sp.exp(-x/2)
tan30 = sp.diff(yt, x).subs(x, tt)*(x - tt) + yt.subs(x, tt)
xi = sp.solve(tan30, x)[0]; yi = tan30.subs(x, 0)
S30 = sp.simplify(xi*yi/2)
a30 = sp.solve(sp.diff(S30, tt), tt)
I30 = sp.expand(sp.integrate(S30, (tt, 0, a30[0])))
pp, rest = I30.as_independent(sp.E)
qq = sp.simplify(rest*sp.E)
M[30] = (a30, I30, pp, qq, pp - qq)

# ---------- 기하 ----------
G[23] = sp.sqrt(2**2 + 2**2 + 1**2)
G[24] = sp.Rational(4 + 9 - 7, 2)
G[25] = 3 + 3   # y=6 → x=3, PF = x + 3
G[26] = 3 + 5 + 6
aa27 = sp.solve(sp.Eq(3/a, sp.Rational(3, 2)), a)[0]
G[27] = 2*sp.sqrt(aa27**2 + 9)
G[28] = sp.nsimplify(2*sp.sqrt(2)/(2*sp.sqrt(3)))
r29 = sp.sqrt((40 - 2*8)/2)   # PA^2+PB^2 = 2PM^2 + AB^2/2, M=(2,2), AB^2=32
G[29] = sp.expand(4*(2 + r29))
u = sp.symbols('u')
Pc = (1 + sp.sqrt(5)*sp.cos(u), 2 + sp.sqrt(5)*sp.sin(u), 0)
d2 = sp.expand(sum((pi_ - qi)**2 for pi_, qi in zip(Pc, (4, 2, 4))))
G[30] = (sp.simplify(d2), max(d2.subs(u, sp.pi*j/180).evalf() for j in range(360)), (30 + 6*sp.sqrt(5)).evalf())

sys.stdout.reconfigure(encoding="utf-8")
for name, D in [('공통', R), ('확통', P), ('미적', M), ('기하', G)]:
    print('=====', name)
    for kq in sorted(D): print(kq, D[kq])
print('===== exam.py 정답')
def show(probs):
    for pr_ in probs:
        ch = next((bl[1] for bl in pr_['blocks'] if bl[0] == 'ch'), None)
        print(pr_['no'], (ch[pr_['ans'] - 1] if ch else pr_['ans']))
show(exam.COMMON)
for nm, probs in exam.SUBJECTS:
    print('--', nm); show(probs)
