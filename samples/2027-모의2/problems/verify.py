"""2회 문항의 정답을 계산으로 검증하고 exam.py 의 ans/보기와 대조한다."""
import os
import sys
from fractions import Fraction as Fr
from itertools import product, combinations, permutations
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exam  # noqa: E402

x, t, h, th, a, b, k = sp.symbols('x t h theta a b k', real=True)
R, P, M, G = {}, {}, {}, {}

# ---------- 공통 ----------
R[1] = sp.nsimplify(sp.root(8, 3) * sp.Integer(27)**sp.Rational(2, 3))
R[2] = sp.diff(2*x**3 - x + 4, x).subs(x, 1)
A1, D_ = sp.symbols('A1 D_')
s = sp.solve([A1 + D_ - 5, (A1 + 5*D_) - (A1 + 2*D_) - 9], [A1, D_])
R[3] = s[A1] + 9*s[D_]
s = sp.solve([4 + 2*a + b, sp.limit((x**2 + a*x + b).subs(b, -4 - 2*a)/(x - 2), x, 2) - 7], [a, b], dict=True)[0]
R[4] = s[a] + s[b]
R[5] = (sp.Rational(1, 2)**2 - 1) / 2
R[6] = sp.integrate(x**3 + 3*x**2 + 2, (x, -1, 1))
s = sp.solve([a + b - 8, a*b - 16], [a, b], dict=True)
R[7] = {sp.simplify(si[a]**2 + si[b]**2) for si in s if si[a] > 0 and si[b] > 0}
R[8] = sp.integrate(2*x - (x**2 - 2*x), (x, 0, 4))
f9 = x**3 - 3*x**2 + 2
tan9 = sp.diff(f9, x).subs(x, 3)*(x - 3) + 2
roots9 = sp.solve(sp.Eq(f9, tan9), x)
R[9] = [f9.subs(x, r) for r in roots9 if r != 3]
# 10: y=3 sin(pi x/4), AB=2
tt = sp.symbols('tt', positive=True)
t10 = sp.solve(sp.Eq((4 - tt) - tt, 2), tt)[0]
k10 = 3*sp.sin(sp.pi*t10/4)
Apt, Bpt, Cpt, Dpt = (t10, k10), (4 - t10, k10), (4 + t10, -k10), (8 - t10, -k10)
poly = [Apt, Bpt, Dpt, Cpt]
R[10] = sp.nsimplify(sp.Abs(sum(poly[i][0]*poly[(i+1) % 4][1] - poly[(i+1) % 4][0]*poly[i][1] for i in range(4))) / 2)
xt = t**3 - 6*t**2 + 9*t
R[11] = sum(abs(xt.subs(t, q) - xt.subs(t, p)) for p, q in [(0, 1), (1, 3), (3, 4)])
seq = [1]
for n in range(1, 10):
    seq.append(2*seq[-1] if n % 2 == 1 else seq[-1] + 3)
R[12] = sum(seq)
# 13: f = 3x^2 + 2a x + C 를 일반 이차식으로 두고 항등식 풀기
c0, c1, c2 = sp.symbols('c0 c1 c2')
f13 = c2*x**2 + c1*x + c0
eq13 = sp.expand(x*f13 - (2*x**3 + a*x**2 + sp.integrate(f13.subs(x, t), (t, 1, x))))
s = sp.solve(list(sp.Poly(eq13, x).coeffs()) + [c0 - 2], [c0, c1, c2, a], dict=True)
R[13] = [f13.subs(si).subs(x, 3) for si in s]
# 14
cosB = sp.cos(2*sp.pi/3)
AC = sp.sqrt(25 + 9 - 2*5*3*cosB)
bd = sp.symbols('bd', positive=True)
# 삼각형 ABD: AB=5, AD=AC(정삼각형 ACD 이므로), angle ABD = 60도
R[14] = (AC, sp.solve(sp.Eq(AC**2, 25 + bd**2 - 2*5*bd*sp.cos(sp.pi/3)), bd))
# 15: f = x^2(x-3) 유일성 + |f|=k 근 개수
f15 = x**2*(x - 3)
def nroots(fx, kk):
    # 정확한 실근(중근은 하나로) — sympy.solve 는 삼차의 실근을 복소 표현으로 돌려줘 놓치므로 real_roots 사용
    rs = set(sp.Poly(fx - kk, x).real_roots()) | set(sp.Poly(fx + kk, x).real_roots())
    return len(rs)
R[15] = sum(kk for kk in range(1, 30) if nroots(f15, kk) == 4)
R[16] = sp.solve(sp.Eq(x + 1, 3*(x - 3)), x)
f17 = x**3 + a*x
R[17] = sp.solve(sp.Eq(2*sp.diff(f17, x).subs(x, 1), 14), a)
S = lambda n: n**2 + 3*n
R[18] = S(10) - S(9)
f19 = 2*x**3 - 9*x**2 + 12*x + k
k19 = sp.solve(sp.Eq(f19.subs(x, 2), 9), k)[0]
R[19] = f19.subs(k, k19).subs(x, 1)
def preds(v):
    out = []
    if v + 2 > 0: out.append(v + 2)
    if (1 - v) % 2 == 0 and (1 - v)//2 <= 0: out.append((1 - v)//2)
    return out
cur = {1}
for _ in range(5): cur = {p for v in cur for p in preds(v)}
def fwd(v):
    for _ in range(5): v = v - 2 if v > 0 else -2*v + 1
    return v
