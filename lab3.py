import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 创建主界面
root = tk.Tk()
root.title("信号显示界面")
root.geometry("900x550")

# ===================== 1. 信息显示框 =====================
text_area = scrolledtext.ScrolledText(root, width=30, height=15)
text_area.place(x=20, y=20)
text_area.insert(tk.END, "=== 信号显示系统 ===\n")
text_area.insert(tk.END, "点击按钮绘制信号\n")

# ===================== 2. 绘图函数 =====================
def draw_signal():
    # 清空图像
    for widget in frame_graph.winfo_children():
        widget.destroy()

    # 生成信号
    t = np.linspace(0, 2*np.pi, 1000)
    y1 = np.cos(t)
    n = np.arange(-5, 10, 1)
    y2 = np.where(n >= 0, 1, 0)

    # 创建图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 4))
    ax1.plot(t, y1, 'b-', linewidth=2, label="Continuous Cos")
    ax1.set_title("Continuous Signal")
    ax1.grid(True)
    ax1.legend()

    ax2.stem(n, y2, 'r-', markerfmt='ro', label="Discrete Step")
    ax2.set_title("Discrete Signal")
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()

    # 把图嵌入界面
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # 更新信息框
    text_area.insert(tk.END, "✅ 绘制成功！\n")
    text_area.insert(tk.END, "→ 连续余弦信号 + 离散阶跃信号\n\n")

# ===================== 3. 按钮 =====================
btn = ttk.Button(root, text="绘制连续/离散信号", command=draw_signal)
btn.place(x=20, y=280)

# ===================== 4. 图形显示框 =====================
frame_graph = tk.Frame(root, width=500, height=480, bg="white")
frame_graph.place(x=280, y=20)

# 启动界面
root.mainloop()