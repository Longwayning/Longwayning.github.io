# 导入需要的库
import numpy as np
import matplotlib.pyplot as plt

# ===================== 1. 生成 连续余弦信号 =====================
# 定义时间范围：0~2π，取1000个点（保证平滑）
t_continuous = np.linspace(0, 2 * np.pi, 1000)
# 生成连续余弦信号
y_continuous = np.cos(t_continuous)

# ===================== 2. 生成 离散阶跃信号 =====================
# 定义离散时间点：-5 ~ 10 的整数点
n_discrete = np.arange(-5, 10, 1)
# 生成离散阶跃信号（n>=0时为1，否则为0）
y_discrete = np.where(n_discrete >= 0, 1, 0)

# ===================== 绘图：分两个子图展示 =====================
plt.figure(figsize=(12, 5))  # 设置画布大小

# 子图1：连续信号
plt.subplot(1, 2, 1)
plt.plot(t_continuous, y_continuous, 'b-', linewidth=2, label='连续余弦信号')
plt.title('连续信号')
plt.xlabel('时间 t')
plt.ylabel('幅值')
plt.grid(True)
plt.legend()

# 子图2：离散信号
plt.subplot(1, 2, 2)
plt.stem(n_discrete, y_discrete, 'r-', markerfmt='ro', label='离散阶跃信号')
plt.title('离散信号')
plt.xlabel('时间 n')
plt.ylabel('幅值')
plt.grid(True)
plt.legend()

# 整体布局调整 + 显示图像
plt.tight_layout()
plt.show()