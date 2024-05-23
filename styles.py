from tkinter import ttk

def configure_styles(root):
    # 기본 폰트 및 색상 설정
    root.option_add("*Font", "Helvetica 12")
    root.option_add("*Background", "#f2f2f2")
    root.option_add("*Foreground", "#333333")
    
    # 버튼 스타일 설정
    root.option_add("*Button.Background", "#4CAF50")
    root.option_add("*Button.Foreground", "white")
    root.option_add("*Button.Font", "Helvetica 12")
    root.option_add("*Button.Padding", 10)
    root.option_add("*Button.relief", "flat")
    root.option_add("*Button.overrelief", "raised")
    root.option_add("*Button.activebackground", "#45a049")
    root.option_add("*Button.activeforeground", "white")
    
    # 엔트리 스타일 설정
    root.option_add("*Entry.Font", "Helvetica 12")
    
    # 라벨 스타일 설정
    root.option_add("*Label.Font", "Helvetica 12")
    root.option_add("*Label.Background", "#f2f2f2")
    
    # 프레임 스타일 설정
    root.option_add("*Frame.Background", "#f2f2f2")
    
    # 스크롤바 스타일 설정
    root.option_add("*Scrollbar.Background", "#f2f2f2")
    root.option_add("*Scrollbar.Foreground", "#333333")
    root.option_add("*Scrollbar.Width", 12)
    
    # 콤보박스 스타일 설정
    root.option_add("*TCombobox.Font", "Helvetica 12")
    root.option_add("*TCombobox.Background", "white")
    root.option_add("*TCombobox.Foreground", "#333333")
    root.option_add("*TCombobox.Padding", 10)
    root.option_add("*TCombobox.relief", "flat")
    root.option_add("*TCombobox.overrelief", "raised")
    root.option_add("*TCombobox.activebackground", "#f2f2f2")
    root.option_add("*TCombobox.activeforeground", "#333333")
    root.option_add("*TCombobox.Listbox.Font", "Helvetica 12")
    root.option_add("*TCombobox.Listbox.Background", "white")
    root.option_add("*TCombobox.Listbox.Foreground", "#333333")
    root.option_add("*TCombobox.Listbox.selectBackground", "#4CAF50")
    root.option_add("*TCombobox.Listbox.selectForeground", "white")
    root.option_add("*TCombobox.Listbox.selectBorderWidth", 0)
    root.option_add("*TCombobox.Listbox.selectRelief", "flat")

    # ttk 스타일 설정
    style = ttk.Style()
    style.configure("TFrame", background="#f2f2f2")
    style.configure("TLabel", background="#f2f2f2", font=("Helvetica", 12))
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("TButton", background="#4CAF50", foreground="white", font=("Helvetica", 12), padding=10)
    style.map("TButton", background=[("active", "#45a049")])
