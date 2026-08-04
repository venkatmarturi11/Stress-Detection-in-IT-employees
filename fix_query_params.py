import os
import re

template_dir = r'c:\Users\naniv\Desktop\Stress Detection In It Employees\backend\assets\templates'

for filename in os.listdir(template_dir):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match {% static 'path?v=2.1' %} and change to {% static 'path' %}?v=2.1
    content = re.sub(r'\{%\s*static\s+[\'"]([^\'?"]+)\?([^\'"]+)[\'"]\s*%\}', r"{% static '\1' %}?\2", content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print('Fixed static query params')
