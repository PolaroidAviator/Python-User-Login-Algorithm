# 🧾 **Python User Login Algorithm**

A simple Python program that allows users to **create accounts, log in, and track login activity** — with an **Admin account** that can reset passwords, deactivate, or reactivate users.  
This project demonstrates Python fundamentals including **classes, loops, conditionals, functions, file I/O, and JSON serialization**.

---

## 🚀 **Features**
- Create new user accounts  
- Log in and increment login count  
- Admin-only controls:
  - Reset any user’s password  
  - Deactivate or reactivate users  
- Automatically saves all users to a JSON file (`users.json`)  
- Automatically loads users on startup  
- Creates a default admin (`admin / admin123`) if none exists  

---

## 🧩 **Concepts Demonstrated**
- **Classes & Inheritance:**  
  `User` (base class) and `AdminUser` (child class)  
- **File I/O:**  
  Save and load users using JSON  
- **Conditionals & Loops:**  
  Used in login logic, menus, and validation  
- **Functions:**  
  Organized reusable code for menu prompts and validation  
- **Error Handling:**  
  Gracefully handles missing files and bad input  

---

## 🗂️ **File Overview**
| File | Description |
|------|--------------|
| `main.py` | Main program logic and menu system |
| `users.json` | Data file created automatically when you save |
| `README.md` | Documentation file (this one) |
| `Python Journal.docx` | Written reflection for Sophia submission |

---

## ⚙️ **How It Works**

### 1. Startup
When you start the program, it looks for a file named `users.json`.  
If it doesn’t exist, it starts fresh and automatically creates an admin user:  
```
username: admin
password: admin123
```

### 2. Menu Options
You’ll see this menu:
```
1) Create user
2) Login
3) List users
4) Admin actions
5) Save
6) Exit
```

### 3. Creating a User
- Enter a new username and password.  
- The program checks if the name is already taken.  
- New users start as **active** with `login_count = 0`.  

### 4. Logging In
- Enter your username and password.  
- If correct, you’ll see “Login successful.”  
- Your `login_count` increases by 1.  
- Disabled accounts print “Account disabled.”  

### 5. Admin Actions
Admins can log in to manage users:
```
a) Reset password
b) Deactivate user
c) Reactivate user
d) Back
```

### 6. Saving Data
When you choose **Save** or **Exit**, all users are written to `users.json`.  
Each user is stored with their type (`User` or `AdminUser`), status, and login count.

---

## 💾 **Example `users.json` Output**
```json
[
  {
    "type": "User",
    "username": "alice",
    "password": "secret",
    "active": true,
    "login_count": 2
  },
  {
    "type": "AdminUser",
    "username": "admin",
    "password": "admin123",
    "active": true,
    "login_count": 1
  }
]
```

---

## 🧠 **Skills Practiced**
- Writing and structuring Python classes  
- Using `super()` for inheritance  
- Storing and retrieving structured data (JSON)  
- Designing logical program flow  
- Testing and debugging code  

---

## 🧪 **Sample Test Scenarios**

| Test | Input | Expected Output |
|------|--------|----------------|
| 1 | Wrong password | “Invalid credentials.” |
| 2 | Deactivated user tries to log in | “Account disabled.” |
| 3 | Duplicate username creation | “Username already exists.” |
| 4 | Saving and reloading users | User data reappears on restart |

---

## 🧰 **Requirements**
- Python 3.8 or newer  
- No external libraries required (uses built-in `json` and `typing` modules)

---

## 🧑‍💻 **How to Run**
1. Open the project folder in VS Code, PyCharm, or Replit.  
2. Run `main.py`.  
3. Follow the on-screen menu instructions.  
4. When done, choose “Save” or “Exit” to write all data to `users.json`.

---

## 🏁 **End of Program Output Example**
```
Saved 2 users to users.json.
Goodbye!
```

---

## 🏆 **About**
Created by **Connor Cain**  
Course: *Introduction to Programming in Python* (Sophia Learning → WGU BS/MS Software Engineering Pathway)  
Last updated: October 2025  
