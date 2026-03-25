
# Smart Internship Portal

A responsive web application to browse, apply, and manage internships efficiently. Built with **Flask** for backend and **HTML/CSS/JS** for frontend.

---

## 🛠️ Features

- User registration and login for **Students** and **Companies**  
- Students can:
  - Create and manage profiles
  - Browse internships
  - Apply for internships
- Companies can:
  - Post internships
  - View applicant details
- Responsive UI with mobile-friendly **hamburger menu**  
- Interactive hero slider on the landing page  
- LinkedIn-style profile navigation  
- Secure password handling and session management

---

## 💻 Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite (or your choice)  
- **Version Control:** Git & GitHub  

---

## 📁 Project Structure


smart_internship_portal/
├─ app/
│ ├─ templates/
│ ├─ static/
│ │ ├─ css/
│ │ ├─ js/
│ │ └─ uploads/
│ ├─ routes/
│ └─ init.py
├─ env/ # Python virtual environment
├─ requirements.txt
├─ run.py
└─ README.md


---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/shrawi10317/smart-internship-portal.git
cd smart-internship-portal
Create and activate virtual environment:
python -m venv env
# Windows
env\Scripts\activate
# Mac/Linux
source env/bin/activate
Install dependencies:
pip install -r requirements.txt
Run the app:
python run.py
Open in browser:
http://127.0.0.1:5000
