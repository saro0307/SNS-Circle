import matplotlib.pyplot as plt
import numpy as np
import calendar
from datetime import datetime, timedelta

# List of students
students = ['Ted', 'Barney', 'Marshall', 'Lily', 'Robin']

# Initialize attendance data for the current year
current_year = datetime.now().year
days_in_year = 366 if calendar.isleap(current_year) else 365
attendance_data = {student: np.zeros(days_in_year) for student in students}

# Function to get user input for attendance
def add_attendance(student):
    current_date = datetime.now().date()
    day_of_year = (current_date - datetime(current_year, 1, 1).date()).days

    if attendance_data[student][day_of_year] != 0:
        update = input(f"Attendance for {student} on {current_date} already exists. Would you like to update it? (y/n): ").lower()
        if update != 'y':
            return

    print(f"Adding attendance for {student} on {current_date}")
    while True:
        status = input("Present (y/n): ").lower()
        if status in ['y', 'n']:
            attendance_data[student][day_of_year] = 1 if status == 'y' else 0
            print(f"Attendance for {student} on {current_date} has been {'updated' if attendance_data[student][day_of_year] != 0 else 'added'}.")
            break
        else:
            print("Please enter 'y' or 'n'.")

# Function to create a bar chart for attendance
def create_attendance_bar_chart(student):
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
    fig, ax = plt.subplots(figsize=(12, 6))
    
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

    plt.tight_layout()
    plt.show()

# Main loop
while True:
    print("\nOptions:")
    print("1. Add attendance")
    print("2. View attendance")
    print("3. Quit")
    choice = input("Enter your choice (1/2/3): ")
    
    if choice == '1':
        student = input("Enter student name: ")
        if student in students:
            add_attendance(student)
        else:
            print("Invalid student name.")
    elif choice == '2':
        student = input("Enter student name to view attendance: ")
        if student in students:
            create_attendance_bar_chart(student)
        else:
            print("Invalid student name.")
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please try again.")

print("Thank you for using the attendance system!")