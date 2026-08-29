#Student Attendance 75% +
#Student CGPA > 8.5
#Bonous marks if Attendance 90%+
#ELigible or not

print("===|Student Scholarship Eligibility Check |===")

name = input("Enter Student name: ")
Rollno = int(input("Enter Student ROll no : "))
Attendance = int(input("Enter Student's Attendance : "))
CGPA = float(input("Enter Student's CGPA: "))

if Attendance >= 90:
    bonous_marks= 5

if Attendance > 75 and CGPA >= 8.5 :
    Eligibility = True
else:
    Eligibility = False

print("==| Report| ==")

print(name )
print(Rollno )
print(Attendance)
print(CGPA)
print(f"{"Eligibile" if Eligibility else "Not Eligible"}")

if bonous_marks == 5:
    print("Honor Scholar")
else:
    print("Not Honor Scholar")