import tkinter as tk
from tkinter import ttk, Scrollbar, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

# 스타일 설정 함수
def configure_styles(root):
    style = ttk.Style()
    style.configure("TNotebook", padding=5)
    style.configure("TNotebook.Tab", padding=[10, 5])
    style.configure("TLabel", padding=5)
    style.configure("TButton", padding=5)
    style.configure("TEntry", padding=5)

class LossGui:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x800")
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
        # 초기 산출
        self.calculate_loss()
        self.calculate_age_at_accident(datetime(1995, 2, 18), datetime(2023, 4, 21))
        self.calculate_income(161858, datetime(2023, 8, 31), datetime(2023, 9, 8), 0.54, 20, 1.0)

    def create_language_tab(self):
        tk.Label(self.language_tab, text="언어 Language:").pack(pady=10)
        tk.Radiobutton(self.language_tab, text="한국어", variable=self.language_var, value="한국어", command=self.update_language).pack(anchor=tk.W)
        tk.Radiobutton(self.language_tab, text="English", variable=self.language_var, value="English", command=self.update_language).pack(anchor=tk.W)

    def create_developer_tab(self):
        tk.Label(self.developer_tab, text="개발자: pimedi").pack(pady=10)
        tk.Label(self.developer_tab, text="이 프로그램은 개발자 본인의 피해산출에 참조하기 위해 제작되었습니다.\n 본 목적 이외의 사용에 대한 모든 책임은 개별 사용자에게 있습니다.").pack(pady=10)
        tk.Label(self.developer_tab, text="2024년 5월 기준으로 제작되었습니다.").pack(pady=10)
        
        tk.Label(self.developer_tab, text="pimedi314@gmail.com").pack(pady=10)
        tk.Label(self.developer_tab, text="https://github.com/pimedi/lossgui").pack(pady=10)
        tk.Label(self.developer_tab, text="로스구이 V1.00 (LossGui V1.00)").pack(pady=10)


    def create_calculation_tab(self):
        self.labels = {}
        self.entries = {}

        canvas = tk.Canvas(self.calculation_tab)
        scrollbar = Scrollbar(self.calculation_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 마우스 휠 이벤트 바인딩
        def _on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

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
        self.entries['birth_date'] = DateEntry(basic_info_frame, date_pattern='yyyy-mm-dd', year=1995, month=2, day=18)
        self.entries['birth_date'].grid(row=2, column=1, pady=5, padx=5)

        self.labels['accident_date'] = tk.Label(basic_info_frame, text="사고 발생일:")
        self.labels['accident_date'].grid(row=3, column=0, pady=5, padx=5)
        self.entries['accident_date'] = DateEntry(basic_info_frame, date_pattern='yyyy-mm-dd', year=2023, month=4, day=21)
        self.entries['accident_date'].grid(row=3, column=1, pady=5, padx=5)

        self.labels['retirement_age'] = tk.Label(basic_info_frame, text="가동 연한:")
        self.labels['retirement_age'].grid(row=4, column=0, pady=5, padx=5)
        self.entries['retirement_age'] = tk.Entry(basic_info_frame)
        self.entries['retirement_age'].grid(row=4, column=1, pady=5, padx=5)
        self.entries['retirement_age'].insert(0, "65")

        # Loss of Earnings Section
        loss_income_frame = tk.LabelFrame(scrollable_frame, text="일실수입")
        loss_income_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.labels['monthly_work_days'] = tk.Label(loss_income_frame, text="월평균 노동일수:")
        self.labels['monthly_work_days'].grid(row=0, column=0, pady=5, padx=5)
        self.entries['monthly_work_days'] = ttk.Combobox(loss_income_frame, values=[str(i) for i in range(32)], state='readonly')
        self.entries['monthly_work_days'].grid(row=0, column=1, pady=5, padx=5)
        self.entries['monthly_work_days'].set("20")

        # Period of Assessment Section
        self.periods_frame = tk.LabelFrame(loss_income_frame, text="산정 기간")
        self.periods_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Adding labels for period entries
        tk.Label(self.periods_frame, text="종료일").grid(row=0, column=0, pady=5, padx=5)
        tk.Label(self.periods_frame, text="일평균 노임단가").grid(row=0, column=1, pady=5, padx=5)
        tk.Label(self.periods_frame, text="노동 상실률").grid(row=0, column=2, pady=5, padx=5)
        tk.Label(self.periods_frame, text="호프만 계수").grid(row=0, column=3, pady=5, padx=5)
        tk.Label(self.periods_frame, text="호프만 계수 적용 개월수").grid(row=0, column=4, pady=5, padx=5)
        tk.Label(self.periods_frame, text="호프만 수치").grid(row=0, column=5, pady=5, padx=5)
        tk.Label(self.periods_frame, text="산정 개월수").grid(row=0, column=6, pady=5, padx=5)

        self.periods = []
        self.add_period_row('2023-08-31', '157068', '100')
        self.add_period_row('2023-09-08', '161858', '100')
        self.add_period_row('2023-12-31', '161858', '54')
        self.add_period_row('2028-04-20', '165545', '54')
        self.add_period_row('2060-02-17', '165545', '30')

        add_period_button = tk.Button(self.periods_frame, text="산정 기간 추가", command=self.add_period_row)
        add_period_button.grid(row=100, column=0, pady=5)
        remove_period_button = tk.Button(self.periods_frame, text="산정 기간 제거", command=self.remove_period_row)
        remove_period_button.grid(row=100, column=1, pady=5)

        self.result_label = tk.Label(scrollable_frame, text="피해 산출 결과: ")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.detail_label = tk.Label(scrollable_frame, text="세부 계산 사항: ")
        self.detail_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.error_label = tk.Label(scrollable_frame, text="", fg="red")
        self.error_label.grid(row=4, column=0, columnspan=2, pady=10)

        # 기본 정보가 변경될 때마다 자동 계산 실행
        self.entries['birth_date'].bind("<<DateEntrySelected>>", self.calculate_loss)
        self.entries['accident_date'].bind("<<DateEntrySelected>>", self.calculate_loss)
        self.entries['retirement_age'].bind("<KeyRelease>", self.calculate_loss)
        self.entries['monthly_work_days'].bind("<<ComboboxSelected>>", self.calculate_loss)

    def add_period_row(self, end_date=None, daily_wage=None, loss_rate=None):
        row = len(self.periods) + 1
        accident_date = self.entries['accident_date'].get()
        accident_date = datetime.strptime(accident_date, '%Y-%m-%d')
        end_date_entry = DateEntry(self.periods_frame, date_pattern='yyyy-mm-dd')
        daily_wage_entry = tk.Entry(self.periods_frame, width=12)
        loss_rate_entry = tk.Entry(self.periods_frame, width=8)
        hoffman_coeff_label = tk.Label(self.periods_frame, text="0.000000", width=12)
        hoffman_months_label = tk.Label(self.periods_frame, text="0", width=12)
        hoffman_value_label = tk.Label(self.periods_frame, text="0.000000", width=12)
        actual_months_label = tk.Label(self.periods_frame, text="0.00", width=12)

        if end_date:
            end_date_entry.set_date(end_date)
        if daily_wage:
            daily_wage_entry.insert(0, daily_wage)
        if loss_rate:
            loss_rate_entry.insert(0, loss_rate)

        end_date_entry.grid(row=row, column=0, pady=5, padx=5)
        daily_wage_entry.grid(row=row, column=1, pady=5, padx=5)
        loss_rate_entry.grid(row=row, column=2, pady=5, padx=5)
        hoffman_coeff_label.grid(row=row, column=3, pady=5, padx=5)
        hoffman_months_label.grid(row=row, column=4, pady=5, padx=5)
        hoffman_value_label.grid(row=row, column=5, pady=5, padx=5)
        actual_months_label.grid(row=row, column=6, pady=5, padx=5)

        # 호프만 계수 업데이트
        def update_hoffman_coeff(*args):
            end_date = datetime.strptime(end_date_entry.get(), '%Y-%m-%d')
            n_months = (end_date.year - accident_date.year) * 12 + (end_date.month - accident_date.month)
            hoffman_coeffs = [(1 / (1 + ((i + 1) / 12.0 * 0.05))) for i in range(n_months)]
            hoffman_value = sum(hoffman_coeffs)
            hoffman_coeff_label.config(text=f"{hoffman_coeffs[-1]:.6f}" if hoffman_coeffs else "0.000000")
            hoffman_months_label.config(text=f"{n_months}")
            hoffman_value_label.config(text=f"{hoffman_value:.6f}")
            actual_months_label.config(text=f"{n_months:.2f}")

        end_date_entry.bind("<<DateEntrySelected>>", update_hoffman_coeff)
        self.entries['accident_date'].bind("<<DateEntrySelected>>", update_hoffman_coeff)
        daily_wage_entry.bind("<KeyRelease>", self.calculate_loss)
        loss_rate_entry.bind("<KeyRelease>", self.calculate_loss)

        self.periods.append((end_date_entry, daily_wage_entry, loss_rate_entry, hoffman_coeff_label, hoffman_months_label, hoffman_value_label, actual_months_label))

    def remove_period_row(self):
        if self.periods:
            end_date_entry, daily_wage_entry, loss_rate_entry, hoffman_coeff_label, hoffman_months_label, hoffman_value_label, actual_months_label = self.periods.pop()
            end_date_entry.grid_forget()
            daily_wage_entry.grid_forget()
            loss_rate_entry.grid_forget()
            hoffman_coeff_label.grid_forget()
            hoffman_months_label.grid_forget()
            hoffman_value_label.grid_forget()
            actual_months_label.grid_forget()

    def update_language(self):
        lang = self.language_var.get()
        if lang == "한국어":
            self.labels['type'].config(text="유형:")
            self.labels['gender'].config(text="성별:")
            self.labels['birth_date'].config(text="생년월일:")
            self.labels['accident_date'].config(text="사고 발생일:")
            self.labels['retirement_age'].config(text="가동 연한:")
            self.labels['monthly_work_days'].config(text="월평균 노동일수:")
            self.result_label.config(text="피해 산출 결과: ")
            self.detail_label.config(text="세부 계산 사항: ")
        elif lang == "English":
            self.labels['type'].config(text="Type:")
            self.labels['gender'].config(text="Gender:")
            self.labels['birth_date'].config(text="Date of Birth:")
            self.labels['accident_date'].config(text="Accident Date:")
            self.labels['retirement_age'].config(text="Retirement Age:")
            self.labels['monthly_work_days'].config(text="Monthly Work Days:")
            self.result_label.config(text="Calculation Result: ")
            self.detail_label.config(text="Detailed Calculation: ")

    def calculate_loss(self, event=None):
        try:
            damage_type = self.entries['type'].get()
            gender = self.entries['gender'].get()
            birth_date = datetime.strptime(self.entries['birth_date'].get(), '%Y-%m-%d')
            accident_date = datetime.strptime(self.entries['accident_date'].get(), '%Y-%m-%d')
            retirement_age = int(self.entries['retirement_age'].get())
            monthly_work_days = int(self.entries['monthly_work_days'].get())

            age_at_accident = self.calculate_age_at_accident(birth_date, accident_date)
            days_to_retirement = (retirement_age * 365) - (age_at_accident['years'] * 365 + age_at_accident['months'] * 30 + age_at_accident['days'])
            years_to_retirement = float(days_to_retirement) / 365

            total_temp_loss_income = 0
            detailed_info = []
            previous_end_date = accident_date

            for end_date_entry, daily_wage_entry, loss_rate_entry, hoffman_coeff_label, hoffman_months_label, hoffman_value_label, actual_months_label in self.periods:
                start_date = previous_end_date + timedelta(days=1)
                end_date = datetime.strptime(end_date_entry.get(), '%Y-%m-%d')
                daily_wage = float(daily_wage_entry.get())
                loss_rate = float(loss_rate_entry.get()) / 100
                hoffman_value = float(hoffman_value_label.cget("text"))

                # 실질적인 적용 개월수 계산
                actual_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + (end_date.day - start_date.day) / 30.0
                days_in_month = (end_date - start_date).days % 30

                hoffman_coeffs = [(1 / (1 + ((i + 1) / 12.0 * 0.05))) for i in range(int(actual_months))]
                hoffman_value = sum(hoffman_coeffs)
                hoffman_value += (days_in_month / 30.0) * (1 / (1 + ((int(actual_months) + 1) / 12.0 * 0.05)))

                actual_months_label.config(text=f"{actual_months:.2f}")

                income = self.calculate_income(daily_wage, start_date, end_date, loss_rate, monthly_work_days, hoffman_value)
                total_temp_loss_income += income
                detailed_info.append(f"{start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}: {income:,.0f} 원 (호프만 계수: {hoffman_coeff_label.cget('text')}, 호프만 계수 적용 개월수: {hoffman_months_label.cget('text')}, 호프만 수치: {hoffman_value:.6f}, 산정 개월수: {actual_months_label.cget('text')})")

                previous_end_date = end_date

            total_loss = total_temp_loss_income

            self.result_label.config(text=f"피해 산출 결과: {total_loss:,.0f} 원")
            detailed_info_text = "\n".join(detailed_info)
            self.detail_label.config(text=f"""
            사고 시 연령: {age_at_accident['years']}세 {age_at_accident['months']}개월 {age_at_accident['days']}일
            가동 연한까지의 기간: {days_to_retirement}일 = ({years_to_retirement:,.4f}년)
            총 손실: {total_loss:,.0f} 원
            세부 사항:
            {detailed_info_text}
            """)
            self.error_label.config(text="")
        except ValueError as ve:
            self.error_label.config(text=f"입력 값이 잘못되었습니다: {str(ve)}")
        except Exception as e:
            self.error_label.config(text=f"오류 발생: {str(e)}")

    def calculate_age_at_accident(self, birth_date, accident_date):
        delta = relativedelta(accident_date, birth_date)
        return {"years": delta.years, "months": delta.months, "days": delta.days}

    def calculate_income(self, daily_wage, start_date, end_date, loss_rate, work_days, hoffman_value):
        total_income = 0
        current_date = start_date

        while current_date < end_date:
            next_date = current_date + relativedelta(months=1)
            if next_date > end_date:
                next_date = end_date
            income_for_period = daily_wage * work_days * loss_rate * hoffman_value
            total_income += income_for_period
            current_date = next_date

        return total_income

# 애플리케이션 실행
root = tk.Tk()
root.title("로스구이 (LossGui)")

# 스타일 설정
configure_styles(root)

app = LossGui(root)
root.mainloop()
