import streamlit as st
import pandas as pd


# ==============================
# 猪牛小窝
# ==============================
question = {
    "stem": "小香猪最喜欢小肥牛哪一点呢？：",
    "options": [
        "A. 如刀刻般英俊帅气的脸庞，三分讥笑三分凉薄三分宠溺，还剩下一分让全世界少女尖叫。",
        "B. 充满智慧的大脑，每天站在高高的山坡上威风凛凛的思考着一些很伟大的问题",
        "C. 幽默的语言风格，他一张嘴空气里自动飘出于谦郭德纲屎尿屁，老白师兄大猪蹄",
        "D. 善良笃定智慧高，聪明伶俐模样俏"
    ],
    "correct": "D",
    "diagnosis": "考查答题者对小香猪子眼中的小肥牛形象的了解程度，以及小香猪的恋爱脑程度化",
    "misconception": [
        "❌ 回答有误,混淆网文霸总人设与小肥牛的真实形象",
        "❌ 回答有误,认为小肥牛只有智慧可言，忽略了小肥牛这个品种的多样性和复杂性",
        "❌ 回答有误,此选项为概念性理解错误，题目为喜欢小肥牛哪一点，应该是优点，但该选项后半截明显偏贬义"
    ]
}

st.markdown("<h1 style='text-align: center;'>欢迎来到香猪肥牛俱乐部</h1>", 
            unsafe_allow_html=True)# 设置标题，并且标题加粗居中
st.text("此小本营是香猪肥牛的秘密小基地，在这里你可以体验到小香猪和小肥牛每天的幸福生活")
# 显示题目
st.subheader("请作答：")
st.write(question["stem"])
user_answer = st.radio(
    "请选择最合适的答案：",
    question["options"],
    index=None,  # 默认不选中
    key="q1"
)
if user_answer:
    if user_answer == question["options"][0]:
        st.write(question["misconception"][0])
    elif user_answer == question["options"][1]:
        st.write(question["misconception"][1])
    elif user_answer == question["options"][2]:
        st.write(question["misconception"][2])
    else:
        st.success("✅ 回答正确!你真棒，你是小香猪子和小肥牛幸福生活的见证者！")
        st.balloons()

