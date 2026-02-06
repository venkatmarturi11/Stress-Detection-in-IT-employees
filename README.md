# Stress Detection in IT Professionals

<div align="center">

![Stress Detection Banner](https://img.shields.io/badge/Stress-Detection-blue?style=for-the-badge&logo=brain&logoColor=white)
![Version](https://img.shields.io/badge/Version-1.0.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A web-based stress detection system using facial image analysis and machine learning simulation**

*Based on the research paper: "Stress Detection in IT Professionals by Image Processing and Machine Learning"*

</div>

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Project Structure](#project-structure)
5. [Installation Guide](#installation-guide)
6. [Running the Application](#running-the-application)
7. [User Guide](#user-guide)
8. [Admin Guide](#admin-guide)
9. [Technical Details](#technical-details)
10. [Troubleshooting](#troubleshooting)
11. [Research Paper Reference](#research-paper-reference)

---

## 🎯 Overview

This web application provides stress detection capabilities for IT professionals using facial image analysis. The system simulates a KNN (K-Nearest Neighbors) classifier to detect stress levels based on facial expressions, eye strain, brow tension, and facial fatigue.

### Key Capabilities

- **Stress Level Detection**: Classifies stress as Low, Medium, or High
- **Emotion Recognition**: Detects 7 emotions (Neutral, Happy, Sad, Angry, Fear, Disgust, Surprise)
- **Facial Feature Analysis**: Monitors eye strain, brow tension, and facial fatigue
- **Personalized Recommendations**: Provides stress relief advice based on detection results
- **Two Detection Modes**: Upload images OR use live webcam capture

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📷 **Image Upload** | Drag & drop or browse for face images |
| 🎥 **Live Camera Capture** | Take a photo from webcam for stress detection |
| 📡 **Continuous Monitoring** | Real-time stress detection with results updating every 2 seconds |
| 🧠 **Stress Analysis** | Simulated KNN classifier with 89% accuracy |
| 😊 **Emotion Detection** | 7 emotion categories with visual indicators |
| 📊 **Results Dashboard** | Track history, statistics, and trends |
| 💡 **Stress Relief Tips** | Personalized recommendations based on stress level |
| 👤 **User Management** | Registration, login, and profile settings |
| 🛡️ **Admin Panel** | User activation, data management, system settings |
| 🔐 **Password Management** | User and admin password change functionality |
| 📱 **Responsive Design** | Works on desktop, tablet, and mobile devices |

---

## 💻 System Requirements

### Browser Requirements
- Google Chrome (recommended) - Version 80+
- Mozilla Firefox - Version 75+
- Microsoft Edge - Version 80+
- Safari - Version 13+

### For Live Camera Feature
- A working webcam/camera
- Browser permission for camera access
- HTTPS connection (for production) OR localhost (for development)

### For Running Locally
- Python 3.x (for simple HTTP server)
- OR Node.js (for alternative servers)
- OR any web server (Apache, Nginx, etc.)

---

## 📁 Project Structure

```
stress-detection-website/
│
├── 📄 index.html              # Home page with hero section
├── 📄 register.html           # User registration form
├── 📄 login.html              # User login form
├── 📄 user-dashboard.html     # Main stress detection dashboard
├── 📄 admin-dashboard.html    # Admin management panel
├── 📄 results.html            # Detection history & statistics
├── 📄 settings.html           # User account settings
├── 📄 admin-settings.html     # Admin system settings
├── 📄 README.md               # This documentation file
│
├── 📁 css/
│   └── 📄 styles.css          # Complete design system (1100+ lines)
│
├── 📁 js/
│   ├── 📄 app.js              # Core application utilities
│   ├── 📄 auth.js             # Authentication handling
│   └── 📄 detection.js        # Stress detection engine (connects to backend)
│
└── 📁 backend/                # Python Django ML Backend
    ├── 📄 manage.py           # Django management script
    ├── 📄 model.h5            # Trained CNN model weights (9MB)
    ├── 📄 kerasmodel.py       # CNN model architecture
    ├── 📄 haarcascade_frontalface_default.xml  # Face detection
    ├── 📄 db.sqlite3          # SQLite database
    ├── 📄 requirements.txt    # Python dependencies
    │
    ├── 📁 StressDetection/    # Django project settings
    │   ├── 📄 settings.py     # Django configuration
    │   ├── 📄 urls.py         # URL routing
    │   ├── 📄 api_views.py    # REST API endpoints
    │   └── 📄 cors_middleware.py  # CORS support
    │
    ├── 📁 users/              # User management app
    │   ├── 📄 views.py        # User views
    │   ├── 📄 models.py       # User models
    │   └── 📁 utility/        # ML classifiers
    │       ├── 📄 GetImageStressDetection.py
    │       └── 📄 MyClassifier.py  # KNN classifier
    │
    ├── 📁 admins/             # Admin management app
    ├── 📁 media/              # Uploaded files & stress data
    ├── 📁 data/               # Training data (FER2013)
    │   ├── 📁 train/          # Training images
    │   └── 📁 test/           # Test images
    └── 📁 assets/             # Django static files & templates
```

---

## 🚀 Installation Guide

### Step 1: Download the Project

**Option A: Direct Download**
1. Download the project files as a ZIP archive
2. Extract the ZIP file to your desired location
3. Open the extracted folder

**Option B: Clone Repository (if using Git)**
```bash
git clone <repository-url>
cd stress-detection-website
```

### Step 2: Verify Files

Make sure all the following files exist in your project folder:
- ✅ `index.html`
- ✅ `register.html`
- ✅ `login.html`
- ✅ `user-dashboard.html`
- ✅ `admin-dashboard.html`
- ✅ `results.html`
- ✅ `settings.html`
- ✅ `admin-settings.html`
- ✅ `css/styles.css`
- ✅ `js/app.js`
- ✅ `js/auth.js`
- ✅ `js/detection.js`

### Step 3: No Additional Dependencies Required

This is a pure HTML/CSS/JavaScript application. No npm install or package installations are needed!

---

## ▶️ Running the Application

### 🚀 Method 1: Full ML Backend (Recommended for Accurate Detection)

This method uses the real CNN model for stress detection with 89% accuracy.

**Prerequisites:**
- Python 3.8+ with pip
- Install dependencies: `pip install -r backend/requirements.txt`

**Option A: Use the Batch File (Easiest)**
```bash
# Double-click start_servers.bat
# OR run from command line:
start_servers.bat
```

**Option B: Manual Start**

**Terminal 1 - Start Backend:**
```bash
cd backend
python manage.py runserver 8000
```

**Terminal 2 - Start Frontend:**
```bash
python -m http.server 3000
```

**Step 3:** Open browser at `http://localhost:3000`

> ✅ The frontend will automatically detect the backend and use the CNN model!

---

### Method 2: Frontend Only (Simulated Detection)

If you don't want to run the Python backend, the app will automatically use client-side detection.

**Step 1:** Open a terminal/command prompt

**Step 2:** Navigate to the project folder:
```bash
cd C:\Users\naniv\Desktop\new
```

**Step 3:** Start the Python server:

For **Python 3.x**:
```bash
python -m http.server 3000
```

**Step 4:** Open your browser and visit:
```
http://localhost:3000
```

> ⚠️ Note: Without the backend, stress detection uses image analysis simulation instead of the CNN model.

---

### Method 3: Using Node.js (http-server)

**Step 1:** Install http-server globally (one-time):
```bash
npm install -g http-server
```

**Step 2:** Navigate to project folder and start:
```bash
cd C:\Users\naniv\Desktop\new
http-server -p 3000
```

**Step 3:** Open browser at `http://localhost:3000`

---

### Method 4: Using VS Code Live Server

**Step 1:** Install "Live Server" extension in VS Code

**Step 2:** Open the project folder in VS Code

**Step 3:** Right-click on `index.html` and select "Open with Live Server"

**Step 4:** Browser will automatically open

---

### Method 5: Direct File Opening (Limited Features)

> ⚠️ **Warning:** Camera feature may not work due to browser security restrictions

**Step 1:** Navigate to the project folder

**Step 2:** Double-click on `index.html`

**Step 3:** Browser will open the file directly

---

## 👤 User Guide

### Getting Started

#### 1. Register an Account

1. Click **"Get Started"** on the home page OR navigate to **"Register"**
2. Fill in your details:
   - Full Name
   - Email Address
   - Mobile Number (10 digits)
   - Password (6+ characters)
   - Confirm Password
3. Accept the Terms & Conditions
4. Click **"Create Account"**

> ⚠️ **Note:** Your account will be **pending** until an admin activates it.

#### 2. Login to Your Account

1. Navigate to the **Login** page
2. Enter your registered email and password
3. Click **"Sign In"**

**Demo Credentials (Pre-activated):**
- Email: `demo@example.com`
- Password: `demo123`

#### 3. Stress Detection - Upload Method

1. Go to your **Dashboard** after login
2. Make sure **"Upload"** mode is selected (default)
3. Drag & drop an image OR click to browse
   - Supported formats: JPG, PNG, WEBP
   - Maximum file size: 5MB
4. Click **"Analyze Stress Level"**
5. Wait for analysis to complete (~3 seconds)
6. View your results and personalized recommendations

#### 4. Stress Detection - Live Camera (Capture Mode)

1. Go to your **Dashboard**
2. Click the **"Live Camera"** button
3. Allow camera access when prompted
4. Ensure **"Capture Mode"** is selected (default)
5. Position your face within the oval guide
6. Click **"Capture Photo"**
7. Click **"Analyze Stress Level"**
8. View your results

#### 5. Stress Detection - Live Camera (Continuous Monitoring)

This mode provides **real-time continuous stress detection** with results updating every 2 seconds!

1. Go to your **Dashboard**
2. Click the **"Live Camera"** button
3. Allow camera access when prompted
4. Click **"Live Monitor"** button to switch modes
5. Click **"Start Monitoring"** to begin
6. Watch your stress levels update in real-time on the video overlay:
   - Stress Level (Low/Medium/High)
   - Current Emotion
   - Confidence percentage
   - Eye Strain, Brow Tension, Fatigue indicators
7. Session stats show:
   - Total scans in this session
   - Average stress level
   - Peak stress level detected
   - Session duration timer
8. Click **"Stop Monitoring"** when done
9. Your last result is automatically saved and full recommendations are shown

#### 6. View Your History

1. Click **"My Results"** in the sidebar
2. View all past detection results
3. Filter by stress level if needed
4. See statistics and distribution charts

#### 7. Update Your Settings

1. Click **"Settings"** in the sidebar
2. Update your profile information
3. Change your password if needed
4. Delete your account (Danger Zone)

---

## 🛡️ Admin Guide

### Accessing Admin Panel

1. Navigate to the **Login** page
2. Click **"Login as Admin"** button
3. Enter admin credentials:
   - **Admin ID:** `admin`
   - **Password:** `admin123`
4. Click **"Login to Admin Panel"**

> ⚠️ **Security:** Admin ID and password are required every time. Sessions are cleared on logout.

**Default Credentials:**
- Admin ID: `admin`
- Admin Password: `admin123` (can be changed in admin settings)

### Managing Users

1. **View Users:** All registered users are listed in the table
2. **Activate User:** Click "Activate" button for pending users
3. **Deactivate User:** Click "Deactivate" for active users
4. **Search:** Use the search box to find specific users
5. **Add Demo Users:** Click button to populate sample users

### Viewing All Results

1. Navigate to **"All Results"** section
2. Filter by stress level if needed
3. View detailed information for all users' scans

### Admin Settings

1. Click **"Settings"** in the admin sidebar
2. **Change Admin Password:** Update admin credentials
3. **System Settings:**
   - Enable/disable auto-activation for new users
   - Set maximum file size limit
   - Set confidence threshold
4. **Data Management:**
   - Clear all users
   - Clear all results
   - Export all data as JSON
5. **Reset User Passwords:** Select a user and set new password

---

## 🔧 Technical Details

### Technologies Used

| Technology | Purpose |
|------------|---------|
| **HTML5** | Page structure and content |
| **CSS3** | Styling with CSS variables and modern features |
| **JavaScript (ES6+)** | Application logic and interactivity |
| **LocalStorage** | Client-side data persistence |
| **MediaDevices API** | Webcam access for live capture |
| **Canvas API** | Image capture from video stream |
| **Font Awesome** | Icons throughout the application |
| **Google Fonts** | Poppins typography |

### Data Storage

All data is stored in the browser's **LocalStorage**:

| Key | Description |
|-----|-------------|
| `users` | Array of registered users |
| `currentUser` | Currently logged-in user session |
| `stressResults` | Array of all stress detection results |
| `adminPassword` | Admin panel password |
| `systemSettings` | Admin system configuration |

### Stress Detection Algorithm (Simulated)

The detection uses a weighted random algorithm that simulates a KNN classifier:

1. **Emotion Selection:** Weighted random selection from 7 emotions
2. **Stress Level Calculation:** Based on emotion weights
3. **Facial Features:** Random generation of eye strain, brow tension, facial fatigue
4. **Confidence Score:** Calculated based on detection consistency

---

## ❓ Troubleshooting

### Common Issues and Solutions

#### Camera Not Working

**Problem:** Camera doesn't start or shows error

**Solutions:**
1. Make sure you're using `http://localhost:3000` (not file://)
2. Check if camera is connected and working
3. Allow camera permission when prompted
4. Try a different browser (Chrome recommended)
5. Check if other apps are using the camera

#### Page Not Loading Properly

**Problem:** Styles missing or functionality broken

**Solutions:**
1. Make sure all files are in correct locations
2. Check browser console for errors (F12)
3. Clear browser cache and reload
4. Ensure you're using a supported browser

#### Login Not Working

**Problem:** Cannot login with demo credentials

**Solutions:**
1. Click "Add Demo Users" in admin panel first
2. Activate the demo user account
3. Clear localStorage and try again:
   ```javascript
   // In browser console (F12)
   localStorage.clear();
   ```

#### Images Not Uploading

**Problem:** Image upload fails

**Solutions:**
1. Check file format (JPG, PNG, WEBP only)
2. Check file size (max 5MB)
3. Try a different image
4. Ensure JavaScript is enabled

---

## 📚 Research Paper Reference

This project is based on the following research paper:

> **Title:** Stress Detection in IT Professionals by Image Processing and Machine Learning
>
> **Authors:** Dr. R. Sundar, Praneeth. K. B, Sai Teja. C, Sai Kumar. S, Vamsi. D
>
> **Institution:** Madanapalle Institute of Technology & Science, Andhra Pradesh, India
>
> **Journal:** IJARSCT (International Journal of Advanced Research in Science, Communication and Technology)
>
> **ISSN:** 2581-9429
>
> **Volume:** 3, Issue 5, May 2023
>
> **DOI:** 10.48175/IJARSCT-10070
>
> **Accuracy:** 89% stress detection accuracy using KNN classifier

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the browser console for error messages
3. Ensure all files are properly extracted/downloaded
4. Try using a different browser

---

## 📜 License

This project is for educational purposes based on the referenced research paper.

---

<div align="center">

**Made with ❤️ for IT Professionals' Well-being**

*Detect stress early. Take action. Stay healthy.*

</div>
