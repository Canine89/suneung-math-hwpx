"""수학 영역 모의 문제지 문항 데이터.

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
    "out_name": "수학영역_문제지",
}

N = lambda *xs: [str(x) for x in xs]  # 숫자 보기
F = lambda *xs: ["{%s} over {%s}" % tuple(x.split("/")) if "/" in x else x for x in xs]  # 분수 보기

COMMON = [
    dict(no=1, pts=2, ans=3, blocks=[
        ('t', "$left ( 2 ^{sqrt {3}} right ) ^{sqrt {3}} TIMES 4 ^{- {1} over {2}}$의 값은?"),
        ('ch', N(1, 2, 4, 8, 16))]),
    dict(no=2, pts=2, ans=2, blocks=[
        ('t', "함수 $f(x)=x ^{3} -2x ^{2} +5$에 대하여 $lim _{h -> 0} {f(2+h)-f(2)} over {h}$의 값은?"),
        ('ch', N(2, 4, 6, 8, 10))]),
    dict(no=3, pts=3, ans=4, blocks=[
        ('t', "공비가 양수인 등비수열 $left lbrace a _{n} right rbrace$에 대하여 "
              "$a _{1} =2$, $a _{5} =4a _{3}$일 때, $a _{4}$의 값은?"),
        ('ch', N(4, 8, 12, 16, 20))]),
    dict(no=4, pts=3, ans=2, blocks=[
        ('t', "함수"),
        ('eq', "f(x)= cases{x ^{3} -a ~~~~~~ & (x<2)#ax+2 & (x >= 2)}"),
        ('t', "이 실수 전체의 집합에서 연속일 때, 상수 $a$의 값은?"),
        ('ch', N(1, 2, 3, 4, 5))]),
    dict(no=5, pts=3, ans=5, blocks=[
        ('t', "함수 $f(x)= left ( x ^{2} +1 right ) left ( 2x-3 right )$에 대하여 $f'(2)$의 값은?"),
        ('ch', N(6, 8, 10, 12, 14))]),
    dict(no=6, pts=3, ans=4, blocks=[
        ('t', "$pi < theta < {3} over {2} pi$인 $theta$에 대하여 "
              "$cos left ( {pi} over {2} + theta right ) = {3} over {5}$일 때, $tan theta$의 값은?"),
        ('ch', ["- {4} over {3}", "- {3} over {4}", "{3} over {5}", "{3} over {4}", "{4} over {3}"])]),
    dict(no=7, pts=3, ans=1, blocks=[
        ('t', "곡선 $y=x ^{2} -2x$와 직선 $y=x$로 둘러싸인 부분의 넓이는?"),
        ('ch', F("9/2", "5", "11/2", "6", "13/2")),
        ('fig', "fig_c07", 60)]),
    dict(no=8, pts=3, ans=1, blocks=[
        ('t', "$1$보다 큰 두 실수 $a,~b$가"),
        ('eq', "log _{a} b=2,~~~~ log _{2} ab=9"),
        ('t', "를 만족시킬 때, $a+b$의 값은?"),
        ('ch', N(72, 74, 76, 78, 80))]),
    dict(no=9, pts=4, ans=5, blocks=[
        ('t', "함수 $f(x)=x ^{3} -3x ^{2} -9x+k$에 대하여 곡선 $y=f(x)$ 위의 점 중 함수 $f(x)$가 "
              "극대가 되는 점을 $rm A$, 극소가 되는 점을 $rm B$라 하자. 선분 $rm AB$의 중점이 "
              "$x$축 위에 있을 때, 상수 $k$의 값은?"),
        ('ch', N(3, 5, 7, 9, 11))]),
    dict(no=10, pts=4, ans=3, blocks=[
        ('t', "두 양수 $a,~b$에 대하여 $0 <= x <= {2 pi} over {b}$에서 정의된 함수 "
              "$f(x)=a sin bx$가 있다. 곡선 $y=f(x)$와 직선 $y= {a} over {2}$가 만나는 두 점을 "
              "$rm A,~rm B$라 하고, 함수 $f(x)$가 최솟값을 갖는 $x$의 값을 $c$라 할 때 "
              "점 $left ( c,~f(c) right )$를 $rm C$라 하자. $overline {rm AB} =4$이고 삼각형 $rm ABC$의 "
              "넓이가 $18$일 때, $a TIMES b$의 값은?"),
        ('ch', ["{pi} over {3}", "{2 pi} over {3}", "pi", "{4 pi} over {3}", "{5 pi} over {3}"]),
        ('fig', "fig_c10", 70)]),
    dict(no=11, pts=4, ans=4, blocks=[
        ('t', "시각 $t=0$일 때 동시에 원점을 출발하여 수직선 위를 움직이는 두 점 $rm P,~rm Q$의 "
              "시각 $t~(t >= 0)$에서의 속도가 각각"),
        ('eq', "v _{1} (t)=3t ^{2} -6t,~~~~ v _{2} (t)=2t"),
        ('t', "이다. 출발한 후 두 점 $rm P,~rm Q$가 처음으로 만나는 시각을 $k$라 할 때, "
              "시각 $t=0$에서 $t=k$까지 점 $rm P$가 움직인 거리는?"),
        ('ch', N(18, 20, 22, 24, 26))]),
    dict(no=12, pts=4, ans=2, blocks=[
        ('t', "공차가 $0$이 아닌 등차수열 $left lbrace a _{n} right rbrace$에 대하여"),
        ('eq', "left | a _{3} right | =a _{9} ,~~~~ sum _{k=1} ^{4} {1} over {a _{k} a _{k+1}} = {1} over {20}"),
        ('t', "일 때, $sum _{k=1} ^{12} a _{k}$의 값은?"),
        ('ch', N(20, 24, 28, 32, 36))]),
    dict(no=13, pts=4, ans=1, blocks=[
        ('t', "두 상수 $a,~b$에 대하여 함수 $f(x)=x ^{3} +ax ^{2} +bx$가 다음 조건을 만족시킨다."),
        ('box', ["(가) 곡선 $y=f(x)$ 위의 점 $left ( 1,~f(1) right )$에서의 접선이 원점을 지난다.",
                 "(나) 함수 $f(x)$는 $x=-1$에서 극값을 갖는다."]),
        ('t', "$f(2)$의 값은?"),
        ('ch', N(-14, -12, -10, -8, -6))]),
    dict(no=14, pts=4, ans=5, blocks=[
        ('t', "그림과 같이 $overline {rm AB} =6,~ overline {rm AC} =4,~ cos left ( angle rm BAC right ) = {1} over {3}$"
              "인 삼각형 $rm ABC$가 있다. 삼각형 $rm ABC$의 외접원 위의 점 중 점 $rm A$를 포함하지 않는 "
              "호 $rm BC$ 위의 점 $rm D$에 대하여 $overline {rm BD} = overline {rm CD}$일 때, "
              "사각형 $rm ABDC$의 넓이는?"),
        ('fig', "fig_c14", 55),
        ('ch', ["{21 sqrt {2}} over {2}", "11 sqrt {2}", "{23 sqrt {2}} over {2}", "12 sqrt {2}",
                "{25 sqrt {2}} over {2}"])]),
    dict(no=15, pts=4, ans=3, blocks=[
        ('t', "최고차항의 계수가 $1$인 삼차함수 $f(x)$가 다음 조건을 만족시킨다."),
        ('box', ["(가) $lim _{x -> 1} {f(x)} over {x-1} =-3$",
                 "(나) 곡선 $y=f(x)$ 위의 점 $left ( 3,~f(3) right )$에서의 접선이 점 $left ( 1,~0 right )$을 지난다."]),
        ('t', "$f(4)$의 값은?"),
        ('ch', N(-22, -20, -18, -16, -14))]),
    # ---------------- 단답형 ----------------
    dict(no=16, pts=3, ans=6, blocks=[
        ('t', "방정식"),
        ('eq', "log _{2} (x+2)+ log _{2} (x-2)=5"),
        ('t', "를 만족시키는 실수 $x$의 값을 구하시오.")]),
    dict(no=17, pts=3, ans=16, blocks=[
        ('t', "함수 $f(x)$에 대하여 $f'(x)=6x ^{2} -4x+3$이고 $f(1)=5$일 때, $f(2)$의 값을 구하시오.")]),
    dict(no=18, pts=3, ans=70, blocks=[
        ('t', "수열 $left lbrace a _{n} right rbrace$에 대하여 $sum _{k=1} ^{10} left ( 2a _{k} +3 right ) =60$일 때, "
              "$sum _{k=1} ^{10} left ( a _{k} +k right )$의 값을 구하시오.")]),
    dict(no=19, pts=3, ans=26, blocks=[
        ('t', "$x$에 대한 방정식 $2x ^{3} -3x ^{2} -12x+k=0$이 서로 다른 세 실근을 갖도록 하는 "
              "정수 $k$의 개수를 구하시오.")]),
    dict(no=20, pts=4, ans=190, blocks=[
        ('t', "모든 항이 자연수인 수열 $left lbrace a _{n} right rbrace$이 모든 자연수 $n$에 대하여"),
        ('eq', 'a _{n+1} = cases{a _{n} +3 ~~~~ & left ( a _{n} "이"~"홀수인"~"경우" right )#'
               '{a _{n}} over {2} & left ( a _{n} "이"~"짝수인"~"경우" right )}'),
        ('t', "를 만족시킨다. $a _{5} =5$가 되도록 하는 모든 $a _{1}$의 값의 합을 구하시오.")]),
    dict(no=21, pts=4, ans=100, blocks=[
        ('t', "$1$보다 큰 실수 $a$와 실수 $k$에 대하여 직선 $y=-x+k$가 두 곡선 $y=a ^{x}$, "
              "$y= log _{a} x$와 만나는 점을 각각 $rm A,~rm B$라 하자. 점 $rm A$의 $x$좌표가 점 $rm B$의 "
              "$x$좌표보다 작고, $overline {rm AB} =4 sqrt {2}$이며 삼각형 $rm OAB$의 넓이가 $16$일 때, "
              "$a ^{4} +k ^{2}$의 값을 구하시오. (단, $rm O$는 원점이다.)")]),
    dict(no=22, pts=4, ans=73, blocks=[
        ('t', "최고차항의 계수가 $1$인 삼차함수 $f(x)$와 실수 $t$에 대하여 $x$에 대한 방정식 "
              "$f(x)=t$의 서로 다른 실근의 개수를 $g(t)$라 하자. 최고차항의 계수가 $1$인 이차함수 "
              "$h(t)$에 대하여 두 함수 $f(x),~h(t)$가 다음 조건을 만족시킨다."),
        ('box', ["(가) 함수 $g(t)h(t)$는 실수 전체의 집합에서 연속이다.",
                 "(나) 함수 $g(t)$는 $t=2$에서 불연속이고, $h(0)=-4$이다.",
                 "(다) $f'(0)=0$이고 $f(0)>0$이다."]),
        ('t', "$f(5)+h(5)$의 값을 구하시오.")]),
]

STATS = [
    dict(no=23, pts=2, ans=5, blocks=[
        ('t', "다섯 개의 문자 $a,~a,~b,~b,~c$를 모두 일렬로 나열하는 경우의 수는?"),
        ('ch', N(10, 15, 20, 25, 30))]),
    dict(no=24, pts=3, ans=4, blocks=[
        ('t', "다항식 $left ( x ^{2} + {2} over {x} right ) ^{6}$의 전개식에서 $x ^{3}$의 계수는?"),
        ('ch', N(100, 120, 140, 160, 180))]),
    dict(no=25, pts=3, ans=1, blocks=[
        ('t', "흰 공 $3$개와 검은 공 $4$개가 들어 있는 주머니에서 임의로 $2$개의 공을 동시에 꺼낸다. "
              "꺼낸 $2$개의 공이 서로 같은 색일 때, 꺼낸 공이 모두 흰 공일 확률은?"),
        ('ch', F("1/3", "5/12", "1/2", "7/12", "2/3"))]),
    dict(no=26, pts=3, ans=3, blocks=[
        ('t', "이항분포 ${rm B} left ( n,~p right )$를 따르는 확률변수 $X$에 대하여"),
        ('eq', "{rm E} left ( 3X+1 right ) =31,~~~~ {rm V} left ( 3X+1 right ) =60"),
        ('t', "일 때, $n$의 값은?"),
        ('ch', N(24, 27, 30, 33, 36))]),
    dict(no=27, pts=3, ans=2, manual_pts=True, blocks=[
        ('t', "확률변수 $X$가 정규분포 ${rm N} left ( m,~2 ^{2} right )$을 따르고"),
        ('side', ["${rm P} left ( X <= 10 right ) = {rm P} left ( X >= 14 right )$",
                  "일 때, ${rm P} left ( 9 <= X <= 13 right )$의",
                  "값을 오른쪽 표준정규분포표를",
                  "이용하여 구한 것은? [3점]"],
         [("0.5", "0.1915"), ("1.0", "0.3413"), ("1.5", "0.4332"), ("2.0", "0.4772")]),
        ('ch', ["0.5328", "0.6247", "0.6687", "0.7745", "0.8185"])]),
    dict(no=28, pts=4, ans=4, blocks=[
        ('t', "숫자 $1,~2,~3,~4,~5$ 중에서 중복을 허락하여 $4$개를 택해 일렬로 나열하여 만들 수 있는 "
              "모든 네 자리의 자연수 중에서 다음 조건을 만족시키는 자연수의 개수는?"),
        ('box', ["(가) 각 자리의 수의 합은 짝수이다.",
                 "(나) 숫자 $3$이 한 개 이상 포함되어 있다."]),
        ('ch', N(170, 175, 180, 185, 190))]),
    dict(no=29, pts=4, ans=61, blocks=[
        ('t', "한 개의 주사위를 세 번 던져 나오는 눈의 수를 차례로 $a,~b,~c$라 할 때, "
              "$a <= b <= c$이고 $a+b+c$가 짝수일 확률은 ${q} over {p}$이다. $p+q$의 값을 구하시오. "
              "(단, $p$와 $q$는 서로소인 자연수이다.)")]),
    dict(no=30, pts=4, ans=35, blocks=[
        ('t', "집합 $X= left lbrace 1,~2,~3,~4,~5 right rbrace$에 대하여 다음 조건을 만족시키는 "
              "함수 $f:X -> X$의 개수를 구하시오."),
        ('box', ["(가) $f(1) <= f(2) <= f(3)$",
                 "(나) $f(3)<f(4)$",
                 "(다) $f(5)=f(1)+f(4)-f(3)$"])]),
]

CALC = [
    dict(no=23, pts=2, ans=1, blocks=[
        ('t', "$lim _{x -> 0} {e ^{3x} -1} over {ln (1+2x)}$의 값은?"),
        ('ch', F("3/2", "2", "5/2", "3", "7/2"))]),
    dict(no=24, pts=3, ans=2, blocks=[
        ('t', "매개변수 $t$로 나타내어진 곡선"),
        ('eq', "x=t ^{2} +1,~~~~ y=t ^{3} -2t"),
        ('t', "에서 $t=2$일 때, ${dy} over {dx}$의 값은?"),
        ('ch', F("2", "5/2", "3", "7/2", "4"))]),
    dict(no=25, pts=3, ans=5, blocks=[
        ('t', "수열 $left lbrace a _{n} right rbrace$에 대하여 "
              "$sum _{n=1} ^{inf} left ( {a _{n}} over {n} -3 right ) =2$일 때, "
              "$lim _{n -> inf} {a _{n} +2n} over {n+1}$의 값은?"),
        ('ch', N(1, 2, 3, 4, 5))]),
    dict(no=26, pts=3, ans=3, blocks=[
        ('t', "그림과 같이 곡선 $y= sqrt {x} e ^{x}$와 $x$축 및 직선 $x=1$로 둘러싸인 부분을 밑면으로 하는 "
              "입체도형이 있다. 이 입체도형을 $x$축에 수직인 평면으로 자른 단면이 모두 정사각형일 때, "
              "이 입체도형의 부피는?"),
        ('fig', "fig_m26", 60),
        ('ch', ["{e ^{2} -1} over {4}", "{e ^{2}} over {4}", "{e ^{2} +1} over {4}",
                "{e ^{2} +2} over {4}", "{e ^{2} +3} over {4}"])]),
    dict(no=27, pts=3, ans=4, blocks=[
        ('t', "곡선 $x ^{2} +xy+y ^{2} =7$ 위의 점 $left ( 1,~2 right )$에서의 접선의 기울기는?"),
        ('ch', ["- {7} over {5}", "- {6} over {5}", "-1", "- {4} over {5}", "- {3} over {5}"])]),
    dict(no=28, pts=4, ans=2, blocks=[
        ('t', "함수 $f(x)=e ^{x} +x$의 역함수를 $g(x)$라 할 때, $int _{1} ^{e+1} g(x)dx$의 값은?"),
        ('ch', F("5/4", "3/2", "7/4", "2", "9/4"))]),
    dict(no=29, pts=4, ans=100, blocks=[
        ('t', "그림과 같이 반지름의 길이가 $2$이고 중심각의 크기가 ${pi} over {2}$인 부채꼴 $rm OAB$가 있다. "
              "호 $rm AB$ 위의 점 $rm P$에 대하여 점 $rm P$에서 선분 $rm OA$에 내린 수선의 발을 $rm H$, "
              "점 $rm P$에서 호 $rm AB$에 접하는 직선이 직선 $rm OA$와 만나는 점을 $rm T$라 하자. "
              "$angle rm POA = theta$일 때, 선분 $rm AT$, 선분 $rm TP$와 호 $rm PA$로 둘러싸인 부분의 "
              "넓이를 $f( theta )$, 삼각형 $rm PHA$의 넓이를 $g( theta )$라 하자. "
              "$lim _{theta -> 0+} {f( theta )+g( theta )} over {theta ^{3}} =k$일 때, $60k$의 값을 구하시오. "
              "(단, $0< theta < {pi} over {2}$)"),
        ('fig', "fig_m29", 55)]),
    dict(no=30, pts=4, ans=12, blocks=[
        ('t', "최고차항의 계수가 $1$인 이차함수 $f(x)$에 대하여 함수 $g(x)=f(x)e ^{-x}$가 다음 조건을 "
              "만족시킨다."),
        ('box', ["(가) 함수 $g(x)$는 $x=1$에서 극대이다.",
                 "(나) 곡선 $y=g(x)$의 모든 변곡점의 $x$좌표의 합은 $2$이다."]),
        ('t', "$int _{-1} ^{1} g(x)dx=pe+ {q} over {e}$일 때, $p-q$의 값을 구하시오. "
              "(단, $p,~q$는 유리수이다.)")]),
]

GEOM = [
    dict(no=23, pts=2, ans=5, blocks=[
        ('t', "좌표공간의 점 ${rm A} left ( 1,~2,~3 right )$을 $xy$평면에 대하여 대칭이동한 점을 $rm B$, "
              "점 $rm A$를 $yz$평면에 대하여 대칭이동한 점을 $rm C$라 할 때, 선분 $rm BC$의 길이는?"),
        ('ch', ["2 sqrt {6}", "2 sqrt {7}", "4 sqrt {2}", "6", "2 sqrt {10}"])]),
    dict(no=24, pts=3, ans=2, blocks=[
        ('t', "포물선 $y ^{2} =8x$의 초점을 $rm F$라 하자. 포물선 위의 점 $rm P$에 대하여 "
              "$overline {rm PF} =6$일 때, 선분 $rm OP$의 길이는? (단, $rm O$는 원점이다.)"),
        ('ch', ["2 sqrt {11}", "4 sqrt {3}", "2 sqrt {13}", "2 sqrt {14}", "2 sqrt {15}"])]),
    dict(no=25, pts=3, ans=3, blocks=[
        ('t', "두 벡터 $vec {a} = left ( 2,~1 right ),~ vec {b} = left ( 1,~-3 right )$에 대하여 "
              "$left | vec {a} +t vec {b} right |$의 최솟값은? (단, $t$는 실수이다.)"),
        ('ch', ["{sqrt {10}} over {2}", "{3 sqrt {10}} over {5}", "{7 sqrt {10}} over {10}",
                "{4 sqrt {10}} over {5}", "{9 sqrt {10}} over {10}"])]),
    dict(no=26, pts=3, ans=4, blocks=[
        ('t', "그림과 같이 두 초점이 $rm F,~rm F'$인 타원 ${x ^{2}} over {25} + {y ^{2}} over {9} =1$ 위의 "
              "점 $rm P$에 대하여 $angle rm FPF' = {pi} over {2}$일 때, 삼각형 $rm PFF'$의 넓이는?"),
        ('fig', "fig_g26", 60),
        ('ch', N(6, 7, 8, 9, 10))]),
    dict(no=27, pts=3, ans=1, blocks=[
        ('t', "쌍곡선 ${x ^{2}} over {4} - {y ^{2}} over {12} =1$ 위의 점 $left ( 4,~6 right )$에서의 접선이 "
              "점 $left ( a,~10 right )$을 지날 때, $a$의 값은?"),
        ('ch', N(6, 7, 8, 9, 10))]),
    dict(no=28, pts=4, ans=5, blocks=[
        ('t', "그림과 같이 한 모서리의 길이가 $6$인 정사면체 $rm ABCD$가 있다. "
              "삼각형 $rm BCD$의 평면 $rm ABC$ 위로의 정사영의 넓이는?"),
        ('fig', "fig_g28", 50),
        ('ch', ["sqrt {3}", "{3 sqrt {3}} over {2}", "2 sqrt {3}", "{5 sqrt {3}} over {2}", "3 sqrt {3}"])]),
    dict(no=29, pts=4, ans=32, blocks=[
        ('t', "좌표평면 위의 두 점 ${rm A} left ( 7,~1 right ),~ {rm B} left ( 1,~7 right )$과 "
              "원 $left ( x-1 right ) ^{2} + left ( y-1 right ) ^{2} =8$ 위의 점 $rm P$에 대하여 "
              "$vec {rm PA} cdot vec {rm PB}$의 최댓값을 구하시오.")]),
    dict(no=30, pts=4, ans=37, blocks=[
        ('t', "좌표공간에서 구 $S:x ^{2} +y ^{2} +z ^{2} =9$와 점 ${rm A} left ( 0,~0,~6 right )$이 있다. "
              "점 $rm A$에서 구 $S$에 그은 접선이 구 $S$와 만나는 점 전체의 집합을 $C$라 하자. "
              "$C$에 속하는 점 $rm P$와 점 ${rm B} left ( 4,~0,~0 right )$에 대하여 "
              "$overline {rm BP} ^{2}$의 최댓값이 $a+b sqrt {3}$일 때, $a+b$의 값을 구하시오. "
              "(단, $a,~b$는 자연수이다.)")]),
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
