import re

with open('w:/VS/IoscXAWS-Project/frontend/js/pages/my-profile.js', 'r', encoding='utf-8') as f:
    js = f.read()

pattern = r'(function renderBasicInfo\(s\) \{\n.*?document\.getElementById\("profileMeta"\)\.textContent = .*?;)'

replacement = r'''\1

  const headerPhoto = document.getElementById("headerProfilePhoto");
  if (headerPhoto) {
    if (s.photo_path) {
      headerPhoto.innerHTML = `<img src="${getPhotoUrl(s.photo_path)}" alt="${s.name}" style="width: 100%; height: 100%; object-fit: cover;">`;
    } else {
      headerPhoto.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`;
    }
  }'''

new_js = re.sub(pattern, replacement, js, flags=re.DOTALL)

with open('w:/VS/IoscXAWS-Project/frontend/js/pages/my-profile.js', 'w', encoding='utf-8') as f:
    f.write(new_js)
