Laptop = {
    "Acer":101,
    "Lenovo":102,
    "Asus":103
}

print(Laptop)
print(Laptop.items())

print(Laptop.get("Asus"))

print(Laptop.keys())
print(Laptop.values())

Laptop.update({"Mac":104})
print(Laptop.items())

Laptop.pop("Mac")
print(Laptop.items())

Laptop.clear()
print(Laptop)