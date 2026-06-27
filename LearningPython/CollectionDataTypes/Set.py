fruits = {"Apple","Banana","Mango"}
print(fruits)

fruits.add("Orange")
print(fruits)

fruits.update(["Kiwi","Pineapple"])
print(fruits)

fruits.pop()
print(fruits)

Vegitables = {"Tomato","Avacado","LadyFinger","Onion" }
fruits.update(["Tomato","Avacado"])

result = fruits.union(Vegitables)
print(result)

result_2 = fruits.intersection(Vegitables)
print(result_2)

result_3 = fruits.difference(Vegitables)
print(result_3)

result_4 = Vegitables.difference(fruits)
print(result_4)

result_5 = Vegitables.symmetric_difference(fruits)
print(result_5)