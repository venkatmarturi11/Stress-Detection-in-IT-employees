import os
import re

js_dir = r'c:\Users\naniv\Desktop\Stress Detection In It Employees\backend\assets\static\js'

replacements = {
    "'login.html'": "'/UserLogin/'",
    '"login.html"': '"/UserLogin/"',
    "'user-dashboard.html'": "'/UserHome/'",
    '"user-dashboard.html"': '"/UserHome/"',
    "'index.html'": "'/index/'",
    '"index.html"': '"/index/"',
    "'admin-dashboard.html'": "'/AdminHome/'",
    '"admin-dashboard.html"': '"/AdminHome/"',
    "'admin-login.html'": "'/AdminLogin/'",
    '"admin-login.html"': '"/AdminLogin/"',
    "'register.html'": "'/UserRegister/'",
    '"register.html"': '"/UserRegister/"',
    "'settings.html'": "'/settings/'",
    '"settings.html"': '"/settings/"',
    "'admin-settings.html'": "'/admin-settings/'",
    '"admin-settings.html"': '"/admin-settings/"',
    "'survey-prediction.html'": "'/survey/'",
    '"survey-prediction.html"': '"/survey/"'
}

for filename in os.listdir(js_dir):
    if not filename.endswith('.js'):
        continue
    filepath = os.path.join(js_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print('Updated all JS redirects')
