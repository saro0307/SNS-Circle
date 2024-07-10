import matplotlib.pyplot as plt
import numpy as np
import calendar
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# List of students
students = ['Ted', 'Barney', 'Marshall', 'Lily', 'Robin']

# Initialize attendance data for the current year
current_year = datetime.now().year
days_in_year = 366 if calendar.isleap(current_year) else 365
attendance_data = {student: np.zeros(days_in_year) for student in students}

class AttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Student Attendance Tracker")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Create tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Add Attendance Tab
        self.add_attendance_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_attendance_frame, text="Add Attendance")

        # View Attendance Tab
        self.view_attendance_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_attendance_frame, text="View Attendance")

        self.setup_add_attendance_tab()
        self.setup_view_attendance_tab()

    def setup_add_attendance_tab(self):
        # Student selection
        ttk.Label(self.add_attendance_frame, text="Select Student:").grid(row=0, column=0, padx=5, pady=5)
        self.student_var = tk.StringVar()
        self.student_dropdown = ttk.Combobox(self.add_attendance_frame, textvariable=self.student_var, values=students)
        self.student_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.student_dropdown.set(students[0])

        # Date selection
        ttk.Label(self.add_attendance_frame, text="Date:").grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.add_attendance_frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        # Attendance status
        self.status_var = tk.StringVar(value="present")
        ttk.Radiobutton(self.add_attendance_frame, text="Present", variable=self.status_var, value="present").grid(row=2, column=0, padx=5, pady=5)
        ttk.Radiobutton(self.add_attendance_frame, text="Absent", variable=self.status_var, value="absent").grid(row=2, column=1, padx=5, pady=5)

        # Submit button
        ttk.Button(self.add_attendance_frame, text="Submit", command=self.add_attendance).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def setup_view_attendance_tab(self):
        # Student selection for viewing
        ttk.Label(self.view_attendance_frame, text="Select Student:").grid(row=0, column=0, padx=5, pady=5)
        self.view_student_var = tk.StringVar()
        self.view_student_dropdown = ttk.Combobox(self.view_attendance_frame, textvariable=self.view_student_var, values=students)
        self.view_student_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.view_student_dropdown.set(students[0])

        # View button
        ttk.Button(self.view_attendance_frame, text="View Attendance", command=self.view_attendance).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Frame for matplotlib figure
        self.chart_frame = ttk.Frame(self.view_attendance_frame)
        self.chart_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def add_attendance(self):
        student = self.student_var.get()
        date_str = self.date_entry.get()
        status = self.status_var.get()

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            day_of_year = (date - datetime(current_year, 1, 1).date()).days

            if 0 <= day_of_year < days_in_year:
                attendance_data[student][day_of_year] = 1 if status == "present" else 0
                messagebox.showinfo("Success", f"Attendance for {student} on {date_str} has been recorded.")
            else:
                messagebox.showerror("Error", "Invalid date for the current year.")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")

    def view_attendance(self):
        student = self.view_student_var.get()
        self.create_attendance_bar_chart(student)

    def create_attendance_bar_chart(self, student):
        data = attendance_data[student]

        # Create monthly attendance summary
        months = range(1, 13)
        monthly_attendance = []
        for month in months:
            days_in_month = calendar.monthrange(current_year, month)[1]
            start_day = (datetime(current_year, month, 1) - datetime(current_year, 1, 1)).days
            end_day = start_day + days_in_month
            attendance_count = np.sum(data[start_day:end_day])
            monthly_attendance.append(attendance_count)

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 5))

        # Create bar chart
        bars = ax.bar(months, monthly_attendance, align='center', alpha=0.8)

        # Customize the plot
        ax.set_title(f"{student}'s Monthly Attendance for {current_year}")
        ax.set_xlabel('Month')
        ax.set_ylabel('Days Present')
        ax.set_xticks(months)
        ax.set_xticklabels(calendar.month_abbr[1:])
        ax.set_ylim(0, max(calendar.monthrange(current_year, m)[1] for m in months))

        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        # Clear previous chart if exists
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()