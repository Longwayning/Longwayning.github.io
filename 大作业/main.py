import os
import numpy as np
import librosa
import soundfile as sf
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# ===================== 路径设置 =====================
BASE_DIR = "./大作业"
MALE_DIR = os.path.join(BASE_DIR, "男声")
FEMALE_DIR = os.path.join(BASE_DIR, "女声")

os.makedirs(MALE_DIR, exist_ok=True)
os.makedirs(FEMALE_DIR, exist_ok=True)


# ===================== 性别识别模型 =====================
class GenderModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = SVC(kernel="linear")
        self.trained = False

    def extract_mfcc(self, path):
        """提取音频特征（性别识别核心）"""
        try:
            y, sr = librosa.load(path, sr=22050)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            return np.hstack([np.mean(mfcc, axis=1), np.var(mfcc, axis=1)])
        except:
            return None

    def load_all_train_data(self):
        """加载所有数据作为训练集（无测试集）"""
        X, y = [], []
        
        # 加载所有男声音频
        for f in os.listdir(MALE_DIR):
            if f.endswith(".wav"):
                feat = self.extract_mfcc(os.path.join(MALE_DIR, f))
                if feat is not None:
                    X.append(feat)
                    y.append(0)

        # 加载所有女声音频
        for f in os.listdir(FEMALE_DIR):
            if f.endswith(".wav"):
                feat = self.extract_mfcc(os.path.join(FEMALE_DIR, f))
                if feat is not None:
                    X.append(feat)
                    y.append(1)

        if len(X) == 0:
            return None, None
        return np.array(X), np.array(y)

    def train(self):
        """只用训练集训练，不划分测试集"""
        X_train, y_train = self.load_all_train_data()
        
        if X_train is None:
            return "❌ 请先添加训练音频！"
        
        # 特征标准化 + 训练
        X_train = self.scaler.fit_transform(X_train)
        self.model.fit(X_train, y_train)
        self.trained = True
        
        return f"✅ 训练完成！\n总训练样本：{len(X_train)} 个"

    def predict(self, path):
        """识别新音频性别"""
        if not self.trained:
            return "请先训练模型"
        f = self.extract_mfcc(path)
        if f is None:
            return "音频无效"
        return "男声" if self.model.predict(self.scaler.transform([f]))[0] == 0 else "女声"


# ===================== Tkinter GUI =====================
class GenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("语音性别识别系统")
        self.root.geometry("520x450")
        self.model = GenderModel()
        self.current_file = ""

        # 标题
        ttk.Label(root, text="语音性别识别", font=("微软雅黑", 18)).pack(pady=10)

        # 当前音频显示
        self.file_label = ttk.Label(root, text="未选择音频", font=("微软雅黑", 11))
        self.file_label.pack(pady=5)

        # 选择单个音频
        ttk.Button(root, text="选择单个 WAV 音频", command=self.select_file).pack(pady=3)

        # 批量导入文件夹
        ttk.Button(root, text="批量导入文件夹音频学习", command=self.batch_import).pack(pady=3)

        # 标记保存
        frame = ttk.Frame(root)
        frame.pack(pady=8)
        ttk.Button(frame, text="标记为 男声", command=lambda: self.save_audio(MALE_DIR)).grid(row=0, column=0, padx=10)
        ttk.Button(frame, text="标记为 女声", command=lambda: self.save_audio(FEMALE_DIR)).grid(row=0, column=1, padx=10)

        # 训练 & 识别
        ttk.Button(root, text="训练模型", command=self.do_train).pack(pady=5)
        ttk.Button(root, text="识别性别", command=self.do_predict).pack(pady=5)

        # 结果显示
        self.result_label = ttk.Label(root, text="", font=("微软雅黑", 12), foreground="blue")
        self.result_label.pack(pady=15)

    def select_file(self):
        f = filedialog.askopenfilename(filetypes=[("WAV音频", "*.wav")])
        if f:
            self.current_file = f
            self.file_label.config(text=f"已选：{os.path.basename(f)}")

    def save_audio(self, target):
        if not self.current_file:
            messagebox.showwarning("提示", "请先选择音频")
            return
        name = os.path.basename(self.current_file)
        out = os.path.join(target, name)
        y, sr = librosa.load(self.current_file, sr=16000)
        sf.write(out, y, sr)
        messagebox.showinfo("成功", "已保存为训练样本！")

    def batch_import(self):
        folder = filedialog.askdirectory(title="选择音频文件夹")
        if not folder:
            return
        choice = messagebox.askyesno("标记", "全部标记为 男声？\n取消 = 标记为 女声")
        target = MALE_DIR if choice else FEMALE_DIR
        count = 0
        for filename in os.listdir(folder):
            if filename.lower().endswith(".wav"):
                try:
                    src = os.path.join(folder, filename)
                    dst = os.path.join(target, filename)
                    y, sr = librosa.load(src, sr=16000)
                    sf.write(dst, y, sr)
                    count += 1
                except:
                    continue
        messagebox.showinfo("完成", f"批量导入 {count} 个音频！")

    def do_train(self):
        res = self.model.train()
        self.result_label.config(text=res)

    def do_predict(self):
        if not self.current_file:
            messagebox.showwarning("提示", "请先选音频")
            return
        res = self.model.predict(self.current_file)
        self.result_label.config(text=f"识别结果：{res}")


if __name__ == "__main__":
    window = tk.Tk()
    GenderApp(window)
    window.mainloop()