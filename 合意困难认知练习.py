import streamlit as st
import random

QUESTIONS = [
    {"topic": "热学", "question": "0℃的冰和0℃的水，温度相同吗？", "answer": "相同"},
    {"topic": "能量守恒", "question": "无摩擦滑梯下滑，机械能是否守恒？", "answer": "是"},
    {"topic": "电路", "question": "两个相同电阻串联，总电阻是单个的几倍？", "answer": "2倍"},
    {"topic": "牛顿定律", "question": "用F大小的力推静止箱子未动，摩擦力大小？", "answer": "F"},
    {"topic": "能量守恒", "question": "功率表示做功的快慢还是多少？", "answer": "快慢"},
]

st.set_page_config(page_title="知识盲盒", page_icon="🎁")
st.markdown("<h1 style='text-align: center;'>🎁 知识盲盒挑战</h1>", unsafe_allow_html=True)
st.caption("每次题目来自不同主题！答完请写下你的思路～")

# 初始化状态
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

# 开盲盒按钮：清空所有状态
if st.button("📦 开盲盒"):
    st.session_state.current_question = random.choice(QUESTIONS)
    st.session_state.ans = ""      # 对应 key="ans"
    st.session_state.exp = ""      # 对应 key="exp"
    st.session_state.feedback = ""

# 显示题目和输入框
if st.session_state.current_question:
    st.markdown(f"### 题目：{st.session_state.current_question['question']}")
    
    # 输入框（Streamlit 会自动用 st.session_state.ans 作为初始值）
    user_answer = st.text_input("请输入你的答案：", key="ans")
    user_explain = st.text_input("请输入你的思路：", key="exp")
    
    # 提交按钮
    if st.button("提交答案"):
        correct_answer = st.session_state.current_question['answer']
        is_correct = user_answer.strip() == correct_answer.strip()
        
        if is_correct:
            st.session_state.feedback = f"""✅ 回答正确！你真棒！
            此知识点考察的是：{st.session_state.current_question['topic']}，
            看来你已经掌握了！"""
            st.balloons()
        else:
            st.session_state.feedback = f"""❌ 回答错误！
            正确答案是：{correct_answer}，
            此知识点考察的是：{st.session_state.current_question['topic']}，
            看来你还有待提高哦！"""

# 始终显示反馈（关键！）
if st.session_state.feedback:
    st.info(st.session_state.feedback)
