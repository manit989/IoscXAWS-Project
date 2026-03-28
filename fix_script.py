import sys

def modify_html(filepath):
    print(f"Modifying {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_btn = '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            Change Password
          </a>'''
          
    new_btn = '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <span class="nav-item-label">Change Password</span>
          </a>'''
          
    if old_btn in content:
        content = content.replace(old_btn, new_btn)
        print("  Button Replaced.")
    else:
        print("  Button not found.")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

modify_html('w:/VS/IoscXAWS-Project/frontend/dashboard2.html')
modify_html('w:/VS/IoscXAWS-Project/frontend/my-profile.html')

## For my-profile.js 
with open('w:/VS/IoscXAWS-Project/frontend/js/pages/my-profile.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

old_js = '''  function renderBasicInfo(s) {
    document.getElementById("profileName").textContent = s.name;
    document.getElementById("profileMeta").textContent = \\ · \ · Year \\;'''

new_js = '''  function renderBasicInfo(s) {
    const el = document.getElementById("enrollmentNumber");
    if (el) el.textContent = s.roll_number;
    const metaEl = document.getElementById("profileMeta");
    if (metaEl) metaEl.textContent = \\ · \ · Year \\;'''

js_content = js_content.replace(old_js, new_js)

old_fail = 'document.getElementById("profileName").textContent = "Error loading student";'
new_fail = 'const errEl = document.getElementById("enrollmentNumber"); if (errEl) errEl.textContent = "Error loading student";'
js_content = js_content.replace(old_fail, new_fail)

with open('w:/VS/IoscXAWS-Project/frontend/js/pages/my-profile.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Done")
