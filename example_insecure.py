API_KEY = "sk-ABC1234567890XYZ0987654321"

def process(data):
    eval("result = " + data)
    return result

def login(user, password):
    print("Logging in", user)
    if password == "admin123":
        print("Access granted")
