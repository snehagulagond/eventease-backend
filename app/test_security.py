from app.security import hash_password,verify_password


password="123@12"
hashed_password=hash_password(password)
print("Hashed Password:",hashed_password)

print("Correct Password:",verify_password(password,hashed_password))
print("Incorrect Password:",verify_password("wrongpassword",hashed_password))