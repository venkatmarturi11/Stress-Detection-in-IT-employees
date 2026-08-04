import os

template_dir = r'c:\Users\naniv\Desktop\Stress Detection In It Employees\backend\assets\templates'

for filename in os.listdir(template_dir):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix escaped double quotes
    content = content.replace(r'\"', '"')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print('Fixed double quotes')
