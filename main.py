# ---------------------------------------------
# User Login System (Classes + JSON Persistence)
# Purpose: Create accounts, log in users (counts logins),
# and allow admin to reset passwords or (de)activate users.
# Demonstrates: variables, conditionals, loops, functions,
# classes/inheritance, file I/O (JSON), input validation.
# ---------------------------------------------

import json
from typing import List, Dict

# ---------- Models ----------
class User:
    """Represents a basic user account."""
    def __init__(self, username: str, password: str, active: bool = True, login_count: int = 0):
        self.username = username
        self.password = password    # NOTE: plain text for demo only
        self.active = active
        self.login_count = login_count

    def check_password(self, pw: str) -> bool:
        """Return True if the given password matches this user's password."""
        return self.password == pw

    def login(self, username: str, password: str) -> bool:
        """Attempt login. Blocks if inactive; increments login_count on success."""
        if not self.active:
            print("Account disabled.")
            return False
        if self.username == username and self.check_password(password):
            self.login_count += 1
            print("Login successful.")
            return True
        print("Invalid credentials.")
        return False

    def to_dict(self) -> Dict:
        """Serialize this user to a dict for saving as JSON."""
        return {
            "type": "User",
            "username": self.username,
            "password": self.password,
            "active": self.active,
            "login_count": self.login_count
        }

    @staticmethod
    def from_dict(d: Dict) -> "User":
        """Create a User from a dict loaded from JSON."""
        return User(
            username=d["username"],
            password=d["password"],
            active=d.get("active", True),
            login_count=d.get("login_count", 0)
        )


class AdminUser(User):
    """An admin account with elevated actions."""
    def __init__(self, username: str, password: str, active: bool = True, login_count: int = 0):
        super().__init__(username, password, active, login_count)

    def reset_password(self, user: User, new_pw: str):
        """Set a new password for another user."""
        user.password = new_pw
        print(f"Password reset for '{user.username}'.")

    def deactivate(self, user: User):
        """Disable the target user."""
        user.active = False
        print(f"User '{user.username}' deactivated.")

    def reactivate(self, user: User):
        """Re-enable the target user."""
        user.active = True
        print(f"User '{user.username}' reactivated.")

    def to_dict(self) -> Dict:
        """Serialize this admin user with type marker."""
        d = super().to_dict()
        d["type"] = "AdminUser"
        return d

    @staticmethod
    def from_dict(d: Dict) -> "AdminUser":
        """Create an AdminUser from a dict loaded from JSON."""
        return AdminUser(
            username=d["username"],
            password=d["password"],
            active=d.get("active", True),
            login_count=d.get("login_count", 0)
        )

# ---------- Persistence ----------
def save_users(users: List[User], filename: str = "users.json") -> None:
    """Write the current user list to JSON so it persists across runs."""
    with open(filename, "w") as f:
        json.dump([u.to_dict() for u in users], f, indent=2)
    print(f"Saved {len(users)} users to {filename}.")

def load_users(filename: str = "users.json") -> List[User]:
    """Load users from JSON, rebuilding User/AdminUser instances."""
    try:
        with open(filename, "r") as f:
            raw = json.load(f)
    except FileNotFoundError:
        return []
    users: List[User] = []
    for d in raw:
        if d.get("type") == "AdminUser":
            users.append(AdminUser.from_dict(d))
        else:
            users.append(User.from_dict(d))
    return users

def find_user(users: List[User], username: str) -> User | None:
    """Return the user with the given username, or None if missing."""
    for u in users:
        if u.username == username:
            return u
    return None

# ---------- Helpers ----------
def prompt_nonempty(prompt: str) -> str:
    """Keep asking until the user enters a non-empty string."""
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Please enter something.")

def prompt_menu() -> str:
    """Display the main menu and return the user's choice."""
    print("\nMenu:")
    print("1) Create user")
    print("2) Login")
    print("3) List users")
    print("4) Admin actions")
    print("5) Save")
    print("6) Exit")
    return input("Choose: ").strip()

# ---------- Admin sub-menu ----------
def admin_actions(users: List[User]) -> None:
    """Authenticate as admin, then perform admin-only actions."""
    admin_name = prompt_nonempty("Admin username: ")
    admin_pw = prompt_nonempty("Admin password: ")
    admin_user = find_user(users, admin_name)

    if not isinstance(admin_user, AdminUser):
        print("That user is not an admin or does not exist.")
        return
    if not admin_user.login(admin_name, admin_pw):
        return

    print("\nAdmin Menu:")
    print("a) Reset password")
    print("b) Deactivate user")
    print("c) Reactivate user")
    print("d) Back")
    choice = input("Choose: ").strip().lower()

    if choice == "a":
        target = prompt_nonempty("Target username: ")
        u = find_user(users, target)
        if u:
            new_pw = prompt_nonempty("New password: ")
            admin_user.reset_password(u, new_pw)
        else:
            print("User not found.")
    elif choice == "b":
        target = prompt_nonempty("Target username: ")
        u = find_user(users, target)
        if u:
            admin_user.deactivate(u)
        else:
            print("User not found.")
    elif choice == "c":
        target = prompt_nonempty("Target username: ")
        u = find_user(users, target)
        if u:
            admin_user.reactivate(u)
        else:
            print("User not found.")
    else:
        print("Back to main menu.")

# ---------- Main ----------
def main():
    """Program entry: load users, ensure an admin exists, present menu loop."""
    users = load_users()

    # Guarantee at least one admin exists (so you can manage users).
    if not any(isinstance(u, AdminUser) for u in users):
        print("No admin found. Creating default admin 'admin' / 'admin123'.")
        users.append(AdminUser("admin", "admin123"))

    # Main loop
    while True:
        choice = prompt_menu()

        if choice == "1":
            username = prompt_nonempty("New username: ")
            if find_user(users, username):
                print("Username already exists.")
                continue
            password = prompt_nonempty("New password: ")
            users.append(User(username, password))
            print(f"User '{username}' created.")

        elif choice == "2":
            username = prompt_nonempty("Username: ")
            password = prompt_nonempty("Password: ")
            u = find_user(users, username)
            if not u:
                print("User not found.")
                continue
            u.login(username, password)

        elif choice == "3":
            print("\nUsers:")
            for u in users:
                role = "Admin" if isinstance(u, AdminUser) else "User"
                print(f"- {u.username} ({role}) | active={u.active} | logins={u.login_count}")

        elif choice == "4":
            admin_actions(users)

        elif choice == "5":
            save_users(users)

        elif choice == "6":
            save_users(users)   # autosave on exit
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()