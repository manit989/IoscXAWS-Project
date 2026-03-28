import re

with open('w:/VS/IoscXAWS-Project/frontend/js/pages/dashboard2.js', 'r', encoding='utf-8') as f:
    js = f.read()

pattern = r"(document\.getElementById\('studentYear'\)\.textContent = student\.year \|\| .*?;)"

replacement = r'''\1
          const headerPhoto = document.getElementById('headerProfilePhoto');
          if (headerPhoto && student.photo_path) {
            const photoUrl = student.photo_path.startsWith('http') ? student.photo_path : `${API}${student.photo_path.startsWith('/') ? '' : '/'}${student.photo_path}`;
            headerPhoto.innerHTML = `<img src="${photoUrl}" alt="${student.name}" style="width: 100%; height: 100%; object-fit: cover;">`;
          }'''

new_js = re.sub(pattern, replacement, js)

with open('w:/VS/IoscXAWS-Project/frontend/js/pages/dashboard2.js', 'w', encoding='utf-8') as f:
    f.write(new_js)
