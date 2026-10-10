"""수학 영역 모의 문제지 문항 데이터 (2회).

표기 규칙
- 본문 문자열 안의 $...$ 는 한글 수식(HWP 수식 스크립트)으로 조판된다.
- 블록: ('t', 문장) / ('eq', 수식) / ('box', [조건 줄...]) / ('fig', 파일이름, 가로mm)
        / ('ch', [보기 5개], 줄수) / ('side', [왼쪽 문장 줄...], 표준정규분포표 행)
- 배점 '[n점]'은 마지막 't' 블록 끝에 자동으로 붙는다 (side 블록은 직접 적음).
- 'ans' 는 정답(5지선다는 번호, 단답형은 값). verify.py 로 계산 검증함.
"""

META = {
    "year_title": "2027학년도 대학수학능력시험 모의 문제지",
    "period": "제 2 교시",
    "type": "홀수형",
    "copyright": "이 문제지는 학습용으로 제작된 모의 문제지입니다.",
    "out_name": "수학영역_문제지_2회",
}

N = lambda *xs: [str(x) for x in xs]  # 숫자 보기
F = lambda *xs: ["{%s} over {%s}" % tuple(x.split("/")) if "/" in x else x for x in xs]  # 분수 보기

COMMON = [
    dict(no=1, pts=2, ans=5, blocks=[
        ('t', "$root {3} of {8} TIMES 27 ^{{2} over {3}}$의 값은?"),
        ('ch', N(6, 9, 12, 15, 18))]),
    dict(no=2, pts=2, ans=3, blocks=[
        ('t', "함수 $f(x)=2x ^{3} -x+4$에 대하여 $f'(1)$의 값은?"),
        ('ch', N(1, 3, 5, 7, 9))]),
    dict(no=3, pts=3, ans=4, blocks=[
        ('t', "등차수열 $left lbrace a _{n} right rbrace$에 대하여 $a _{2} =5$, $a _{6} =a _{3} +9$일 때, "
              "$a _{10}$의 값은?"),
        ('ch', N(23, 25, 27, 29, 31))]),
    dict(no=4, pts=3, ans=1, blocks=[
        ('t', "두 상수 $a,~b$에 대하여"),
        ('eq', "lim _{x -> 2} {x ^{2} +ax+b} over {x-2} =7"),
        ('t', "일 때, $a+b$의 값은?"),
        ('ch', N(-7, -6, -5, -4, -3))]),
    dict(no=5, pts=3, ans=2, blocks=[
        ('t', "$sin theta + cos theta = {1} over {2}$일 때, $sin theta cos theta$의 값은?"),
        ('ch', ["- {1} over {2}", "- {3} over {8}", "- {1} over {4}", "- {1} over {8}", "{1} over {8}"])]),
    dict(no=6, pts=3, ans=4, blocks=[
        ('t', "$int _{-1} ^{1} left ( x ^{3} +3x ^{2} +2 right ) dx$의 값은?"),
        ('ch', N(3, 4, 5, 6, 7))]),
    dict(no=7, pts=3, ans=1, blocks=[
        ('t', "두 양수 $a,~b$가"),
        ('eq', "log _{2} (a+b)=3,~~~~ log _{2} a+ log _{2} b=4"),
        ('t', "를 만족시킬 때, $a ^{2} +b ^{2}$의 값은?"),
        ('ch', N(32, 34, 36, 38, 40))]),
    dict(no=8, pts=3, ans=5, blocks=[
        ('t', "곡선 $y=x ^{2} -2x$와 직선 $y=2x$로 둘러싸인 부분의 넓이는?"),
        ('ch', ["8", "{26} over {3}", "{28} over {3}", "10", "{32} over {3}"]),
        ('fig', "fig_c08", 55)]),
    dict(no=9, pts=4, ans=2, blocks=[
        ('t', "곡선 $y=x ^{3} -3x ^{2} +2$ 위의 점 $left ( 3,~2 right )$에서의 접선이 이 곡선과 만나는 점 중 "
              "점 $left ( 3,~2 right )$가 아닌 점의 $y$좌표는?"),
        ('ch', N(-54, -52, -50, -48, -46))]),
    dict(no=10, pts=4, ans=3, blocks=[
        ('t', "그림과 같이 함수 $y=3 sin {pi x} over {4}~(0 <= x <= 8)$의 그래프와 직선 $y=k$가 "
              "만나는 두 점을 $x$좌표가 작은 것부터 차례로 $rm A,~rm B$라 하고, 직선 $y=-k$가 만나는 두 점을 "
              "$x$좌표가 작은 것부터 차례로 $rm C,~rm D$라 하자. $overline {rm AB} =2$일 때, "
              "사각형 $rm ABDC$의 넓이는? (단, $0<k<3$)"),
        ('fig', "fig_c10", 65),
        ('ch', ["4 sqrt {2}", "5 sqrt {2}", "6 sqrt {2}", "7 sqrt {2}", "8 sqrt {2}"])]),
    dict(no=11, pts=4, ans=2, blocks=[
        ('t', "수직선 위를 움직이는 점 $rm P$의 시각 $t~(t >= 0)$에서의 위치 $x$가"),
        ('eq', "x=t ^{3} -6t ^{2} +9t"),
        ('t', "이다. 시각 $t=0$에서 $t=4$까지 점 $rm P$가 움직인 거리는?"),
        ('ch', N(10, 12, 14, 16, 18))]),
    dict(no=12, pts=4, ans=4, blocks=[
        ('t', "수열 $left lbrace a _{n} right rbrace$이 $a _{1} =1$이고, 모든 자연수 $n$에 대하여"),
        ('eq', 'a _{n+1} = cases{2a _{n} ~~~~ & left ( n "이"~"홀수인"~"경우" right )#'
               'a _{n} +3 & left ( n "이"~"짝수인"~"경우" right )}'),
        ('t', "를 만족시킬 때, $sum _{k=1} ^{10} a _{k}$의 값은?"),
        ('ch', N(315, 319, 323, 327, 331))]),
    dict(no=13, pts=4, ans=1, blocks=[
        ('t', "다항함수 $f(x)$가 모든 실수 $x$에 대하여"),
        ('eq', "xf(x)=2x ^{3} +ax ^{2} + int _{1} ^{x} f(t)dt"),
        ('t', "를 만족시킨다. $f(0)=2$일 때, $f(3)$의 값은? (단, $a$는 상수이다.)"),
        ('ch', N(11, 13, 15, 17, 19))]),
    dict(no=14, pts=4, ans=5, blocks=[
        ('t', "그림과 같이 $overline {rm AB} =5$, $overline {rm BC} =3$, $angle rm ABC = {2} over {3} pi$인 "
              "삼각형 $rm ABC$가 있다. 삼각형 $rm ABC$의 외접원 위의 점 중 점 $rm B$를 포함하지 않는 "
              "호 $rm AC$ 위의 점 $rm D$에 대하여 $overline {rm AD} = overline {rm CD}$일 때, "
              "선분 $rm BD$의 길이는?"),
        ('fig', "fig_c14", 50),
        ('ch', ["6", "{13} over {2}", "7", "{15} over {2}", "8"])]),
    dict(no=15, pts=4, ans=3, blocks=[
        ('t', "최고차항의 계수가 $1$인 삼차함수 $f(x)$가 다음 조건을 만족시킨다."),
        ('box', ["(가) $f(0)=0$",
                 "(나) 함수 $left | f(x) right |$는 $x=3$에서만 미분가능하지 않다."]),
        ('t', "$x$에 대한 방정식 $left | f(x) right | =k$의 서로 다른 실근의 개수가 $4$가 되도록 하는 "
              "모든 자연수 $k$의 값의 합은?"),
        ('ch', N(4, 5, 6, 7, 8))]),
    # ---------------- 단답형 ----------------
    dict(no=16, pts=3, ans=5, blocks=[
        ('t', "방정식 $2 ^{x+1} =8 ^{x-3}$을 만족시키는 실수 $x$의 값을 구하시오.")]),
    dict(no=17, pts=3, ans=4, blocks=[
        ('t', "함수 $f(x)=x ^{3} +ax$에 대하여"),
        ('eq', "lim _{h -> 0} {f(1+2h)-f(1)} over {h} =14"),
        ('t', "일 때, 상수 $a$의 값을 구하시오.")]),
    dict(no=18, pts=3, ans=22, blocks=[
        ('t', "수열 $left lbrace a _{n} right rbrace$의 첫째항부터 제$n$항까지의 합 $S _{n}$이 "
              "$S _{n} =n ^{2} +3n$일 때, $a _{10}$의 값을 구하시오.")]),
    dict(no=19, pts=3, ans=10, blocks=[
        ('t', "함수 $f(x)=2x ^{3} -9x ^{2} +12x+k$의 극솟값이 $9$일 때, 함수 $f(x)$의 극댓값을 구하시오. "
              "(단, $k$는 상수이다.)")]),
    dict(no=20, pts=4, ans=21, blocks=[
        ('t', "모든 항이 정수인 수열 $left lbrace a _{n} right rbrace$이 모든 자연수 $n$에 대하여"),
        ('eq', 'a _{n+1} = cases{a _{n} -2 ~~~~ & left ( a _{n} >0 right )#'
               '-2a _{n} +1 & left ( a _{n} <= 0 right )}'),
        ('t', "을 만족시킨다. $a _{6} =1$이 되도록 하는 모든 $a _{1}$의 값의 합을 구하시오.")]),
    dict(no=21, pts=4, ans=64, blocks=[
        ('t', "$1$보다 큰 실수 $k$에 대하여 직선 $y=k$가 두 곡선 $y=2 ^{x}$, $y=2 ^{x-3}$과 만나는 점을 "
              "각각 $rm A,~rm B$라 하자. 점 $rm B$를 지나고 $y$축에 평행한 직선이 곡선 $y=2 ^{x}$과 만나는 점을 "
              "$rm C$, 점 $rm A$를 지나고 $y$축에 평행한 직선이 곡선 $y=2 ^{x-3}$과 만나는 점을 $rm D$라 하자. "
              "사각형 $rm ADBC$의 넓이가 ${189} over {2}$일 때, 점 $rm C$의 $y$좌표를 구하시오."),
        ('fig', "fig_c21", 55)]),
    dict(no=22, pts=4, ans=91, blocks=[
        ('t', "최고차항의 계수가 $1$인 사차함수 $f(x)$가 다음 조건을 만족시킨다."),
        ('box', ["(가) 모든 실수 $x$에 대하여 $f(-x)=f(x)$이다.",
                 "(나) 함수 $f(x)$의 극솟값은 $-9$이다.",
                 "(다) 방정식 $f(x)=0$의 실근 중 가장 큰 값은 $3$이다."]),
        ('t', "$f(4)$의 값을 구하시오.")]),
]

