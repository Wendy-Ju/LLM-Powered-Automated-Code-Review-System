def admin_panel(user):
    if user == "admin":
        if check_status():
            if access_level(user) > 2:
                if not is_banned(user):
                    print("Welcome admin.")
                else:
                    print("Banned user.")
        else:
            print("Inactive.")
    else:
        print("Access denied.")

def access_level(u):
    return 3
