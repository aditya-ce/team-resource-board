import re

with open('app.py', 'r') as f:
    content = f.read()

# Fix TemplateResponse calls
content = re.sub(
    r'templates\.TemplateResponse\(\s*"([^"]+)",\s*\{(.*?)\}\s*\)',
    r'templates.TemplateResponse(request=request, name="\1", context={\2})',
    content,
    flags=re.DOTALL
)

with open('app.py', 'w') as f:
    f.write(content)
