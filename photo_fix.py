import re

with open("w:/VS/IoscXAWS-Project/frontend/js/change-password.js", "r", encoding="utf-8") as f:
    js = f.read()

pattern = r"async function submitChangePassword\(e\) \{[\s\S]*?(?=\}\n\n// Check authentication on load)"

replacement = """async function submitChangePassword(e) {
  e.preventDefault();
  
  const currentPassword = document.getElementById('currentPassword').value;
  const newPassword = document.getElementById('newPassword').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  const photoFile = document.getElementById('studentPhoto').files[0];
  const submitBtn = document.getElementById('submitBtn');
  
  // Validation
  if (!currentPassword || !newPassword || !confirmPassword) {
    showAlert('Please fill in all password fields', 'error');
    return;
  }
  
  if (!photoFile) {
    showAlert('Please select a profile photograph', 'error');
    return;
  }
  
  if (newPassword !== confirmPassword) {
    showAlert('New passwords do not match', 'error');
    return;
  }
  
  if (newPassword.length < 8) {
    showAlert('New password must be at least 8 characters', 'error');
    return;
  }
  
  if (currentPassword === newPassword) {
    showAlert('New password must be different from current password', 'error');
    return;
  }
  
  submitBtn.disabled = true;
  
  try {
    const token = localStorage.getItem('token');
    
    if (!token) {
      showAlert('No authentication token found. Please login again.', 'error');
      window.location.href = 'login.html';
      return;
    }

    // First get the student ID
    const meResponse = await fetch(`${API}/auth/me`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (!meResponse.ok) {
      throw new Error('Could not identify user');
    }
    const userData = await meResponse.json();
    const studentId = userData.enrollment_number || userData.username;
    
    // Change password
    const pwdResponse = await fetch(`${API}/account/change-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        old_password: currentPassword,
        new_password: newPassword
      })
    });
    
    if (!pwdResponse.ok) {
      const error = await pwdResponse.json();
      showAlert(error.detail || 'Failed to change password', 'error');
      submitBtn.disabled = false;
      return;
    }

    // Upload photo
    const formData = new FormData();
    formData.append('photo', photoFile);

    const photoResponse = await fetch(`${API}/students/${studentId}/photo`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    if (!photoResponse.ok) {
      const error = await photoResponse.json();
      showAlert(error.detail || 'Password changed, but photo upload failed!', 'error');
      submitBtn.disabled = false;
      return;
    }
    
    // Update flag and redirect
    localStorage.setItem('must_change_password', 'false');
    showAlert('Password changed and photo uploaded! Redirecting...', 'success');
    
    setTimeout(() => {
      window.location.href = 'dashboard2.html';
    }, 1500);
  } catch (error) {
    console.error('Change password error:', error);
    showAlert('Connection error. Please try again.', 'error');
    submitBtn.disabled = false;
  }
"""

new_js = re.sub(pattern, replacement, js)

with open("w:/VS/IoscXAWS-Project/frontend/js/change-password.js", "w", encoding="utf-8") as f:
    f.write(new_js)
