import os

files = [
    r'c:\Users\naniv\Desktop\Stress Detection In It Employees\backend\users\views.py',
    r'c:\Users\naniv\Desktop\Stress Detection In It Employees\backend\admins\views.py'
]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("'users/UserHome.html'", "'user-dashboard.html'")
    content = content.replace("'admins/AdminHome.html'", "'admin-dashboard.html'")

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print('Replaced legacy paths in views')
