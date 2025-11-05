import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="平面简谐波函数演示", layout="wide")
st.title("平面简谐波函数演示")

#st.markdown("""
#本演示展示一维平面简谐波从 x=0 开始传播的过程：
#- **t = 0 时，所有质点均位于 y = 0（平衡位置）**
#- **随时间推移，波以速度 v = ω/k 向右传播**
#- **每个质点在其“被波到达”后，从平衡位置开始做简谐振动**
#""")

# ========== 初始化状态 ==========
if 'animating' not in st.session_state:
    st.session_state.animating = False
if 't_current' not in st.session_state:
    st.session_state.t_current = 0.0

# ========== 侧边栏参数 ==========
with st.sidebar:
    st.header("📊 参数设置")
    
    A = st.slider("振幅 A", 0.5, 5.0, 2.0, 0.1)
    k = st.slider("波数 k", 0.1, 5.0, 1.5, 0.1)
    omega = st.slider("角频率 ω", 0.1, 5.0, 1.5, 0.1)

    # ✅ 固定 x_min = 0
    x_min = 0.0
    x_max = st.number_input("x 最大值", 0.0, 20.0, 10.0, 0.5)
    num_points = st.slider("质点数量", 30, 200, 100, 10)

    st.divider()
    if st.button("🔄 重置时间"):
        st.session_state.animating = False
        st.session_state.t_current = 0.0
        st.rerun()

# ========== 计算波速 ==========
v = omega / k if k > 0 else 0.01

# ========== 时间控制 ==========
T_total = 4 * 2 * np.pi / omega if omega > 0 else 10
t = st.slider("时间 t (s)", 0.0, float(T_total), st.session_state.t_current, 0.01)
st.session_state.t_current = t

# ========== 播放按钮 ==========
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("▶️ 播放动画"):
        st.session_state.animating = True

with col2:
    if st.session_state.animating:
        st.warning("动画播放中... 拖动滑块或点击重置可暂停")
    else:
        st.success("就绪：可拖动时间滑块或点击播放")

# ========== 数据准备 ==========
x = np.linspace(x_min, x_max, num_points)

# ========== 波函数：只有当波到达后才开始振动 ==========
def wave_displacement(xi, t):
    delay = xi / v  # 波传到 xi 所需时间
    if t < delay:
        return 0.0  # 尚未被波到达，保持平衡位置
    else:
        # 从平衡位置开始振动：使用 sin 函数
        return A * np.sin(omega * (t - delay))
        # 等价于：A * np.sin(omega * t - k * xi) （因为 k = omega / v）

y = [wave_displacement(xi, t) for xi in x]

# ========== 双图显示 ==========
col_plot1, col_plot2 = st.columns(2)

# 左图：空间波形（x-y）
with col_plot1:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(x, y, '-', color='blue', lw=1.5, alpha=0.8, label='波形')
    ax1.plot(x, y, 'o', color='red', markersize=5, label='质点')
    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(-A - 0.3, A + 0.3)
    ax1.set_xlabel("位置 x")
    ax1.set_ylabel("位移 y")
    ax1.set_title(f"空间波形：t = {t:.2f} s")
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend()
    st.pyplot(fig1)
    plt.close(fig1)

# 右图：单个质点振动（如 x=0）
with col_plot2:
    x_probe = 0.0
    t_vals = np.linspace(0, T_total, 300)
    y_probe = [wave_displacement(x_probe, tt) for tt in t_vals]

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(t_vals, y_probe, 'b-', lw=1.5, alpha=0.7)
    ax2.plot(t, wave_displacement(x_probe, t), 'ro', markersize=8)
    ax2.set_xlim(0, T_total)
    ax2.set_ylim(-A - 0.3, A + 0.3)
    ax2.set_xlabel("时间 t (s)")
    ax2.set_ylabel(f"位移 y (x={x_probe:.1f})")
    ax2.set_title(f"质点振动：x = {x_probe:.1f}")
    ax2.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig2)
    plt.close(fig2)

# ========== 公式与物理量 ==========
st.divider()
col_eq, col_phys = st.columns(2)

# 左：波函数公式
#with col_eq:
    #eq = r"$y(x,t) = \begin{cases} 0 & t < \frac{x}{v} \\ A \sin(\omega (t - \frac{x}{v})) & t \ge \frac{x}{v} \end{cases}$"
    #st.markdown(f"### 📐 当前波函数\n{eq}")

# 右：物理量
#with col_phys:
    #wavelength = 2 * np.pi / k if k > 0 else float('inf')
    #period = 2 * np.pi / omega if omega > 0 else float('inf')
    #wave_speed = v
    #frequency = 1 / period if period != float('inf') else 0

    #st.markdown("### 📏 物理参数")
    #st.markdown(f"""
    #- 波长 $\\lambda = {wavelength:.2f}$
    #- 周期 $T = {period:.2f}$ s
    #- 频率 $f = {frequency:.2f}$ Hz
    #- 波速 $v = {wave_speed:.2f}$ 单位/秒
    #""")

# ========== 动画循环 ==========
if st.session_state.animating:
    dt = 0.05
    placeholder = st.empty()
    try:
        while st.session_state.animating and st.session_state.t_current < T_total:
            current_t = st.session_state.t_current
            y_anim = [wave_displacement(xi, current_t) for xi in x]

            # 绘制空间波形
            fig, ax = plt.subplots(figsize=(10, 3.5))
            ax.plot(x, y_anim, '-', color='blue', lw=1.5, alpha=0.8)
            ax.plot(x, y_anim, 'o', color='red', markersize=5)
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(-A - 0.3, A + 0.3)
            ax.set_title(f"波传播演示：t = {current_t:.2f} s")
            ax.grid(True, linestyle='--', alpha=0.5)
            
            placeholder.pyplot(fig)
            plt.close(fig)
            
            st.session_state.t_current += dt
            time.sleep(0.04)
    except Exception as e:
        st.error(f"动画出错: {e}")
    finally:
        st.session_state.animating = False
        st.rerun()