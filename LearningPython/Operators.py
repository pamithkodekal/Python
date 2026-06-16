# =====================================
# Arithmetic Operators
# =====================================

print("===== Arithmetic Operators =====")

sum_result = 3 + 5
subtraction = 3 - 5
multiplication = 3 * 5
division = 5 / 3
modulo = 10 % 5

print(f"Addition       : {sum_result}")
print(f"Subtraction    : {subtraction}")
print(f"Multiplication : {multiplication}")
print(f"Division       : {division}")
print(f"Modulo         : {modulo}")


# =====================================
# Relational (Comparison) Operators
# =====================================

print("\n===== Relational Operators =====")

num1 = 50
num2 = 60

if num1 == num2:
    print("Both numbers are equal")
else:
    print("Both numbers are not equal")

if num1 > num2:
    print(f"{num1} is greater than {num2}")
else:
    print(f"{num2} is greater than {num1}")

if num1 < num2:
    print(f"{num1} is smaller than {num2}")
else:
    print(f"{num2} is smaller than {num1}")


# =====================================
# Logical Operators
# =====================================

print("\n===== Logical Operators =====")

age = 18
physical_fit = True
vehicle = "Bike"

# AND Operator
print("AND Operation:")
print(age >= 18 and physical_fit and vehicle == "Bike")

# OR + NOT Operator
print("\nOR / NOT Operation:")
print(age > 18 or not physical_fit or vehicle == "Car")


# =====================================
# Assignment Operators
# =====================================

print("\n===== Assignment Operators =====")

a = 40
b = 25

print(f"Initial Value of a : {a}")
a = 40

a += b
print(f"After a += b  : {a}")
a = 40
a -= b
print(f"After a -= b  : {a}")
a = 40
a *= b
print(f"After a *= b  : {a}")
a = 40
a /= b
print(f"After a /= b  : {a}")
a = 40
a %= b
print(f"After a %= b  : {a}")

a = 40
a //= b
print(f"After a //= b : {a}")

a = 40
a **= 2
print(f"After a **= 2 : {a}")

#============================== |
#       Bitwise Operator        |
#============================== |

AND = 12 & 10
print("AND : " , AND)

OR = 12 | 10
print("OR : " , OR)

XOR = 12 ^ 10
print("XOR : " , XOR)

Complement = ~15
print("Complement : ",Complement)

RightShift = 12>>2
print("RightShift : ", RightShift)

LeftShift = 12<<3
print("LeftShift : ", LeftShift)
