import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import streamlit as st

st.title('交互组件示例')

# 文本输入
name = st.text_input('请输入你的名字：')

# 滑块
age = st.slider('选择你的年龄：', 0, 100, 25)
st.write(f'你好，{name}！你选择的年龄是 {age}。')

# # 按钮
# if st.button('提交'):
#     st.write(f'你好，{name}！你选择的年龄是 {age}。')


# st.title('数据展示示例')

# # 显示数据框
# data = pd.DataFrame({
#     '列1': [1, 2, 3, 4],
#     '列2': [10, 20, 30, 40]
# })
# st.write('数据框：', data)

# # 显示图表
# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c']
# )
# st.line_chart(chart_data)

# # 显示 matplotlib 图表
# fig, ax = plt.subplots()
# ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
# st.pyplot(fig)

