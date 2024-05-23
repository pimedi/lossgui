import tkinter as tk
from tkinter import ttk
from styles import configure_styles
from loss_gui import LossGui

# GUI 설정
root = tk.Tk()
root.title("로스구이 (LossGui)")

# 스타일 설정
configure_styles(root)

# 애플리케이션 실행
app = LossGui(root)
root.mainloop()
