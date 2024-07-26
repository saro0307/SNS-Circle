import sqlite3

class FeePaymentSystem:
    def __init__(self, db_name='fee_payment.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                fee REAL NOT NULL,
                paid REAL DEFAULT 0,
                status TEXT DEFAULT 'Unpaid'
            )
        ''')
        self.conn.commit()

    def clear_table(self):
        self.cursor.execute('DELETE FROM students')
        self.conn.commit()

    def add_student(self, name, fee):
        self.cursor.execute('INSERT INTO students (name, fee) VALUES (?, ?)', (name, fee))
        self.conn.commit()

    def get_all_students(self):
        self.cursor.execute('SELECT * FROM students')
        return self.cursor.fetchall()

    def update_payment(self, student_id, amount):
        self.cursor.execute('SELECT fee, paid FROM students WHERE id = ?', (student_id,))
        result = self.cursor.fetchone()
        if result is None:
            return False
        fee, paid = result
        new_paid = paid + amount
        status = 'Paid' if new_paid >= fee else 'Partially Paid'
        
        self.cursor.execute('''
            UPDATE students 
            SET paid = ?, status = ? 
            WHERE id = ?
        ''', (new_paid, status, student_id))
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()

def initialize_database(system):
    system.clear_table()  # Clear existing data
    students = [
        ('Ted', 1000),
        ('Marshal', 1200),
        ('Barney', 800),
        ('Lily', 1500),
        ('Robin', 950)
    ]
    for name, fee in students:
        system.add_student(name, fee)
    print("Database initialized with 5 students.")

def main():
    system = FeePaymentSystem()
    
    initialize_database(system)

    while True:
        print("\n1. View all students")
        print("2. Update payment")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            students = system.get_all_students()
            print("\nStudent Information:")
            print("ID | Name    | Fee    | Paid   | Status")
            print("-" * 45)
            for student in students:
                print(f"{student[0]:2d} | {student[1]:7s} | ${student[2]:6.2f} | ${student[3]:6.2f} | {student[4]}")

        elif choice == '2':
            try:
                student_id = int(input("Enter student ID: "))
                amount = float(input("Enter payment amount: "))
                if amount < 0:
                    raise ValueError("Payment amount cannot be negative")
                if system.update_payment(student_id, amount):
                    print("Payment updated successfully.")
                else:
                    print("Student not found.")
            except ValueError as e:
                print(f"Invalid input: {e}")

        elif choice == '3':
            system.close()
            print("Thank you for using the Fee Payment System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
