#Tuples Cannot be Updated But we can create a new Tuples

List = ["Apple","Mango","Banana"]
print(List," ", id(List))

List.append("Kiwi")
print(List," ", id(List))

Tuple = ("Apple","Mango","Banana")
print(Tuple," ",id(Tuple))

Tuple = Tuple[:1] +   ("Kiwi",)+ Tuple[1:]
print(Tuple," ",id(Tuple))