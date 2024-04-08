import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import time

# 创建一个空的 DataFrame 用于存储数据
df = pd.DataFrame(columns=['timestamp', 'nodeno', 'temperature'])

# 创建一个 Plotly Figure 对象
fig = make_subplots(rows=1, cols=1, subplot_titles=("Temperature Heatmap"))

# 初始化热力图
heatmap_trace = go.Heatmap(z=[[0]], colorscale='Viridis')
fig.add_trace(heatmap_trace, row=1, col=1)

# 更新热力图函数
def update_heatmap(timestamp, nodeno, temperature):
    df.loc[len(df)] = [timestamp, nodeno, temperature]
    heatmap_data = df.pivot_table(index='timestamp', columns='nodeno', values='temperature')
    fig.data[0].z = heatmap_data.values.tolist()

# 模拟实时更新数据
for i in range(10):
    timestamp = pd.Timestamp.now()
    nodeno = np.random.randint(1, 5)
    temperature = np.random.uniform(20, 30)
    update_heatmap(timestamp, nodeno, temperature)
    time.sleep(1)  # 模拟每秒更新一次数据

# 显示图表
fig.update_layout(title='Real-time Temperature Heatmap')
fig.show()
