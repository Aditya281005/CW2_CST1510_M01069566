import bcrypt
import os

#pass hashing

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

#pass check

def special_character(c):
    return not c.isalnum()


def check_password_strength(password) -> tuple[bool, str]:
    if len(password) < 8:
        return (False, "Password must be at least 8 characters long.")

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(special_character(c) for c in password)

    if not has_upper:
        return (False, "Password must contain an uppercase letter.")
    if not has_lower:
        return (False, "Password must contain a lowercase letter.")
    if not has_digit:
        return (False, "Password must contain a digit.")
    if not has_special:
        return (False, "Password must contain a special character.")

    return (True, "Password is strong.")


def validate_password(password):
    return check_password_strength(password)



#user validation

def validate_username(username):
    if len(username) < 3:
        return (False, "Username must be at least 3 characters long.")
    if "," in username:
        return (False, "Username cannot contain commas.")
    return (True, "")


# ---------------------------------------------------
# CHECK IF USER ALREADY EXISTS
# ---------------------------------------------------
def user_exists(username):
    if not os.path.exists("users.txt"):
        return False

    with open("users.txt", "r") as f:
        for line in f:
            stored_username = line.split(",", 1)[0]
            if stored_username == username:
                return True

    return False

#register user

def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed_password = hash_password(password)

    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")

    print(f"User '{username}' registered successfully.\n")
    return True

#login user

def login_user(username, password):
    if not os.path.exists("users.txt"):
        print("Error: No registered users.")
        return False

    with open("users.txt", "r") as f:
        for line in f:
            stored_user, stored_hash = line.strip().split(",", 1)
            if stored_user == username:
                if verify_password(password, stored_hash):
                    print(f"\nSuccess: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    print("Error: Username not found.")
    return False

#menu

def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

#main loop

def main():
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
#user registration
        
        if choice == '1':
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, msg = validate_username(username)
            if not is_valid:
                print(f"Error: {msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, msg = validate_password(password)
            if not is_valid:
                print(f"Error: {msg}")
                continue

            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

      #login
        
        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            if login_user(username, password):
                input("\nPress Enter to return to main menu...")

      
        #exit
    
        elif choice == '3':
            print("\nThank you for using the authentication system.")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

#program entry

if __name__ == "__main__":
    main()
