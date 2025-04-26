import mysql.connector
from mysql.connector import Error

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="<your_password>",
        database="project"
    )

def create_table():
    try:
        with get_connection() as con:
            with con.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS teacher(
                        t_id INT PRIMARY KEY,
                        tname VARCHAR(50),
                        gender CHAR(1),
                        joining_date DATE,
                        subject VARCHAR(15),
                        salary DECIMAL(10,2),
                        phone BIGINT,
                        email VARCHAR(40),
                        address VARCHAR(100)
                    )
                """)
    except Error as e:
        print("Error while creating table:", e)

def add_teacher():
    try:
        with get_connection() as con:
            with con.cursor() as cur:
                data = (
                    int(input("Enter Teacher ID: ")),
                    input("Enter Name: "),
                    input("Enter Gender (M/F): "),
                    input("Enter Joining Date (YYYY-MM-DD): "),
                    input("Enter Subject: "),
                    float(input("Enter Monthly Salary: ")),
                    int(input("Enter Phone: ")),
                    input("Enter Email: "),
                    input("Enter Address: ")
                )
                query = """
                    INSERT INTO teacher 
                    (t_id, tname, gender, joining_date, subject, salary, phone, email, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(query, data)
                con.commit()
                print("Teacher record added successfully!")
    except Error as e:
        print("Error while adding teacher:", e)

def search_teacher():
    try:
        with get_connection() as con:
            with con.cursor() as cur:
                teacher_id = int(input("Enter Teacher ID to search: "))
                cur.execute("SELECT * FROM teacher WHERE t_id = %s", (teacher_id,))
                row = cur.fetchone()
                if row:
                    display_teacher(row)
                else:
                    print("No teacher found with this ID.")
    except Error as e:
        print("Error while searching teacher:", e)

def display_all_teachers():
    try:
        with get_connection() as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM teacher")
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        display_teacher(row)
                    print(f"Total Records: {len(rows)}")
                else:
                    print("No records found.")
    except Error as e:
        print("Error while displaying teachers:", e)

def delete_teacher():
    try:
        with get_connection() as con:
            with con.cursor() as cur:
                teacher_id = int(input("Enter Teacher ID to delete: "))
                cur.execute("DELETE FROM teacher WHERE t_id = %s", (teacher_id,))
                con.commit()
                if cur.rowcount:
                    print("Teacher deleted successfully.")
                else:
                    print("No teacher found with this ID.")
    except Error as e:
        print("Error while deleting teacher:", e)

def update_teacher():
    try:
        with get_connection() as con:
            with con.cursor() as cur:
                teacher_id = int(input("Enter Teacher ID to update: "))
                print("""
                1. Update Name
                2. Update Gender
                3. Update Joining Date
                4. Update Subject
                5. Update Salary
                6. Update Phone
                7. Update Email
                8. Update Address
                """)
                choice = int(input("Enter your choice (1-8): "))
                fields = ["tname", "gender", "joining_date", "subject", "salary", "phone", "email", "address"]
                if 1 <= choice <= 8:
                    new_value = input(f"Enter new {fields[choice-1]}: ")
                    query = f"UPDATE teacher SET {fields[choice-1]} = %s WHERE t_id = %s"
                    cur.execute(query, (new_value, teacher_id))
                    con.commit()
                    if cur.rowcount:
                        print(f"{fields[choice-1].capitalize()} updated successfully.")
                    else:
                        print("No teacher found with this ID.")
                else:
                    print("Invalid choice.")
    except Error as e:
        print("Error while updating teacher:", e)

def display_teacher(row):
    print("\n--- Teacher Details ---")
    print(f"ID: {row[0]}")
    print(f"Name: {row[1]}")
    print(f"Gender: {row[2]}")
    print(f"Joining Date: {row[3]}")
    print(f"Subject: {row[4]}")
    print(f"Salary: {row[5]}")
    print(f"Phone: {row[6]}")
    print(f"Email: {row[7]}")
    print(f"Address: {row[8]}")
    print("-" * 30)

# Main Program
def main():
    create_table()  # Create table once
    while True:
        print("\n" + "#" * 30)
        print("\tDAV Public School")
        print("1. Add Teacher")
        print("2. Search Teacher")
        print("3. Display All Teachers")
        print("4. Delete Teacher")
        print("5. Update Teacher")
        print("6. Exit")
        print("#" * 30)

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                add_teacher()
            elif choice == 2:
                search_teacher()
            elif choice == 3:
                display_all_teachers()
            elif choice == 4:
                delete_teacher()
            elif choice == 5:
                update_teacher()
            elif choice == 6:
                print("Exiting the program...")
                break
            else:
                print("Invalid choice! Please try again.")
        except ValueError:
            print("Please enter a valid number.")

        cont = input("Do you want to continue? (y/n): ").lower()
        if cont != 'y':
            break

if __name__ == "__main__":
    main()
