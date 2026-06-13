import os

html_file = r"c:\VIRAS\OneDrive\Desktop\Diet_Project\front\templates\result.html"
css_file = r"c:\VIRAS\OneDrive\Desktop\Diet_Project\front\static\css\result.css"

with open(html_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if '<style>' in line:
        start_idx = i
    if '</style>' in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    css_content = "".join(lines[start_idx+1:end_idx])
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
        
    new_lines = lines[:start_idx] + ["    <link rel=\"stylesheet\" href=\"{% static 'css/result.css' %}\">\n"] + lines[end_idx+1:]
    with open(html_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Successfully moved CSS to result.css")
else:
    print("Could not find style tags")
