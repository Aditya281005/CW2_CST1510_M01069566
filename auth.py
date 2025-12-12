import bcrypt
import os
<<<<<<< HEAD
import sqlite3
import pathlib as Path
=======

#pass hashing
>>>>>>> 10fce835a4f4bf058648b3c709043a20e4ba509b

# ---------------------------------------------------
# PASSWORD HASHING
# ---------------------------------------------------
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

<<<<<<< HEAD

# ---------------------------------------------------
# PASSWORD STRENGTH CHECK
# ---------------------------------------------------
=======
#pass check

>>>>>>> 10fce835a4f4bf058648b3c709043a20e4ba509b
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


<<<<<<< HEAD
# ---------------------------------------------------
# USERNAME VALIDATION
# ---------------------------------------------------
=======

#user validation

>>>>>>> 10fce835a4f4bf058648b3c709043a20e4ba509b
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

<<<<<<< HEAD

# ---------------------------------------------------
# REGISTER USER
# ---------------------------------------------------
=======
#register user

>>>>>>> 10fce835a4f4bf058648b3c709043a20e4ba509b
def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed_password = hash_password(password)

    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")
<<<<<<< HEAD
=======

    print(f"User '{username}' registered successfully.\n")
    return True

#login user
>>>>>>> 10fce835a4f4bf058648b3c709043a20e4ba509b

    print(f"User '{username}' registered successfully.\n")
    return True


# ---------------------------------------------------
# LOGIN USER
# ---------------------------------------------------
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

<<<<<<< HEAD
=======
#menu
>>>>>>> 10fce835a4f4bf058648b3c709043a20e4ba509b

# ---------------------------------------------------
# MENU DISPLAY
# ---------------------------------------------------
def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)
<<<<<<< HEAD
=======

#main loop
>>>>>>> 10fce835a4f4bf058648b3c709043a20e4ba509b


# ---------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------
def main():
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
<<<<<<< HEAD

        # -------------------------------
        # REGISTRATION
        # -------------------------------
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

        # -------------------------------
        # LOGIN
        # -------------------------------
        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            if login_user(username, password):
                input("\nPress Enter to return to main menu...")

        # -------------------------------
        # EXIT
        # -------------------------------
        elif choice == '3':
            print("\nThank you for using the authentication system.")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


# ---------------------------------------------------
# PROGRAM ENTRY
# ---------------------------------------------------
if __name__ == "__main__":
    main()

def migrate_users_from_file(conn, filepath=Path("DATA") / "users.txt"):
    
    if not filepath.exists():
        print(f" File not found: {filepath}")
        print("   No users to migrate.")
        return
    
    cursor = conn.cursor()
    migrated_count = 0
    valid_roles = ['user', 'admin', 'analyst']
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse line: username,hashed_password,role
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                role = parts[2] if len(parts) >= 3 and parts[2] in valid_roles else 'user'  # Default to 'user' if invalid/missing
                
                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, role)
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")
    
    conn.commit()
    print(f"Migrated {migrated_count} users from {filepath.name}")
=======
        
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
>>>>>>> 10fce835a4f4bf058648b3c709043a20e4ba509b
