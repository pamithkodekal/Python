
name = input("Enter your name: ")
age = int(input("Enter your age: "))
RollNo = int(input("Enter your Rollno: "))
CGPA = float(input("Enter your CGPA: "))
print("=====================")
print(f"Name : {name} Age:{age}\nRollNo:{RollNo}\nCGPA: {CGPA}\nResult : {"Pass" if CGPA > 5 else "Fail"}")
