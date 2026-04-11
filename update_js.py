import os

filepath = r'c:\Users\naniv\Desktop\Stress Detection In It Employees\backend\assets\static\js\auth.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("window.location.href = 'login.html';", "window.location.href = '/UserLogin/';")
content = content.replace("window.location.href = 'user-dashboard.html';", "window.location.href = '/UserHome/';")
content = content.replace("window.location.href = 'index.html';", "window.location.href = '/index/';")
content = content.replace("window.location.href = 'admin-dashboard.html';", "window.location.href = '/AdminHome/';")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated auth.js redirects')
