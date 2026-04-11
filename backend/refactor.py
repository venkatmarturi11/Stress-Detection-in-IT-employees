import os
import re

template_dir = r'c:\Users\naniv\Desktop\Stress Detection In It Employees\backend\assets\templates'

files_to_process = [
    'admin-dashboard.html', 'admin-login.html', 'admin-settings.html', 
    'index.html', 'login.html', 'register.html', 'results.html', 'settings.html', 
    'survey-prediction.html', 'user-dashboard.html'
]

replacements = {
    'href=\"login.html\"': 'href=\"{% url \\\'UserLogin\\\' %}\"',
    'href=\"admin-login.html\"': 'href=\"{% url \\\'AdminLogin\\\' %}\"',
    'href=\"register.html\"': 'href=\"{% url \\\'UserRegister\\\' %}\"',
    'href=\"index.html\"': 'href=\"{% url \\\'index\\\' %}\"',
    'href=\"user-dashboard.html\"': 'href=\"{% url \\\'UserHome\\\' %}\"',
    'href=\"admin-dashboard.html\"': 'href=\"{% url \\\'AdminHome\\\' %}\"',
    'href=\"results.html\"': 'href=\"{% url \\\'user_results\\\' %}\"',
    'href=\"settings.html\"': 'href=\"{% url \\\'user_settings\\\' %}\"',
    'href=\"admin-settings.html\"': 'href=\"{% url \\\'admin_settings\\\' %}\"',
    'href=\"survey-prediction.html\"': 'href=\"{% url \\\'survey_prediction\\\' %}\"'
}

for filename in files_to_process:
    filepath = os.path.join(template_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Inject load static
    if '{% load static %}' not in content:
        content = '{% load static %}\\n' + content
        
    # Replace static files CSS / JS
    content = re.sub(r'href=\"(css/[^\"]+)\"', r'href=\"{% static \'\1\' %}\"', content)
    content = re.sub(r'src=\"(js/[^\"]+)\"', r'src=\"{% static \'\1\' %}\"', content)

    # Note: query parameters in css/js e.g. css/styles.css?v=2.1
    # Django static tag doesn't take query params nicely inside the string like 'css/styles.css?v=2.1'
    # Wait, {% static 'css/styles.css' %}?v=2.1 is the right way if query string exists.
    # So I should handle the ?v=2.1 separately!
    # Let's fix that by regex.
    content = re.sub(r'href=\"{% static \'(css/[^\?]+)\?([^\']+)\' %}\"', r'href=\"{% static \'\1\' %}?\2\"', content)
    content = re.sub(r'src=\"{% static \'(js/[^\?]+)\?([^\']+)\' %}\"', r'src=\"{% static \'\1\' %}?\2\"', content)

    # Route URLs
    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done!')