assert all(fwd(v) == 1 for v in cur) and all((fwd(v) == 1) == (v in cur) for v in range(-500, 500))
R[20] = sum(cur)
# 21
kk = sp.symbols('kk', positive=True)
area = 3*((kk - kk/8) + (8*kk - kk))/2
k21 = sp.solve(sp.Eq(area, sp.Rational(189, 2)), kk)[0]
R[21] = 8*k21
# 22: f = x^4 + p x^2 + q
p, q = sp.symbols('p q', real=True)
cands = []
for sol in sp.solve([81 + 9*p + q, q - p**2/4 + 9], [p, q], dict=True):
    fx = x**4 + sol[p]*x**2 + sol[q]
    rr = [r for r in sp.solve(fx, x) if r.is_real]
    if sol[p] < 0 and max(rr) == 3: cands.append(fx)
R[22] = [c.subs(x, 4) for c in cands]

# ---------- 확률과 통계 ----------
P[23] = sum(1 for a_, b_ in product(range(8), repeat=2) if a_ + b_ <= 7)
pB = sp.symbols('pB')
P[24] = sp.solve(sp.Eq(sp.Rational(1, 2) + pB - pB/2, sp.Rational(4, 5)), pB)
P[25] = sum(1 for perm in permutations(range(6)) if perm[0] == 0 and abs(perm.index(1) - perm.index(2)) in (1, 5)) \
    if False else sp.factorial(4)*2
aa = sp.solve(sp.Eq(sum((xx + a)/9 for xx in range(3)), 1), a)[0]
pr = [(xx + aa)/9 for xx in range(3)]
E = sum(xx*pr[xx] for xx in range(3)); V = sum(xx**2*pr[xx] for xx in range(3)) - E**2
P[26] = 81*V
P[27] = sp.nsimplify(4.9 / (2*1.96) * 4)
ev = [c for c in combinations(range(1, 7), 3) if sum(c) % 2 == 0]
P[28] = Fr(sum(1 for c in ev if max(c) - min(c) >= 4), len(ev))
P[29] = sum(1 for perm in set(permutations([1, 1, 2, 2, 3, 3])) if all(perm[i] != perm[i+1] for i in range(5)))
P[30] = sum(1 for f in product(range(1, 7), repeat=6) if f[0] + f[1] + f[2] == 7 and f[3] < f[4] < f[5] and f[0] <= f[3])

# ---------- 미적분 ----------
M[23] = sp.limit(sp.log(1 + 4*x)/sp.sin(2*x), x, 0)
M[24] = sp.simplify(sp.diff(x*sp.exp(2*x), x).subs(x, 1))
r = sp.solve(sp.Eq(4/(1 - x), 6), x)[0]
M[25] = 16/(1 - r**2)
M[26] = sp.simplify(sp.integrate(x*sp.exp(x**2), (x, 0, 1)))
M[27] = sp.simplify(sp.integrate(2*sp.sin(x) - 1, (x, sp.pi/6, 5*sp.pi/6)))
fx = sp.log(x)/x
t0 = sp.solve(sp.Eq(fx.subs(x, t), t*sp.diff(fx, x).subs(x, t)), t)
M[28] = [sp.simplify(sp.diff(fx, x).subs(x, tv)) for tv in t0]
P_ = (sp.Rational(1, 2)*sp.sin(2*th)*2*sp.sin(th)**2)
Q_ = sp.Rational(1, 2)*(2*th - sp.sin(2*th))
M[29] = 30*sp.limit((P_ + Q_)/th**3, th, 0)
apos = sp.symbols('apos', positive=True)
fa = sp.integrate((apos - t)*sp.exp(t), (t, 0, x))
a30 = sp.solve(sp.Eq(fa.subs(x, apos), sp.E**2 - 3), apos)
I30 = sp.expand(sp.integrate(fa.subs(apos, a30[0]), (x, 0, a30[0])))
M[30] = (a30, I30, I30.coeff(sp.E**2)**2 + (I30 - I30.coeff(sp.E**2)*sp.E**2)**2)

# ---------- 기하 ----------
G[23] = sp.sqrt((3 + 2)**2 + (1 - 4)**2)
pt = [(2*1 + 1*4)/3, (2*3 + 1*(-3))/3, (2*(-2) + 1*7)/3]
G[24] = sum(pt)
# 타원 접선 2x/8 + y/2 = 1 -> 절편 4, 2
G[25] = sp.Rational(1, 2)*4*2
G[26] = 10 + (10 - 6) + 10
xs = sp.solve(sp.Eq(4 + 4*x, (x + 1)**2), x)
G[27] = [xv + 1 for xv in xs if xv > 0]
# 28: tan = PA / dist(A, BD) = 4 / 2sqrt2
G[28] = sp.nsimplify(sp.cos(sp.atan(4/(2*sp.sqrt(2)))))
Mx = sp.Matrix([1, 2])
G[29] = sp.expand((sp.sqrt(5) + 2)**2)
d30 = sp.Abs(4*2 + 3*(-1) - 15)/5
r2 = 29 - d30**2
G[30] = r2*sp.Rational(3, 5) + r2*sp.Rational(4, 5)

for name, D in [('공통', R), ('확통', P), ('미적', M), ('기하', G)]:
    print('=====', name)
    for kq in sorted(D): print(kq, D[kq])

# exam.py 의 정답 번호/값 출력 (대조용)
print('===== exam.py 정답')
def show(probs):
    for pr_ in probs:
        ch = next((bl[1] for bl in pr_['blocks'] if bl[0] == 'ch'), None)
        print(pr_['no'], (ch[pr_['ans'] - 1] if ch else pr_['ans']))
show(exam.COMMON)
for nm, probs in exam.SUBJECTS:
    print('--', nm); show(probs)
