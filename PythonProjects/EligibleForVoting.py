 #Age #name
#city
#state

#eligible ki nai


Age = int(input("Enter your age : "))
#

if Age >= 18 :
    name = input("Enter your Name: ")
    Region = input("Enter your Region of Voting: ")
    city = input("Enter your City: ")
    State = input("ENter your State: ")

    print (f"===Voter Report===\nname: {name}\nRegion:{Region}\nCity:{city}\nState:{State}\nIs ready for Voting")
else:
    elgible = 18-Age
    print(f"You are not eligible for Voting. Please vist after {elgible} years . Thank you  ")

#