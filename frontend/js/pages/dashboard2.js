// Student Dashboard Logic

const API = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') 
  ? "http://localhost:8000" 
  : "https://estudent-cell.onrender.com";

async function loadStudentData() {
  try {
    const token = localStorage.getItem('token');
    
    if (!token) {
      window.location.href = 'login.html';
      return;
    }

    // Get current user info
    const meResponse = await fetch(`${API}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!meResponse.ok) {
      throw new Error('Failed to fetch user data');
    }

    const user = await meResponse.json();

    // Try to fetch student data if enrollment number exists
    if (user.enrollment_number) {
      try {
        const response = await fetch(`${API}/student/${user.enrollment_number}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const student = await response.json();
          document.getElementById('enrollmentNumber').textContent = student.roll_number || user.enrollment_number;
          document.getElementById('studentName').textContent = student.name || '—';
          document.getElementById('studentBranch').textContent = student.branch || '—';
          document.getElementById('studentYear').textContent = student.year || '—';
          const headerPhoto = document.getElementById('headerProfilePhoto');
          if (headerPhoto && student.photo_path) {
            const photoUrl = student.photo_path.startsWith('http') ? student.photo_path : `${API}${student.photo_path.startsWith('/') ? '' : '/'}${student.photo_path}`;
            headerPhoto.innerHTML = `<img src="${photoUrl}" alt="${student.name}" style="width: 100%; height: 100%; object-fit: cover;">`;
          }

          // Calculate Profile Completion
          let completed = 0;
          const totalDocs = 10;
          if (student.classification) completed++;
          if (student.parent_details) completed++;
          if (student.academic_records) completed++;
          if (student.financial_info) completed++;
          if (student.internships && student.internships.length > 0) completed++;
          if (student.research_papers && student.research_papers.length > 0) completed++;
          if (student.documents) completed++;
          if (student.noc_records) completed++;
          if (student.placement) completed++;
          if (student.academic_documents) completed++;

          let pcent = Math.round((completed / totalDocs) * 100);
          const chartEl = document.getElementById('profileCompletionChart');
          const textEl = document.getElementById('profileCompletionText');
          if (chartEl && textEl) {
            chartEl.style.background = `conic-gradient(var(--accent) ${pcent}%, var(--bg-3) 0%)`;
            textEl.textContent = `${pcent}%`;
          }

          // Calculate Profile Completion
          let completed = 0;
          const totalDocs = 10;
          if (student.classification) completed++;
          if (student.parent_details) completed++;
          if (student.academic_records) completed++;
          if (student.financial_info) completed++;
          if (student.internships && student.internships.length > 0) completed++;
          if (student.research_papers && student.research_papers.length > 0) completed++;
          if (student.documents) completed++;
          if (student.noc_records) completed++;
          if (student.placement) completed++;
          if (student.academic_documents) completed++;

          let pcent = Math.round((completed / totalDocs) * 100);
          const chartEl = document.getElementById('profileCompletionChart');
          const textEl = document.getElementById('profileCompletionText');
          if (chartEl && textEl) {
            chartEl.style.background = `conic-gradient(var(--accent) ${pcent}%, var(--bg-3) 0%)`;
            textEl.textContent = `${pcent}%`;
          }
        }
      } catch (error) {
        console.log('Could not fetch student details:', error);
      }
    }
  } catch (error) {
    console.error('Error loading student data:', error);
  }
}

// Show account settings
function showAccountSettings() {
  alert('Account settings will be available soon. You can currently change your password in your profile settings.');
}

// Load data on page load
document.addEventListener('DOMContentLoaded', () => {
  // Check if user is logged in as student
  const role = localStorage.getItem('role');
  const token = localStorage.getItem('token');
  
  if (!token || role !== 'student') {
    window.location.href = 'login.html';
    return;
  }

  loadStudentData();
});
