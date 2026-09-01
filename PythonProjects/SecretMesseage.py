Message = input("Enter your password : ")
key = 7
Encryp = ""

for ch in Message:
    Encryp += chr(ord(ch) ^ key)
print("Message : ", Encryp)

Decryp = ""

for ch in Encryp:
    Decryp += chr(ord(ch) ^ key)
print("Secret message is : ", Decryp)