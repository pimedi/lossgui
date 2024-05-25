import tkinter as tk
from tkinter import ttk, Scrollbar, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

from styles import configure_styles

class LossGui:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x600")  # 창의 기본 크기 설정
        self.language_var = tk.StringVar(value="한국어")
        self.tab_control = ttk.Notebook(root)

        self.calculation_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.calculation_tab, text='피해 산출')
        self.create_calculation_tab()

        self.language_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.language_tab, text='언어 설정')
        self.create_language_tab()

        self.developer_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.developer_tab, text='개발자 정보')
        self.create_developer_tab()

        self.tab_control.pack(expand=1, fill='both')

    def create_language_tab(self):
        tk.Label(self.language_tab, text="언어 Language:").pack(pady=10)
        tk.Radiobutton(self.language_tab, text="한국어", variable=self.language_var, value="한국어", command=self.update_language).pack(anchor=tk.W)
        tk.Radiobutton(self.language_tab, text="English", variable=self.language_var, value="English", command=self.update_language).pack(anchor=tk.W)

    def create_developer_tab(self):
        tk.Label(self.developer_tab, text="개발자: pimedi").pack(pady=10)
        tk.Label(self.developer_tab, text="이 프로그램은 아직 불완전하며, 개발자 본인의 피해를 산출하기 위해 개발되었습니다.").pack(pady=10)
        tk.Label(self.developer_tab, text="pimedi314@gmail.com").pack(pady=10)
        tk.Label(self.developer_tab, text="https://github.com/pimedi/lossgui").pack(pady=10)

    def create_calculation_tab(self):
        self.labels = {}
        self.entries = {}

        canvas = tk.Canvas(self.calculation_tab)
        scrollbar = Scrollbar(self.calculation_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 마우스 휠 이벤트 바인딩
        def _on_mouse_wheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        # Basic Information Section
        basic_info_frame = tk.LabelFrame(scrollable_frame, text="기초 사항")
        basic_info_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.labels['type'] = tk.Label(basic_info_frame, text="유형:")
        self.labels['type'].grid(row=0, column=0, pady=5, padx=5)
        self.entries['type'] = tk.StringVar(value="부상")
        tk.OptionMenu(basic_info_frame, self.entries['type'], "부상", "사망").grid(row=0, column=1, pady=5, padx=5)

        self.labels['gender'] = tk.Label(basic_info_frame, text="성별:")
        self.labels['gender'].grid(row=1, column=0, pady=5, padx=5)
        self.entries['gender'] = tk.StringVar(value="남성")
        tk.OptionMenu(basic_info_frame, self.entries['gender'], "남성", "여성").grid(row=1, column=1, pady=5, padx=5)

        self.labels['birth_date'] = tk.Label(basic_info_frame, text="생년월일:")
        self.labels['birth_date'].grid(row=2, column=0, pady=5, padx=5)
        self.entries['birth_date'] = DateEntry(basic_info_frame, date_pattern='yyyy-mm-dd', year=1995, month=2, day=18)  # 디폴트 날짜 설정
        self.entries['birth_date'].grid(row=2, column=1, pady=5, padx=5)

        self.labels['accident_date'] = tk.Label(basic_info_frame, text="사고 발생일:")
        self.labels['accident_date'].grid(row=3, column=0, pady=5, padx=5)
        self.entries['accident_date'] = DateEntry(basic_info_frame, date_pattern='yyyy-mm-dd', year=2023, month=4, day=21)  # 디폴트 날짜 설정
        self.entries['accident_date'].grid(row=3, column=1, pady=5, padx=5)

        self.labels['retirement_age'] = tk.Label(basic_info_frame, text="가동 연한:")
        self.labels['retirement_age'].grid(row=4, column=0, pady=5, padx=5)
        self.entries['retirement_age'] = tk.Entry(basic_info_frame)
        self.entries['retirement_age'].grid(row=4, column=1, pady=5, padx=5)
        self.entries['retirement_age'].insert(0, "65")

        # Loss of Earnings Section
        loss_income_frame = tk.LabelFrame(scrollable_frame, text="일실수입")
        loss_income_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.labels['daily_wage'] = tk.Label(loss_income_frame, text="일평균 노임단가:")
        self.labels['daily_wage'].grid(row=0, column=0, pady=5, padx=5)
        self.entries['daily_wage'] = tk.Entry(loss_income_frame, width=10)
        self.entries['daily_wage'].grid(row=0, column=1, pady=5, padx=5)
        self.entries['daily_wage'].insert(0, "150000")  # 예시 데이터

        self.labels['monthly_work_days'] = tk.Label(loss_income_frame, text="월평균 노동일수:")
        self.labels['monthly_work_days'].grid(row=1, column=0, pady=5, padx=5)
        self.entries['monthly_work_days'] = ttk.Combobox(loss_income_frame, values=[str(i) for i in range(32)], state='readonly')
        self.entries['monthly_work_days'].grid(row=1, column=1, pady=5, padx=5)
        self.entries['monthly_work_days'].set("20")  # 기본값 설정

        self.labels['temp_loss_rate'] = tk.Label(loss_income_frame, text="노동 상실률 (%):")
        self.labels['temp_loss_rate'].grid(row=2, column=0, pady=5, padx=5)
        self.entries['temp_loss_rate'] = tk.Entry(loss_income_frame)
        self.entries['temp_loss_rate'].grid(row=2, column=1, pady=5, padx=5)
        self.entries['temp_loss_rate'].insert(0, "54")  # 예시 데이터

        """
        self.labels['temp_loss_months'] = tk.Label(loss_income_frame, text="기간 (개월):")
        self.labels['temp_loss_months'].grid(row=3, column=0, pady=5, padx=5)
        self.entries['temp_loss_months'] = tk.Entry(loss_income_frame)
        self.entries['temp_loss_months'].grid(row=3, column=1, pady=5, padx=5)
        self.entries['temp_loss_months'].insert(0, "60")  # 예시 데이터
        
        """
        """
        self.labels['perm_loss_rate'] = tk.Label(loss_income_frame, text="영구적 노동 상실률 (%):")
        self.labels['perm_loss_rate'].grid(row=4, column=0, pady=5, padx=5)
        self.entries['perm_loss_rate'] = tk.Entry(loss_income_frame)
        self.entries['perm_loss_rate'].grid(row=4, column=1, pady=5, padx=5)
        self.entries['perm_loss_rate'].insert(0, "30")  # 예시 데이터
        """
        # Period of Assessment Section
        self.periods_frame = tk.LabelFrame(loss_income_frame, text="산정 기간")
        self.periods_frame.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.periods = []
        self.add_period_row()
        

        add_period_button = tk.Button(self.periods_frame, text="산정 기간 추가", command=self.add_period_row)
        add_period_button.grid(row=100, column=0, pady=5)
        remove_period_button = tk.Button(self.periods_frame, text="산정 기간 제거", command=self.remove_period_row)
        remove_period_button.grid(row=100, column=1, pady=5)

        calculate_button = tk.Button(loss_income_frame, text="산출", command=self.calculate_loss)
        calculate_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(scrollable_frame, text="피해 산출 결과: ")
        self.result_label.grid(row=2, column=0, columnspan=2)

        self.detail_label = tk.Label(scrollable_frame, text="세부 계산 사항: ")
        self.detail_label.grid(row=3, column=0, columnspan=2)

    def add_period_row(self):
        row = len(self.periods)
        start_date = DateEntry(self.periods_frame, date_pattern='yyyy-mm-dd',year=2023, month=4, day=21)
        start_date.grid(row=row, column=0, pady=5, padx=5)
       

        end_date = DateEntry(self.periods_frame, date_pattern='yyyy-mm-dd')
        end_date.grid(row=row, column=1, pady=5, padx=5)
        self.periods.append((start_date, end_date))

    def remove_period_row(self):
        if self.periods:
            start_date, end_date = self.periods.pop()
            start_date.grid_forget()
            end_date.grid_forget()

    def update_language(self):
        lang = self.language_var.get()
        if lang == "한국어":
            self.labels['type'].config(text="유형:")
            self.labels['gender'].config(text="성별:")
            self.labels['birth_date'].config(text="생년월일:")
            self.labels['accident_date'].config(text="사고 발생일:")
            self.labels['retirement_age'].config(text="가동 연한:")
            self.labels['daily_wage'].config(text="일평균 노임단가 ")
            self.labels['monthly_work_days'].config(text="월평균 노동일수:")
            self.labels['temp_loss_rate'].config(text="한시적 노동 상실률 (%):")
            self.labels['temp_loss_months'].config(text="한시적 기간 (개월):")
            self.labels['perm_loss_rate'].config(text="영구적 노동 상실률 (%):")
            self.result_label.config(text="피해 산출 결과: ")
            self.detail_label.config(text="세부 계산 사항: ")
        elif lang == "English":
            self.labels['type'].config(text="Type:")
            self.labels['gender'].config(text="Gender:")
            self.labels['birth_date'].config(text="Date of Birth:")
            self.labels['accident_date'].config(text="Accident Date:")
            self.labels['retirement_age'].config(text="Retirement Age:")
            self.labels['daily_wage'].config(text="Daily Wage:")
            self.labels['monthly_work_days'].config(text="Monthly Work Days:")
            self.labels['temp_loss_rate'].config(text="Temporary Loss Rate (%):")
            self.labels['temp_loss_months'].config(text="Temporary Period (Months):")
            self.labels['perm_loss_rate'].config(text="Permanent Loss Rate (%):")
            self.result_label.config(text="Calculation Result: ")
            self.detail_label.config(text="Detailed Calculation: ")

    def calculate_loss(self):
        try:
            damage_type = self.entries['type'].get()
            gender = self.entries['gender'].get()
            birth_date = datetime.strptime(self.entries['birth_date'].get(), '%Y-%m-%d')
            accident_date = datetime.strptime(self.entries['accident_date'].get(), '%Y-%m-%d')
            retirement_age = int(self.entries['retirement_age'].get())
            monthly_work_days = int(self.entries['monthly_work_days'].get())
            temp_loss_rate = float(self.entries['temp_loss_rate'].get()) / 100
            temp_loss_months = int(self.entries['temp_loss_months'].get())
            perm_loss_rate = float(self.entries['perm_loss_rate'].get()) / 100

            age_at_accident = self.calculate_age_at_accident(birth_date, accident_date)
            days_to_retirement = (retirement_age * 365) - (age_at_accident['years'] * 365 + age_at_accident['months'] * 30 + age_at_accident['days'])
            # to float
            years_to_retirement = float(days_to_retirement) / 365

            if temp_loss_months > (days_to_retirement // 30):
                messagebox.showerror("입력 오류", "한시적 기간은 가동 연한까지의 기간보다 길 수 없습니다.")
                return

            daily_wage_data = json.loads(self.entries['daily_wage'].get())

            total_temp_loss_income = 0
            total_perm_loss_income = 0

            for start_date_entry, end_date_entry in self.periods:
                start_date = datetime.strptime(start_date_entry.get(), '%Y-%m-%d')
                end_date = datetime.strptime(end_date_entry.get(), '%Y-%m-%d')
                months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

                temp_loss_income = self.calculate_income(daily_wage_data, start_date, temp_loss_rate, monthly_work_days)
                perm_loss_income = self.calculate_income(daily_wage_data, start_date + timedelta(days=temp_loss_months*30), months - temp_loss_months, perm_loss_rate, monthly_work_days)

                total_temp_loss_income += temp_loss_income
                total_perm_loss_income += perm_loss_income

            total_loss = total_temp_loss_income + total_perm_loss_income

            self.result_label.config(text=f"피해 산출 결과: {total_loss:,.0f} 원")
            self.detail_label.config(text=f"""
            사고시 연령: {age_at_accident['years']}세 {age_at_accident['months']}개월 {age_at_accident['days']}일
            가동 연한까지의 기간: {days_to_retirement} 일 = ({years_to_retirement:,.4f} 년)
            손실 소득: {total_temp_loss_income:,.0f} 원
            총 손실: {total_loss:,.0f} 원
            """)
            # 임시 코드// 영구적 손실 소득: {total_perm_loss_income:,.0f} 원

        except ValueError as ve:
            messagebox.showerror("입력 오류", f"입력 값이 잘못되었습니다: {str(ve)}")
        except json.JSONDecodeError:
            messagebox.showerror("입력 오류", "일평균 노임단가 입력 값이 유효한 JSON 형식이 아닙니다.")
        except Exception as e:
            messagebox.showerror("오류", f"오류 발생: {str(e)}")

    def calculate_age_at_accident(self, birth_date, accident_date):
        delta = relativedelta(accident_date, birth_date)
        return {"years": delta.years, "months": delta.months, "days": delta.days}

    def calculate_income(self, daily_wage, start_date, months, loss_rate, work_days):
        total_income = 0
        end_date = start_date + relativedelta(months=months)
        current_date = start_date

        while current_date < end_date:
            next_month = current_date + relativedelta(months=1)
            income_for_month = daily_wage * work_days * loss_rate
            total_income += income_for_month
            current_date = next_month

        return total_income

############################################
# 개발용 임시코드
############################################

root = tk.Tk()
root.title("로스구이 (LossGui)")

# 스타일 설정
configure_styles(root)

# 애플리케이션 실행
app = LossGui(root)
root.mainloop()
