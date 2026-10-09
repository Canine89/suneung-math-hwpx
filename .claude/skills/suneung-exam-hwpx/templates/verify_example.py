"""모든 문항의 정답을 계산으로 검증한다."""
from fractions import Fraction as Fr
from itertools import product
import sympy as sp

x, t, h, th = sp.symbols('x t h theta', real=True)
R = {}

# ---------- 공통 ----------
R[1] = sp.simplify((2**sp.sqrt(3))**sp.sqrt(3) * 4**sp.Rational(-1, 2))
f = x**3 - 2*x**2 + 5
R[2] = sp.limit((f.subs(x, 2+h) - f.subs(x, 2))/h, h, 0)
r = sp.symbols('r', positive=True); rs = sp.solve(sp.Eq(2*r**4, 4*2*r**2), r)
R[3] = 2*rs[0]**3
a = sp.symbols('a'); R[4] = sp.solve(sp.Eq(2**3 - a, a*2 + 2), a)[0]
R[5] = sp.diff((x**2+1)*(2*x-3), x).subs(x, 2)
# 6: pi<th<3pi/2, cos(pi/2+th)=3/5 -> sin th=-3/5, cos=-4/5
R[6] = sp.Rational(-3, 5)/sp.Rational(-4, 5)
R[7] = sp.integrate(x - (x**2 - 2*x), (x, 0, 3))
A_, B_ = sp.symbols('A B', positive=True)
sol = sp.solve([sp.Eq(B_, A_**2), sp.Eq(A_**3, 2**9)], [A_, B_], dict=True)
R[8] = [s[A_] + s[B_] for s in sol if s[A_] > 1]
k = sp.symbols('k'); g = x**3 - 3*x**2 - 9*x + k
R[9] = sp.solve(sp.Eq(g.subs(x, -1) + g.subs(x, 3), 0), k)
# 10: f=a sin bx, AB=4, area=18
aa, bb = sp.symbols('a b', positive=True)
AB = (5*sp.pi/6 - sp.pi/6)/bb
s10 = sp.solve([sp.Eq(AB, 4), sp.Eq(sp.Rational(1, 2)*4*(aa/2 + aa), 18)], [aa, bb], dict=True)[0]
R[10] = s10[aa]*s10[bb]
# 11
xP = sp.integrate(3*t**2 - 6*t, (t, 0, t)); xQ = sp.integrate(2*t, (t, 0, t))
kk = [s for s in sp.solve(sp.Eq(xP, xQ), t) if s > 0][0]
R[11] = (kk, sp.integrate(sp.Abs(3*t**2 - 6*t), (t, 0, kk)))
# 12: a_n = d(n-6), |a3|=a9, sum_{k=1}^4 1/(a_k a_{k+1}) = 1/20
d = sp.symbols('d', real=True)
an = lambda n: d*(n-6)
sols = [dv for dv in sp.solve(sp.Eq(sum(1/(an(i)*an(i+1)) for i in range(1, 5)), sp.Rational(1, 20)), d)
        if sp.Abs(an(3).subs(d, dv)) == an(9).subs(d, dv)]
R[12] = [sum(an(i).subs(d, dv) for i in range(1, 13)) for dv in sols]
# 13
p, q = sp.symbols('p q')
F = x**3 + p*x**2 + q*x
s13 = sp.solve([sp.Eq(F.subs(x, 1), sp.diff(F, x).subs(x, 1)), sp.Eq(sp.diff(F, x).subs(x, -1), 0)], [p, q])
R[13] = F.subs(s13).subs(x, 2)
# 14
cosA = sp.Rational(1, 3); sinA = sp.sqrt(1 - cosA**2)
BC2 = 36 + 16 - 2*6*4*cosA
X2 = BC2/(2*(1 + cosA))
R[14] = sp.nsimplify(sp.Rational(1, 2)*6*4*sinA + sp.Rational(1, 2)*X2*sinA)
# 15: f=(x-1)(x^2+px+q), f'(1)=-3, tangent at 3 through (1,0)
F = (x-1)*(x**2 + p*x + q); dF = sp.diff(F, x)
s15 = sp.solve([sp.Eq(dF.subs(x, 1), -3), sp.Eq(F.subs(x, 3) + dF.subs(x, 3)*(1-3), 0)], [p, q])
R[15] = (s15, F.subs(s15).subs(x, 4))
R[16] = [s for s in sp.solve(sp.Eq((x+2)*(x-2), 32), x) if s > 2]
C = sp.symbols('C'); Fx = sp.integrate(6*x**2 - 4*x + 3, x) + C
R[17] = Fx.subs(C, sp.solve(sp.Eq(Fx.subs(x, 1), 5), C)[0]).subs(x, 2)
R[18] = (60 - 30)//2 + 55
G = 2*x**3 - 3*x**2 - 12*x
R[19] = len([kv for kv in range(-100, 100) if len(set(sp.Poly(G + kv, x).real_roots())) == 3])
# 20
def nxt(v): return v + 3 if v % 2 else v // 2
R[20] = sum(a1 for a1 in range(1, 2000) if nxt(nxt(nxt(nxt(a1)))) == 5)
# 21: A=(2,6) on y=a^x, k=8 -> a^4 + k^2
R[21] = 6**2 + 8**2
# 22: f=(x-1)^3-3(x-1), h=t^2-4
f22 = (x-1)**3 - 3*(x-1)
crit = sp.solve(sp.diff(f22, x), x)
R[22] = (sorted(f22.subs(x, c) for c in crit), f22.subs(x, 0), sp.diff(f22, x).subs(x, 0), f22.subs(x, 5) + (25 - 4))

