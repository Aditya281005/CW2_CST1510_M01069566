import bcrypt
import os
import bcrypt

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode('utf-8')

def register_user(username, password):
 
    hashed_password = hash_password(password)

    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")
    
    print(f"User {username} registered successfully.")

def login_user(username, password):

    with open("user.txt", "r") as f:
        for line in f.readlines():
            user,hash = line.strip().split(',', 1)
            if user == username:
                return verify_password(password, hash)
    return False

def verify_password(plain_text_password, hashed_password):
     password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
def check_password_strength(password) -> tuple[bool,str] :
    
    if len(password) < 8:
        return (False, False, False, False, False)
    else:
       
        has_lower = False
        has_digit = False
        has_special_character = False

        for char in password:
            if char.isupper():               
                has_upper = True
            elif char.islower():            
                has_lower = True
            elif char.isdigit():             
                has_digit = True
            elif special_character(char):   
                has_special_character = True

    return (len(password) >= 8, has_upper, has_lower, has_digit, has_special_character)

test_password = "SecurePassword123"

hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")

is_valid = verify_password(test_password, hashed)
print(f"\nVerification with correct password: {is_valid}")

is_invalid = verify_password("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")

def validate_password(password):
    pass

def display_menu():
 """Displays the main menu options."""
 print("\n" + "="*50)
 print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
 print(" Secure Authentication System")
 print("="*50)
 print("\n[1] Register a new user")
 print("[2] Login")
 print("[3] Exit")
 print("-"*50)

def main():
 """Main program loop."""
 print("\nWelcome to the Week 7 Authentication System!")

 while True:
 display_menu()
 choice = input("\nPlease select an option (1-3): ").strip()

 if choice == '1':
 # Registration flow
 print("\n--- USER REGISTRATION ---")
 username = input("Enter a username: ").strip()

 # Validate username
 is_valid, error_msg = validate_username(username)
 if not is_valid:
 print(f"Error: {error_msg}")
 continue

 password = input("Enter a password: ").strip() 

_valid, error_msg = validate_password(password)
 if not is_valid:
 print(f"Error: {error_msg}")
 continue

password_confirm = input("Confirm password: ").strip()
 if password != password_confirm:
 print("Error: Passwords do not match.")
 continue

ster_user(username, password)

 elif choice == '2':
 # Login flow
 print("\n--- USER LOGIN ---")
 username = input("Enter your username: ").strip()
 password = input("Enter your password: ").strip()

if login_user(username, password):
 print("\nYou are now logged in.")
 print("(In a real application, you would now access the d

 input("\nPress Enter to return to main menu...")

 elif choice == '3':
 
 print("\nThank you for using the authentication system.")
 print("Exiting...")
 break

 else:
 print("\nError: Invalid option. Please select 1, 2, or 3.")

 if __name__ == "__main__":
    main()