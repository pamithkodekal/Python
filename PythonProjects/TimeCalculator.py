speed = int(input("Enter your avg Speed : "))
distance = int(input("Enter your distance (Km) to be coverd : "))
time = distance/speed

hour = int(time) 
min = int((time-hour)*60)
sec = int ((((time-hour) *60)-min)*60)

print(f"You will reach your Destination in\n{hour} hrs : {min} mins : {sec} secs\nIf you keep your speeed {speed} constant\nHappyy Journey Drive Safe")