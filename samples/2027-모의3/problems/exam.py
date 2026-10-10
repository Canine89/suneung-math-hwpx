"""수학 영역 모의 문제지 문항 데이터 (3회).

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
    "out_name": "수학영역_문제지_3회",
}

N = lambda *xs: [str(x) for x in xs]  # 숫자 보기
F = lambda *xs: ["{%s} over {%s}" % tuple(x.split("/")) if "/" in x else x for x in xs]  # 분수 보기

COMMON = [
    dict(no=1, pts=2, ans=3, blocks=[
        ('t', "$left ( {1} over {4} right ) ^{- {3} over {2}} TIMES 2 ^{-1}$의 값은?"),
        ('ch', N(1, 2, 4, 8, 16))]),
    dict(no=2, pts=2, ans=2, blocks=[
        ('t', "$lim _{x -> inf} {2x ^{2} +3x} over {x ^{2} -1}$의 값은?"),
        ('ch', N(1, 2, 3, 4, 5))]),
    dict(no=3, pts=3, ans=4, blocks=[
        ('t', "등비수열 $left lbrace a _{n} right rbrace$에 대하여 $a _{1} =3$, $a _{4} =24$일 때, "
              "$a _{2} +a _{3}$의 값은? (단, 공비는 실수이다.)"),
        ('ch', N(12, 14, 16, 18, 20))]),
    dict(no=4, pts=3, ans=5, blocks=[
        ('t', "두 함수 $f(x)=x ^{2} -3x$, $g(x)=(x+1)f(x)$에 대하여 $g'(2)$의 값은?"),
        ('ch', N(-3, -2, -1, 0, 1))]),
    dict(no=5, pts=3, ans=5, blocks=[
        ('t', "${pi} over {2} < theta < pi$인 $theta$에 대하여 $cos left ( pi + theta right ) = {1} over {3}$일 때, "
              "$sin theta$의 값은?"),
        ('ch', ["{sqrt {2}} over {3}", "{sqrt {3}} over {3}", "{2} over {3}", "{sqrt {5}} over {3}",
                "{2 sqrt {2}} over {3}"])]),
    dict(no=6, pts=3, ans=1, blocks=[
        ('t', "$int _{0} ^{3} left | x-1 right | dx$의 값은?"),
        ('ch', F("5/2", "3", "7/2", "4", "9/2"))]),
    dict(no=7, pts=3, ans=4, blocks=[
        ('t', "두 실수 $a,~b$가 $3 ^{a} =5$, $5 ^{b} =9$를 만족시킬 때, $ab$의 값은?"),
        ('ch', F("1/2", "1", "3/2", "2", "5/2"))]),
    dict(no=8, pts=3, ans=2, blocks=[
        ('t', "곡선 $y=x ^{3} -2x+1$ 위의 점 $left ( 1,~0 right )$에서의 접선이 점 $left ( a,~3 right )$을 "
              "지날 때, $a$의 값은?"),
        ('ch', N(3, 4, 5, 6, 7))]),
    dict(no=9, pts=4, ans=1, blocks=[
        ('t', "세 상수 $a$, $b$, $c$에 대하여 함수 $f(x)=a cos bx+c$의 그래프가 그림과 같다. "
              "함수 $f(x)$의 최댓값은 $5$, 최솟값은 $-1$이고, 곡선 $y=f(x)$와 직선 $y=2$가 만나는 점 중 "
              "$x$좌표가 양수인 점의 $x$좌표의 최솟값이 ${pi} over {4}$일 때, $a TIMES b TIMES c$의 값은? "
              "(단, $a>0$, $b>0$)"),
        ('fig', "fig_c09", 60),
        ('ch', N(12, 14, 16, 18, 20))]),
    dict(no=10, pts=4, ans=5, blocks=[
        ('t', "그림과 같이 곡선 $y=-x ^{2} +4x$와 $x$축으로 둘러싸인 부분의 넓이가 직선 $y=mx$에 의하여 "
              "이등분될 때, $left ( 4-m right ) ^{3}$의 값은? (단, $0<m<4$)"),
        ('fig', "fig_c10", 55),
        ('ch', N(16, 20, 24, 28, 32))]),
    dict(no=11, pts=4, ans=1, blocks=[
        ('t', "자연수 $n$에 대하여"),
        ('eq', "sum _{k=1} ^{n} {1} over {sqrt {k+1} + sqrt {k}} =4"),
        ('t', "일 때, $n$의 값은?"),
        ('ch', N(24, 25, 26, 27, 28))]),
    dict(no=12, pts=4, ans=2, blocks=[
        ('t', "시각 $t=0$일 때 동시에 원점을 출발하여 수직선 위를 움직이는 두 점 $rm P,~rm Q$의 "
              "시각 $t~(t >= 0)$에서의 위치가 각각"),
        ('eq', "x _{1} =t ^{3} -3t ^{2} ,~~~~ x _{2} =3t ^{2} -9t"),
        ('t', "이다. $t>0$에서 두 점 $rm P,~rm Q$의 속도가 같아지는 모든 시각에서의 두 점 사이의 거리의 합은?"),
        ('ch', N(3, 4, 5, 6, 7))]),
    dict(no=13, pts=4, ans=4, blocks=[
        ('t', "그림과 같이 $4$보다 큰 실수 $k$에 대하여 직선 $x=k$가 두 곡선 $y= log _{2} x$, "
              "$y= log _{2} (x-4)$와 만나는 점을 각각 $rm A,~rm B$라 하자. 점 $rm A$를 지나고 $x$축에 평행한 "
              "직선이 곡선 $y= log _{2} (x-4)$와 만나는 점을 $rm C$라 하자. $overline {rm AB} =1$일 때, "
              "삼각형 $rm ABC$의 넓이는?"),
        ('fig', "fig_c13", 55),
        ('ch', F("1/2", "1", "3/2", "2", "5/2"))]),
    dict(no=14, pts=4, ans=3, blocks=[
        ('t', "그림과 같이 $overline {rm AB} =4$, $overline {rm AC} =6$, $cos left ( angle rm BAC right ) "
              "= {1} over {4}$인 삼각형 $rm ABC$의 외접원의 넓이는?"),
        ('fig', "fig_c14", 50),
        ('ch', ["{28} over {3} pi", "10 pi", "{32} over {3} pi", "{34} over {3} pi", "12 pi"])]),
    dict(no=15, pts=4, ans=3, blocks=[
        ('t', "최고차항의 계수가 $1$인 이차함수 $f(x)$와 실수 $t$에 대하여 함수 $h(t)$를"),
        ('eq', "h(t)= int _{t} ^{t+2} f(x)dx"),
        ('t', "라 하자. 함수 $h(t)$가 다음 조건을 만족시킨다."),
        ('box', ["(가) 함수 $h(t)$는 $t=1$에서 최솟값을 갖는다.",
                 "(나) $h(1)= {2} over {3}$"]),
        ('t', "$f(5)+h(0)$의 값은?"),
        ('ch', ["11", "{34} over {3}", "{35} over {3}", "12", "{37} over {3}"])]),
    # ---------------- 단답형 ----------------
    dict(no=16, pts=3, ans=3, blocks=[
        ('t', "방정식 $log _{3} (x+6)=2 log _{3} x$를 만족시키는 실수 $x$의 값을 구하시오.")]),
    dict(no=17, pts=3, ans=10, blocks=[
        ('t', "$int _{0} ^{2} left ( 3x ^{2} +2x-1 right ) dx$의 값을 구하시오.")]),
    dict(no=18, pts=3, ans=100, blocks=[
        ('t', "수열 $left lbrace a _{n} right rbrace$에 대하여 $sum _{k=1} ^{10} a _{k} =20$, "
              "$sum _{k=1} ^{10} {a _{k}} ^{2} =50$일 때, $sum _{k=1} ^{10} left ( a _{k} +1 right ) ^{2}$의 값을 "
              "구하시오.")]),
    dict(no=19, pts=3, ans=28, blocks=[
        ('t', "닫힌구간 $left [ -2,~4 right ]$에서 함수 $f(x)=-x ^{3} +3x ^{2} +9x+1$의 최댓값을 구하시오.")]),
    dict(no=20, pts=4, ans=79, blocks=[
        ('t', "수열 $left lbrace a _{n} right rbrace$이 $a _{1} =1$이고, 모든 자연수 $n$에 대하여"),
        ('eq', 'a _{n+1} = cases{{a _{n}} over {2} ~~~~ & left ( a _{n} "이"~"짝수인"~"경우" right )#'
               'a _{n} +5 & left ( a _{n} "이"~"홀수인"~"경우" right )}'),
        ('t', "를 만족시킬 때, $sum _{k=1} ^{20} a _{k}$의 값을 구하시오.")]),
    dict(no=21, pts=4, ans=9, blocks=[
        ('t', "$0 <= x < 2 pi$일 때, $x$에 대한 방정식"),
        ('eq', "left | 3 sin x-1 right | =k"),
        ('t', "의 서로 다른 실근의 개수가 $3$이 되도록 하는 실수 $k$에 대하여, 이 방정식의 모든 실근의 합은 "
              "${q} over {p} pi$이다. $p+q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.)")]),
    dict(no=22, pts=4, ans=70, blocks=[
        ('t', "최고차항의 계수가 $1$인 삼차함수 $f(x)$와 양수 $a$에 대하여 함수 $g(x)$를"),
        ('eq', "g(x)= cases{-f(x) ~~~~ & (x<a)#f(x) & (x >= a)}"),
        ('t', "라 하자. 함수 $g(x)$가 다음 조건을 만족시킨다."),
        ('box', ["(가) 함수 $g(x)$는 실수 전체의 집합에서 미분가능하다.",
                 "(나) 함수 $g(x)$는 $x=a+2$에서 극소이다.",
                 "(다) $g(0)=4$"]),
        ('t', "$g(-2)+g(5)$의 값을 구하시오.")]),
]

STATS = [
    dict(no=23, pts=2, ans=4, blocks=[
        ('t', "숫자 $1,~2,~3$ 중에서 중복을 허락하여 $4$개를 택해 일렬로 나열하여 만들 수 있는 "
              "네 자리의 자연수의 개수는?"),
        ('ch', N(27, 54, 64, 81, 108))]),
    dict(no=24, pts=3, ans=2, blocks=[
        ('t', "다항식 $left ( 1+2x right ) ^{5}$의 전개식에서 $x ^{3}$의 계수는?"),
        ('ch', N(60, 80, 100, 120, 140))]),
    dict(no=25, pts=3, ans=5, blocks=[
        ('t', "어느 반 학생 $30$명 중 남학생은 $18$명, 여학생은 $12$명이고, 안경을 쓴 학생은 남학생 $8$명, "
              "여학생 $6$명이다. 이 반 학생 중에서 임의로 선택한 한 명이 안경을 쓴 학생일 때, 이 학생이 "
              "여학생일 확률은?"),
        ('ch', F("1/7", "2/7", "5/14", "2/5", "3/7"))]),
    dict(no=26, pts=3, ans=1, blocks=[
        ('t', "한 개의 주사위를 $120$번 던질 때, $3$의 배수의 눈이 나오는 횟수를 확률변수 $X$라 하자. "
              "${rm V} left ( 3X right )$의 값은?"),
        ('ch', N(240, 260, 280, 300, 320))]),
    dict(no=27, pts=3, ans=3, manual_pts=True, blocks=[
        ('t', "확률변수 $X$가 정규분포 ${rm N} left ( m,~4 ^{2} right )$을 따르고"),
        ('side', ["${rm P} left ( X <= 48 right ) =0.1587$일 때,",
                  "${rm P} left ( 54 <= X <= 60 right )$의 값을",
                  "오른쪽 표준정규분포표를",
                  "이용하여 구한 것은? [3점]"],
         [("0.5", "0.1915"), ("1.0", "0.3413"), ("1.5", "0.4332"), ("2.0", "0.4772")]),
        ('ch', ["0.1359", "0.2417", "0.2857", "0.3023", "0.3830"])]),
    dict(no=28, pts=4, ans=4, blocks=[
        ('t', "한 개의 주사위를 $4$번 던질 때 나오는 눈의 수를 차례로 $a,~b,~c,~d$라 하자. "
              "$abcd$가 $4$의 배수일 확률은?"),
        ('ch', F("2/3", "35/48", "3/4", "37/48", "5/6"))]),
    dict(no=29, pts=4, ans=70, blocks=[
        ('t', "다음 조건을 만족시키는 음이 아닌 정수 $a,~b,~c,~d$의 모든 순서쌍 $left ( a,~b,~c,~d right )$의 "
              "개수를 구하시오."),
        ('box', ["(가) $a+b+c+d=12$",
                 "(나) $a >= 1$, $b >= 2$",
                 "(다) $c$와 $d$는 모두 짝수이다."])]),
    dict(no=30, pts=4, ans=18, blocks=[
        ('t', "집합 $X= left lbrace 1,~2,~3,~4,~5 right rbrace$에 대하여 다음 조건을 만족시키는 "
              "함수 $f:X -> X$의 개수를 구하시오."),
        ('box', ["(가) $f(1)+f(5)=6$",
                 "(나) $f(1)<f(2)<f(3)$",
                 "(다) 함수 $f$의 치역의 원소의 개수는 $3$이다."])]),
]

CALC = [
    dict(no=23, pts=2, ans=4, blocks=[
        ('t', "$lim _{x -> 0} {e ^{2x} -1} over {3x}$의 값은?"),
        ('ch', F("1/6", "1/3", "1/2", "2/3", "5/6"))]),
    dict(no=24, pts=3, ans=2, blocks=[
        ('t', "매개변수 $t$로 나타내어진 곡선"),
        ('eq', "x=e ^{t} +t,~~~~ y=e ^{2t}"),
        ('t', "에서 $t=0$일 때, ${dy} over {dx}$의 값은?"),
        ('ch', F("1/2", "1", "3/2", "2", "5/2"))]),
    dict(no=25, pts=3, ans=5, blocks=[
        ('t', "$lim _{n -> inf} {2 ^{n+1} +3 ^{n}} over {3 ^{n+1} -2 ^{n}}$의 값은?"),
        ('ch', F("1/9", "1/6", "1/5", "1/4", "1/3"))]),
    dict(no=26, pts=3, ans=1, blocks=[
        ('t', "$int _{0} ^{{pi} over {2}} x cos x~dx$의 값은?"),
        ('ch', ["{pi} over {2} -1", "{pi} over {2} - {1} over {2}", "{pi} over {2}", "{pi} over {2} + {1} over {2}",
                "{pi} over {2} +1"])]),
    dict(no=27, pts=3, ans=3, blocks=[
        ('t', "그림과 같이 곡선 $y= ln x$ 위의 점 $left ( e,~1 right )$에서의 접선과 곡선 $y= ln x$ 및 "
              "$x$축으로 둘러싸인 부분의 넓이는?"),
        ('fig', "fig_m27", 55),
        ('ch', ["{e-2} over {4}", "{e-2} over {3}", "{e-2} over {2}", "{e-1} over {3}", "{e-1} over {2}"])]),
    dict(no=28, pts=4, ans=1, blocks=[
        ('t', "함수 $f(x)= left ( x ^{2} +a right ) e ^{-x}$가 실수 전체의 집합에서 감소하도록 하는 실수 $a$의 "
              "최솟값을 $m$이라 하자. $a=m$일 때, 함수 $f(x)$의 역함수를 $g(x)$라 하자. "
              "$g' left ( {5} over {e ^{2}} right )$의 값은?"),
        ('ch', ["-e ^{2}", "-e", "-1", "- {1} over {e}", "- {1} over {e ^{2}}"])]),
    dict(no=29, pts=4, ans=40, blocks=[
        ('t', "그림과 같이 반지름의 길이가 $1$이고 중심각의 크기가 ${pi} over {2}$인 부채꼴 $rm OAB$가 있다. "
              "호 $rm AB$ 위의 점 $rm P$에 대하여 점 $rm P$에서 선분 $rm OB$에 내린 수선의 발을 $rm Q$, "
              "점 $rm A$에서 선분 $rm OP$에 내린 수선의 발을 $rm R$라 하자. $angle rm POA = theta$일 때, "
              "삼각형 $rm PQR$의 넓이를 $f( theta )$, 선분 $rm PA$와 호 $rm PA$로 둘러싸인 부분의 넓이를 "
              "$g( theta )$라 하자."),
        ('eq', "lim _{theta -> 0+} {f( theta )+g( theta )} over {theta ^{3}} =k"),
        ('t', "일 때, $120k$의 값을 구하시오. (단, $0< theta < {pi} over {2}$)"),
        ('fig', "fig_m29", 50)]),
    dict(no=30, pts=4, ans=30, blocks=[
        ('t', "양수 $t$에 대하여 곡선 $y=e ^{- {x} over {2}}$ 위의 점 $left ( t,~e ^{- {t} over {2}} right )$에서의 "
              "접선이 $x$축, $y$축과 만나는 점을 각각 $rm A,~rm B$라 하고, 삼각형 $rm OAB$의 넓이를 $S(t)$라 하자. "
              "함수 $S(t)$가 $t=a$에서 최댓값을 가질 때,"),
        ('eq', "int _{0} ^{a} S(t)dt=p+ {q} over {e}"),
        ('t', "이다. $p-q$의 값을 구하시오. (단, $rm O$는 원점이고, $p,~q$는 정수이다.)")]),
]

GEOM = [
    dict(no=23, pts=2, ans=5, blocks=[
        ('t', "좌표공간의 두 점 ${rm A} left ( 2,~-1,~3 right ),~ {rm B} left ( 4,~1,~2 right )$ 사이의 거리는?"),
        ('ch', ["sqrt {5}", "sqrt {6}", "sqrt {7}", "2 sqrt {2}", "3"])]),
    dict(no=24, pts=3, ans=2, blocks=[
        ('t', "두 벡터 $vec {a} ,~ vec {b}$에 대하여 $left | vec {a} right | =2$, $left | vec {b} right | =3$, "
              "$left | vec {a} - vec {b} right | = sqrt {7}$일 때, $vec {a} cdot vec {b}$의 값은?"),
        ('ch', N(2, 3, 4, 5, 6))]),
    dict(no=25, pts=3, ans=3, blocks=[
        ('t', "포물선 $y ^{2} =12x$의 초점을 $rm F$라 하자. 포물선 위의 점 $rm P$의 $y$좌표가 $6$일 때, "
              "선분 $rm PF$의 길이는?"),
        ('ch', N(4, 5, 6, 7, 8))]),
    dict(no=26, pts=3, ans=4, blocks=[
        ('t', "그림과 같이 두 초점이 $rm F,~rm F'$인 타원 ${x ^{2}} over {16} + {y ^{2}} over {7} =1$ 위의 점 $rm P$에 "
              "대하여 $overline {rm PF} =3$일 때, 삼각형 $rm PF'F$의 둘레의 길이는?"),
        ('fig', "fig_g26", 60),
        ('ch', N(8, 10, 12, 14, 16))]),
    dict(no=27, pts=3, ans=1, blocks=[
        ('t', "쌍곡선 ${x ^{2}} over {a ^{2}} - {y ^{2}} over {9} =1$의 한 점근선의 기울기가 ${3} over {2}$일 때, "
              "이 쌍곡선의 두 초점 사이의 거리는? (단, $a>0$)"),
        ('ch', ["2 sqrt {13}", "2 sqrt {14}", "2 sqrt {15}", "8", "2 sqrt {17}"])]),
    dict(no=28, pts=4, ans=3, blocks=[
        ('t', "그림과 같이 한 모서리의 길이가 $2$인 정육면체 $rm ABCD - EFGH$가 있다. 선분 $rm AG$와 "
              "평면 $rm EFGH$가 이루는 예각의 크기를 $theta$라 할 때, $cos theta$의 값은?"),
        ('fig', "fig_g28", 45),
        ('ch', ["{sqrt {3}} over {3}", "{sqrt {2}} over {2}", "{sqrt {6}} over {3}", "{sqrt {3}} over {2}",
                "{2 sqrt {2}} over {3}"])]),
    dict(no=29, pts=4, ans=16, blocks=[
        ('t', "좌표평면 위의 두 점 ${rm A} left ( 4,~0 right ),~ {rm B} left ( 0,~4 right )$에 대하여 "
              "$left | vec {rm PA} right | ^{2} + left | vec {rm PB} right | ^{2} =40$을 만족시키는 점 $rm P$가 있다. "
              "$vec {rm OP} cdot vec {rm OA}$의 최댓값이 $a+b sqrt {3}$일 때, $a+b$의 값을 구하시오. "
              "(단, $rm O$는 원점이고, $a,~b$는 자연수이다.)")]),
    dict(no=30, pts=4, ans=36, blocks=[
        ('t', "좌표공간에서 구"),
        ('eq', "S:left ( x-1 right ) ^{2} + left ( y-2 right ) ^{2} + left ( z-2 right ) ^{2} =9"),
        ('t', "가 $xy$평면과 만나서 생기는 원을 $C$라 하자. 원 $C$ 위의 점 $rm P$와 점 ${rm Q} left ( 4,~2,~4 right )$에 "
              "대하여 $overline {rm PQ} ^{2}$의 최댓값이 $a+b sqrt {5}$일 때, $a+b$의 값을 구하시오. "
              "(단, $a,~b$는 자연수이다.)")]),
]

SUBJECTS = [("확률과 통계", STATS), ("미적분", CALC), ("기하", GEOM)]

# 쪽 격자 배치: (왼쪽 단, 오른쪽 단). 한 단에 문항 1개(1칸) 또는 2개(위·아래 2칸).
# 'MC'(5지선다형 표시), 'SA'(단답형 표시)는 다음 문항 칸 맨 위에 붙는다.
COMMON_LAYOUT = [
    (['MC', 1, 2], [3, 4]),
    ([5, 6], [7, 8]),
    ([9], [10]),
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
# 2칸 단에서 두 번째 문항 번호의 위치(쪽 위에서부터 pt) — 원본 수능 실측. 없으면 단 가운데.
SECOND_TARGET = {2: 623, 4: 623, 6: 576, 8: 576, 17: 665, 19: 603}