# ---------- 확률과 통계 ----------
P = {}
P[23] = sp.factorial(5)/(sp.factorial(2)**2)
P[24] = sp.Poly(sp.expand((x**2 + 2/x)**6 * x**6), x).coeff_monomial(x**9)
P[25] = Fr(3, 3 + 6)
P[26] = 'n=30' if (30*Fr(1, 3) == 10 and 9*30*Fr(1, 3)*Fr(2, 3) == 60) else 'X'
P[27] = round(0.4332 + 0.1915, 4)
P[28] = sum(1 for s in product(range(1, 6), repeat=4) if sum(s) % 2 == 0 and 3 in s)
cnt = tot = 0
for a_, b_, c_ in product(range(1, 7), repeat=3):
    tot += 1
    if a_ <= b_ <= c_ and (a_ + b_ + c_) % 2 == 0: cnt += 1
P[29] = (Fr(cnt, tot), Fr(cnt, tot).numerator + Fr(cnt, tot).denominator)
P[30] = sum(1 for f_ in product(range(1, 6), repeat=5)
            if f_[0] <= f_[1] <= f_[2] and f_[2] < f_[3] and f_[4] == f_[0] + f_[3] - f_[2])

# ---------- 미적분 ----------
M = {}
M[23] = sp.limit((sp.exp(3*x) - 1)/sp.log(1 + 2*x), x, 0)
M[24] = ((3*t**2 - 2)/(2*t)).subs(t, 2)
M[25] = 3 + 2
M[26] = sp.simplify(sp.integrate(x*sp.exp(2*x), (x, 0, 1)))
yy = sp.Function('y')(x)
dy = sp.solve(sp.diff(x**2 + x*yy + yy**2, x), sp.diff(yy, x))[0]
M[27] = dy.subs(yy, 2).subs(x, 1)
M[28] = sp.simplify(1*(sp.E + 1) - 0 - sp.integrate(sp.exp(x) + x, (x, 0, 1)))
# 29: radius 2 sector; S = region between AT, TP, arc PA; T = triangle PHA
S = 2*sp.tan(th) - 2*th
T = sp.Rational(1, 2)*(2 - 2*sp.cos(th))*2*sp.sin(th)
M[29] = 60*sp.limit((S + T)/th**3, th, 0)
g30 = (x + 1)**2*sp.exp(-x)
I30 = sp.simplify(sp.integrate(g30, (x, -1, 1)))
M[30] = (sp.solve(sp.diff(g30, x), x), sp.solve(sp.diff(g30, x, 2), x), I30)

# ---------- 기하 ----------
Gm = {}
Gm[23] = sp.sqrt((1 - (-1))**2 + 0 + (-3 - 3)**2)
Gm[24] = sp.sqrt(4**2 + 8*4)
tt = sp.symbols('tt'); expr = (2 + tt)**2 + (1 - 3*tt)**2
Gm[25] = sp.sqrt(expr.subs(tt, sp.solve(sp.diff(expr, tt), tt)[0]))
Gm[26] = 9  # b^2 tan(45deg)
Gm[27] = sp.solve(sp.Eq(10, 2*x - 2), x)
Gm[28] = 9*sp.sqrt(3)*sp.Rational(1, 3)
u = sp.symbols('u'); r8 = sp.sqrt(8)
Pp = (1 + r8*sp.cos(u), 1 + r8*sp.sin(u))
dot = (7 - Pp[0])*(1 - Pp[0]) + (1 - Pp[1])*(7 - Pp[1])
Gm[29] = sp.simplify(sp.maximum(dot, u, sp.Interval(0, 2*sp.pi)))
rr = 3*sp.sqrt(3)/2
Gm[30] = sp.expand((-rr - 4)**2 + 0 + sp.Rational(3, 2)**2)

for name, D in [('공통', R), ('확통', P), ('미적', M), ('기하', Gm)]:
    print('=====', name)
    for kq in sorted(D): print(kq, D[kq])
