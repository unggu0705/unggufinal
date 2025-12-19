
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
from math import gcd

# -----------------------------------------------------------
# 1. 페이지 기본 설정 (제목, 설명)
# -----------------------------------------------------------
st.set_page_config(page_title="분수 곱셈 시각화", layout="wide")

st.title("🎨 겹쳐보면 답이 보이는 마법의 색종이")
st.markdown("### (진분수) $\\times$ (진분수)의 원리를 눈으로 확인해봐요!")

# -----------------------------------------------------------
# 2. 사용자 입력 받기 (사이드바 또는 상단 컬럼)
# -----------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.info("🟡 **첫 번째 분수 (가로)**")
    den1 = st.slider("가로를 몇 칸으로 나눌까요? (분모)", 2, 10, 2, key='d1')
    num1 = st.slider("그 중 몇 칸을 색칠할까요? (분자)", 1, den1, 1, key='n1')
    st.latex(f"\\frac{{{num1}}}{{{den1}}}") # 수식 표시

with col2:
    st.info("🔵 **두 번째 분수 (세로)**")
    den2 = st.slider("세로를 몇 칸으로 나눌까요? (분모)", 2, 10, 3, key='d2')
    num2 = st.slider("그 중 몇 칸을 색칠할까요? (분자)", 1, den2, 2, key='n2')
    st.latex(f"\\frac{{{num2}}}{{{den2}}}")

# -----------------------------------------------------------
# 3. 시각화 그리기 (Matplotlib)
# -----------------------------------------------------------
# 그래프 영역 생성
fig, ax = plt.subplots(figsize=(3, 3))

# (1) 배경 정사각형 (흰색)
ax.add_patch(patches.Rectangle((0, 0), 1, 1, fill=False, edgecolor='black', linewidth=2))

# (2) 첫 번째 분수 (가로 - 밝은 노란색)
# 높이(y축)를 분수만큼 채웁니다.
rect1 = patches.Rectangle((0, 0), 1, num1/den1, color='#FFE4B5', alpha=0.7, label='분수 1')
ax.add_patch(rect1)

# (3) 두 번째 분수 (세로 - 밝은 파란색)
# 너비(x축)를 분수만큼 채웁니다.
rect2 = patches.Rectangle((0, 0), num2/den2, 1, color='#ADD8E6', alpha=0.7, label='분수 2')
ax.add_patch(rect2)

# (4) 격자 그리기
# 가로 선 그리기
for i in range(1, den1):
    ax.axhline(y=i/den1, color='black', linestyle='-', linewidth=1)

# 세로 선 그리기
for i in range(1, den2):
    ax.axvline(x=i/den2, color='black', linestyle='-', linewidth=1)

# (5) 숫자 표시
# 가로 숫자 (위쪽)
for i in range(den2):
    ax.text((i + 0.5) / den2, 1.05, str(i + 1), ha='center', va='bottom', fontsize=10, fontweight='bold')

# 세로 숫자 (왼쪽)
for i in range(den1):
    ax.text(-0.05, 1 - (i + 0.5) / den1, str(i + 1), ha='right', va='center', fontsize=10, fontweight='bold')

# 그래프 꾸미기
ax.set_xlim(-0.15, 1.15)
ax.set_ylim(-0.1, 1.15)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect('equal')

# Streamlit에 그래프 출력 (고정된 크기로 표시하여 스크롤 방지)
buf = io.BytesIO()
fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
buf.seek(0)
st.image(buf, use_container_width=False, width=480)
plt.close(fig)

# -----------------------------------------------------------
# 4. 결과 및 원리 설명 (텍스트 & 수식)
# -----------------------------------------------------------
st.divider() # 구분선

# 계산 로직
result_num = num1 * num2
result_den = den1 * den2

# 결과 보여주기
st.subheader("💡 계산 결과 확인하기")

st.markdown("### 먼저 답을 맞춰보세요!")

# 분자와 분모를 입력받기
c1, c2, c3 = st.columns(3)

with c1:
    user_num = st.number_input("분자를 입력하세요", min_value=1, value=1, step=1)

with c2:
    st.markdown("### ÷")

with c3:
    user_den = st.number_input("분모를 입력하세요", min_value=2, value=2, step=1)

# 입력 값 출력
st.latex(f"\\frac{{{int(user_num)}}}{{{int(user_den)}}}")

# 정답 검사
if st.button("정답 확인"):
    # 기약분수로 변환
    reduced_result_num = result_num
    reduced_result_den = result_den
    common_divisor = gcd(result_num, result_den)
    reduced_result_num = result_num // common_divisor
    reduced_result_den = result_den // common_divisor
    
    # 사용자 입력도 기약분수로 변환
    user_gcd = gcd(int(user_num), int(user_den))
    user_reduced_num = int(user_num) // user_gcd
    user_reduced_den = int(user_den) // user_gcd
    
    # 두 가지 형태 모두 정답으로 인정 (원래 형태 또는 기약분수 형태)
    if (user_num == result_num and user_den == result_den) or (user_reduced_num == reduced_result_num and user_reduced_den == reduced_result_den):
        st.balloons()
        st.success("🎉 정답입니다! 완벽해요!")
    else:
        st.error(f"❌ 아직 아니에요. 정답은 $\\frac{{{result_num}}}{{{result_den}}}$ 또는 기약분수로 $\\frac{{{reduced_result_num}}}{{{reduced_result_den}}}$입니다.")

# 힌트 보여주기
with st.expander("💡 계산 방법 보기"):
    c1, c2, c3 = st.columns([1, 0.2, 1])
    
    with c1:
        st.markdown(f"""
        **전체 조각 수 (분모)** 가로 {den1}칸 $\\times$ 세로 {den2}칸  
        = **{result_den} 조각**
        """)
    
    with c2:
        st.markdown("### $\\rightarrow$")
    
    with c3:
        st.markdown(f"""
        **겹친 초록색 조각 수 (분자)** 가로 {num1}칸 $\\times$ 세로 {num2}칸  
        = **{result_num} 조각**
        """)
    
    # 최종 수식
    st.info("따라서 분모는 분모끼리, 분자는 분자끼리 곱합니다!")
    
    # 기약분수 계산
    common_divisor = gcd(result_num, result_den)
    reduced_num = result_num // common_divisor
    reduced_den = result_den // common_divisor
    
    # 기약분수가 필요한 경우에만 표시
    if common_divisor > 1:
        st.latex(f"\\frac{{{num1}}}{{{den1}}} \\times \\frac{{{num2}}}{{{den2}}} = \\frac{{{num1} \\times {num2}}}{{{den1} \\times {den2}}} = \\frac{{{result_num}}}{{{result_den}}} = \\frac{{{reduced_num}}}{{{reduced_den}}}")
    else:
        st.latex(f"\\frac{{{num1}}}{{{den1}}} \\times \\frac{{{num2}}}{{{den2}}} = \\frac{{{num1} \\times {num2}}}{{{den1} \\times {den2}}} = \\frac{{{result_num}}}{{{result_den}}}")