STATS = [
    dict(no=23, pts=2, ans=2, blocks=[
        ('t', "방정식 $a+b+c=7$을 만족시키는 음이 아닌 정수 $a,~b,~c$의 모든 순서쌍 $left ( a,~b,~c right )$의 "
              "개수는?"),
        ('ch', N(32, 36, 40, 44, 48))]),
    dict(no=24, pts=3, ans=4, blocks=[
        ('t', "두 사건 $A,~B$가 서로 독립이고"),
        ('eq', "{rm P} left ( A right ) = {1} over {2} ,~~~~ {rm P} left ( A cup B right ) = {4} over {5}"),
        ('t', "일 때, ${rm P} left ( B right )$의 값은?"),
        ('ch', F("1/5", "2/5", "1/2", "3/5", "4/5"))]),
    dict(no=25, pts=3, ans=1, blocks=[
        ('t', "두 학생 $rm A,~rm B$를 포함한 $6$명의 학생이 원 모양의 탁자에 일정한 간격을 두고 둘러앉을 때, "
              "$rm A$와 $rm B$가 서로 이웃하도록 앉는 경우의 수는? (단, 회전하여 일치하는 것은 같은 것으로 본다.)"),
        ('ch', N(48, 54, 60, 66, 72))]),
    dict(no=26, pts=3, ans=5, blocks=[
        ('t', "이산확률변수 $X$가 가질 수 있는 값이 $0,~1,~2$이고"),
        ('eq', "{rm P} left ( X=x right ) = {x+a} over {9} ~~ left ( x=0,~1,~2 right )"),
        ('t', "일 때, ${rm V} left ( 9X right )$의 값은? (단, $a$는 상수이다.)"),
        ('ch', N(30, 35, 40, 45, 50))]),
    dict(no=27, pts=3, ans=3, blocks=[
        ('t', "정규분포 ${rm N} left ( m,~ sigma ^{2} right )$을 따르는 모집단에서 크기가 $16$인 표본을 "
              "임의추출하여 얻은 표본평균을 이용하여 구한 모평균 $m$에 대한 신뢰도 $95 %$의 신뢰구간이"),
        ('eq', "a <= m <= b"),
        ('t', "이다. $b-a=4.9$일 때, $sigma$의 값은? (단, $Z$가 표준정규분포를 따르는 확률변수일 때, "
              "${rm P} left ( left | Z right | <= 1.96 right ) =0.95$로 계산한다.)"),
        ('ch', N(3, 4, 5, 6, 7))]),
    dict(no=28, pts=4, ans=4, blocks=[
        ('t', "$1$부터 $6$까지의 자연수가 하나씩 적혀 있는 $6$장의 카드가 들어 있는 주머니에서 임의로 "
              "$3$장의 카드를 동시에 꺼낸다. 꺼낸 카드에 적혀 있는 세 수의 합이 짝수일 때, 세 수 중 가장 큰 수와 "
              "가장 작은 수의 차가 $4$ 이상일 확률은?"),
        ('ch', F("1/5", "3/10", "2/5", "1/2", "3/5"))]),
    dict(no=29, pts=4, ans=30, blocks=[
        ('t', "숫자 $1,~1,~2,~2,~3,~3$이 하나씩 적혀 있는 $6$장의 카드를 모두 일렬로 나열할 때, "
              "같은 숫자가 적혀 있는 카드끼리는 서로 이웃하지 않도록 나열하는 경우의 수를 구하시오. "
              "(단, 같은 숫자가 적혀 있는 카드끼리는 서로 구별하지 않는다.)")]),
    dict(no=30, pts=4, ans=154, blocks=[
        ('t', "집합 $X= left lbrace 1,~2,~3,~4,~5,~6 right rbrace$에 대하여 다음 조건을 만족시키는 "
              "함수 $f:X -> X$의 개수를 구하시오."),
        ('box', ["(가) $f(1)+f(2)+f(3)=7$",
                 "(나) $f(4)<f(5)<f(6)$",
                 "(다) $f(1) <= f(4)$"])]),
]

