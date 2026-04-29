import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont


# 图形显示区域
class GraphicsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 250)
        self.setStyleSheet("background-color:white; border:1px solid #333;")
        self.points = []

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 画坐标轴
        pen = QPen(QColor("#555"), 2)
        painter.setPen(pen)
        painter.drawLine(50, 200, 350, 200)
        painter.drawLine(50, 50, 50, 200)

        # 画随机点
        pen = QPen(QColor("#ff4744"), 8)
        painter.setPen(pen)
        for x, y in self.points:
            painter.drawPoint(x, y)

    def draw_random(self):
        self.points = [(random.randint(60,340), random.randint(60,190)) for _ in range(15)]
        self.update()


# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 GUI 界面")
        self.setFixedSize(650, 500)

        # 主布局
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(30,30,30,30)

        # 标题
        title = QLabel("PyQt5 图形界面演示")
        title.setFont(QFont("Microsoft YaHei",14,QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 图形显示框
        self.canvas = GraphicsWidget()
        layout.addWidget(self.canvas)

        # 按钮
        btn_layout = QHBoxLayout()
        self.btn1 = QPushButton("生成随机图形")
        self.btn2 = QPushButton("输出信息")
        self.btn3 = QPushButton("清空内容")
        btn_layout.addWidget(self.btn1)
        btn_layout.addWidget(self.btn2)
        btn_layout.addWidget(self.btn3)
        layout.addLayout(btn_layout)

        # 信息显示框
        self.text = QTextEdit()
        self.text.setPlaceholderText("操作信息将显示在这里...")
        layout.addWidget(self.text)

        # 绑定事件
        self.btn1.clicked.connect(self.draw)
        self.btn2.clicked.connect(self.show_msg)
        self.btn3.clicked.connect(self.clear)

    def draw(self):
        self.canvas.draw_random()
        self.text.append("已生成随机图形")

    def show_msg(self):
        self.text.append("PyQt5 GUI 运行成功！")

    def clear(self):
        self.text.clear()
        self.text.append("已清空显示框")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())