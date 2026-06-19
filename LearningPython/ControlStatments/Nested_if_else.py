#21+
#Employeed for 2-3 years
#CIBIL 700-750+

Age = 21
Employeed_Duration = 2
CIBIL_Score= 700

if Age >= 21:
    if Employeed_Duration >= 2:
        if CIBIL_Score > 750:
            print("You are Eligible for Loan")
        else:
            print("Your CIBIL Score is Low ")
    else :
        print("Employment Duration Should be 2 years +")
else:
    print("Age must be greater  than or should equal to" \
    " 21")