CALC = [
    dict(no=23, pts=2, ans=4, blocks=[
        ('t', "$lim _{x -> 0} {ln (1+4x)} over {sin 2x}$의 값은?"),
        ('ch', F("1/2", "1", "3/2", "2", "5/2"))]),
    dict(no=24, pts=3, ans=2, blocks=[
        ('t', "함수 $f(x)=xe ^{2x}$에 대하여 $f'(1)$의 값은?"),
        ('ch', ["2e ^{2}", "3e ^{2}", "4e ^{2}", "5e ^{2}", "6e ^{2}"])]),
    dict(no=25, pts=3, ans=5, blocks=[
        ('t', "첫째항이 $4$인 등비수열 $left lbrace a _{n} right rbrace$에 대하여 "
              "$sum _{n=1} ^{inf} a _{n} =6$일 때, $sum _{n=1} ^{inf} left ( a _{n} right ) ^{2}$의 값은?"),
        ('ch', N(10, 12, 14, 16, 18))]),
    dict(no=26, pts=3, ans=1, blocks=[
        ('t', "$int _{0} ^{1} xe ^{x ^{2}} dx$의 값은?"),
        ('ch', ["{e-1} over {2}", "{e} over {2}", "{e+1} over {2}", "{e+2} over {2}", "{e+3} over {2}"])]),
    dict(no=27, pts=3, ans=3, blocks=[
        ('t', "그림과 같이 곡선 $y=2 sin x~(0 <= x <= pi )$와 직선 $y=1$로 둘러싸인 부분의 넓이는?"),
        ('fig', "fig_m27", 55),
        ('ch', ["2 sqrt {3} - pi", "2 sqrt {3} - {5 pi} over {6}", "2 sqrt {3} - {2 pi} over {3}",
                "2 sqrt {3} - {pi} over {2}", "2 sqrt {3} - {pi} over {3}"], 3)]),
    dict(no=28, pts=4, ans=4, blocks=[
        ('t', "함수 $f(x)= {ln x} over {x}~(x>0)$에 대하여 곡선 $y=f(x)$ 위의 점에서 그은 접선 중 "
              "원점을 지나는 접선의 기울기는?"),
        ('ch', ["{1} over {5e}", "{1} over {4e}", "{1} over {3e}", "{1} over {2e}", "{1} over {e}"])]),
    dict(no=29, pts=4, ans=80, blocks=[
        ('t', "그림과 같이 길이가 $2$인 선분 $rm AB$를 지름으로 하는 반원의 호 $rm AB$ 위의 점 $rm P$에 대하여 "
              "점 $rm P$에서 선분 $rm AB$에 내린 수선의 발을 $rm H$라 하자. $angle rm PAB = theta$일 때, "
              "삼각형 $rm PHB$의 넓이를 $f( theta )$, 선분 $rm PB$와 호 $rm PB$로 둘러싸인 부분의 넓이를 "
              "$g( theta )$라 하자."),
        ('eq', "lim _{theta -> 0+} {f( theta )+g( theta )} over {theta ^{3}} =k"),
        ('t', "일 때, $30k$의 값을 구하시오. (단, $0< theta < {pi} over {2}$)"),
        ('fig', "fig_m29", 55)]),
    dict(no=30, pts=4, ans=104, blocks=[
        ('t', "양수 $a$에 대하여 함수 $f(x)$를"),
        ('eq', "f(x)= int _{0} ^{x} (a-t)e ^{t} dt"),
        ('t', "라 하자. 함수 $f(x)$의 최댓값이 $e ^{2} -3$일 때,"),
        ('eq', "int _{0} ^{a} f(x)dx=pe ^{2} +q"),
        ('t', "이다. $p ^{2} +q ^{2}$의 값을 구하시오. (단, $p,~q$는 유리수이다.)")]),
]

GEOM = [
    dict(no=23, pts=2, ans=1, blocks=[
        ('t', "두 벡터 $vec {a} = left ( 3,~1 right ),~ vec {b} = left ( 1,~-2 right )$에 대하여 "
              "벡터 $vec {a} +2 vec {b}$의 크기는?"),
        ('ch', ["sqrt {34}", "6", "sqrt {38}", "2 sqrt {10}", "sqrt {42}"])]),
    dict(no=24, pts=3, ans=5, blocks=[
        ('t', "좌표공간의 두 점 ${rm A} left ( 1,~3,~-2 right ),~ {rm B} left ( 4,~-3,~7 right )$에 대하여 "
              "선분 $rm AB$를 $1:2$로 내분하는 점의 좌표를 $left ( a,~b,~c right )$라 할 때, $a+b+c$의 값은?"),
        ('ch', N(0, 1, 2, 3, 4))]),
    dict(no=25, pts=3, ans=2, blocks=[
        ('t', "타원 ${x ^{2}} over {8} + {y ^{2}} over {2} =1$ 위의 점 $left ( 2,~1 right )$에서의 접선과 "
              "$x$축 및 $y$축으로 둘러싸인 부분의 넓이는?"),
        ('ch', N(3, 4, 5, 6, 7))]),
    dict(no=26, pts=3, ans=4, blocks=[
        ('t', "그림과 같이 두 초점이 $rm F,~rm F'$인 쌍곡선 ${x ^{2}} over {9} - {y ^{2}} over {16} =1$ 위의 "
              "제$1$사분면에 있는 점 $rm P$에 대하여 $overline {rm PF'} =10$일 때, 삼각형 $rm PF'F$의 둘레의 "
              "길이는? (단, 점 $rm F$의 $x$좌표는 양수이다.)"),
        ('fig', "fig_g26", 60),
        ('ch', N(18, 20, 22, 24, 26))]),
    dict(no=27, pts=3, ans=3, blocks=[
        ('t', "초점이 $rm F$인 포물선 $y ^{2} =4x$ 위의 점 $rm P$에서 포물선의 준선에 내린 수선의 발을 "
              "$rm H$라 하자. 삼각형 $rm PHF$가 정삼각형일 때, 선분 $rm PF$의 길이는?"),
        ('ch', N(2, 3, 4, 5, 6))]),
    dict(no=28, pts=4, ans=5, blocks=[
        ('t', "그림과 같이 평면 $alpha$ 위에 한 변의 길이가 $4$인 정사각형 $rm ABCD$가 있다. 점 $rm A$를 "
              "지나고 평면 $alpha$에 수직인 직선 위의 점 $rm P$에 대하여 $overline {rm PA} =4$이다. "
              "평면 $rm PBD$와 평면 $alpha$가 이루는 예각의 크기를 $theta$라 할 때, $cos theta$의 값은?"),
        ('fig', "fig_g28", 50),
        ('ch', ["{sqrt {3}} over {6}", "{sqrt {2}} over {4}", "{sqrt {6}} over {6}", "{sqrt {3}} over {4}",
                "{sqrt {3}} over {3}"])]),
    dict(no=29, pts=4, ans=13, blocks=[
        ('t', "좌표평면 위의 두 점 ${rm A} left ( 2,~0 right ),~ {rm B} left ( 0,~4 right )$에 대하여 "
              "$left | vec {rm PA} + vec {rm PB} right | =4$를 만족시키는 점 $rm P$가 있다. "
              "$left | vec {rm OP} right | ^{2}$의 최댓값이 $a+b sqrt {5}$일 때, $a+b$의 값을 구하시오. "
              "(단, $rm O$는 원점이고, $a,~b$는 자연수이다.)")]),
    dict(no=30, pts=4, ans=35, blocks=[
        ('t', "좌표공간에서 구"),
        ('eq', "S:left ( x-1 right ) ^{2} + left ( y-2 right ) ^{2} + left ( z+1 right ) ^{2} =29"),
        ('t', "와 평면 $alpha :4y+3z=15$가 만나서 생기는 원을 $C$라 하자. 원 $C$의 $xy$평면 위로의 정사영의 "
              "넓이를 $S _{1}$, $zx$평면 위로의 정사영의 넓이를 $S _{2}$라 할 때, ${S _{1} +S _{2}} over {pi}$의 "
              "값을 구하시오.")]),
]

SUBJECTS = [("확률과 통계", STATS), ("미적분", CALC), ("기하", GEOM)]

# 쪽 배치: (왼쪽 단 항목, 오른쪽 단 항목). 항목은 문항 번호, 'MC'(5지선다형 표시), 'SA'(단답형 표시)
COMMON_LAYOUT = [
    (['MC', 1, 2], [3, 4]),
    ([5, 6], [7]),
    ([8, 9], [10]),
    ([11], [12]),
    ([13], [14]),
    ([15], ['SA', 16, 17]),
    ([18, 19], [20]),
    ([21], [22]),
]
ELECTIVE_LAYOUT = [
    (['MC', 23], [24]),
    ([25], [26]),
    ([27], [28]),
    (['SA', 29], [30]),
]
# 한 단에 두 번째로 오는 문항의 번호 위치(쪽 위에서부터 pt) — 원본 수능 문제지 실측값
SECOND_TARGET = {2: 623, 4: 623, 6: 576, 9: 603, 17: 665, 19: 603}
