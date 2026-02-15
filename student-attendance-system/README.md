# 🎓 Student Attendance System - Barcode Scanner

A complete web-based student attendance management system with real-time barcode scanning capabilities.

## 📋 Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Features
- ✅ **Real-time Barcode Scanning** - Use device camera to scan student ID barcodes
- ✅ **Manual Entry** - Alternative barcode input method
- ✅ **Live Dashboard** - Real-time attendance statistics and updates
- ✅ **Student Management** - Complete CRUD operations for student records
- ✅ **Attendance Reports** - Generate reports for custom date ranges
- ✅ **Search Functionality** - Quick search through student database
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile devices
- ✅ **Modern UI** - Smooth animations and professional styling

### Admin Features
- Add/Delete student records
- Search students by name, barcode, or class
- Generate attendance reports by date range
- View all students in the system

## 🛠 Technology Stack

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **MySQL 8.0+** - Database
- **Flask-CORS** - Cross-origin resource sharing
- **mysql-connector-python** - MySQL driver

### Frontend
- **HTML5** - Single-file architecture
- **CSS3** - Custom styling with animations
- **Vanilla JavaScript** - No framework dependencies
- **Html5-Qrcode** - Barcode scanning library
- **Google Fonts** - Syne & JetBrains Mono

## 📁 Project Structure

```
student-attendance-system/
│
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   ├── routes.py              # API endpoints
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── index.html             # Main dashboard (single file)
│   └── admin.html             # Admin panel (single file)
│
├── database/
│   └── schema.sql             # MySQL database schema
│
├── config/
│   └── config.py              # Configuration settings
│
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)
- Modern web browser with camera support

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd student-attendance-system
```

### Step 2: Database Setup
```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE student_attendance;
exit;

# Import schema
mysql -u root -p student_attendance < database/schema.sql
```

### Step 3: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and update these values:
# DB_PASSWORD=your_mysql_password
# SECRET_KEY=your_secret_key
```

### Step 4: Install Python Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Step 5: Run Application
```bash
python backend/app.py
```

### Step 6: Access Application
Open your browser and navigate to:
- **Dashboard:** http://localhost:5000/
- **Admin Panel:** http://localhost:5000/admin

## 📖 Usage

### For Students - Marking Attendance

#### Method 1: Barcode Scanner
1. Navigate to the dashboard
2. Click "Start Scanner"
3. Allow camera permissions
4. Show your ID card barcode to the camera
5. Wait for confirmation

#### Method 2: Manual Entry
1. Enter your barcode ID in the input field
2. Press Enter or click "Submit"
3. See confirmation message

### For Administrators

#### Adding Students
1. Go to Admin Panel
2. Fill in the student form:
   - Barcode ID (required)
   - Name (required)
   - Class (required)
   - Email (optional)
   - Phone (optional)
3. Click "Add Student"

#### Managing Students
- **Search:** Use search bar to find students
- **Delete:** Click delete button on student cards
- **View All:** Scroll through the student list

#### Generating Reports
1. Switch to "Reports" tab
2. Select start date
3. Select end date
4. Click "Generate Report"
5. View attendance summary

## 🔌 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Students Endpoints

#### Get All Students
```http
GET /api/students
```

#### Get Student by ID
```http
GET /api/students/{id}
```

#### Get Student by Barcode
```http
GET /api/students/barcode/{barcode_id}
```

#### Create Student
```http
POST /api/students
Content-Type: application/json

{
  "barcode_id": "STU2026001",
  "name": "John Doe",
  "class": "Computer Science - A",
  "email": "john@example.com",
  "phone": "1234567890"
}
```

#### Update Student
```http
PUT /api/students/{id}
Content-Type: application/json

{
  "name": "John Smith",
  "email": "johnsmith@example.com"
}
```

#### Delete Student
```http
DELETE /api/students/{id}
```

#### Search Students
```http
GET /api/students/search?q=keyword
```

### Attendance Endpoints

#### Mark Attendance
```http
POST /api/attendance
Content-Type: application/json

{
  "barcode_id": "STU2026001",
  "status": "present"
}
```

#### Get Today's Attendance
```http
GET /api/attendance/today
```

#### Get Attendance by Date
```http
GET /api/attendance/date/2026-02-15
```

#### Get Student Attendance History
```http
GET /api/attendance/student/{student_id}
```

#### Get Statistics
```http
GET /api/attendance/statistics
```

#### Generate Report
```http
GET /api/attendance/report?start_date=2026-02-01&end_date=2026-02-15
```

## ⚙ Configuration

### Environment Variables (.env)

```env
# Flask Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
HOST=0.0.0.0
PORT=5000

# Database Settings
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=student_attendance
```

### Customization

#### Change Colors
Edit CSS variables in `frontend/index.html` and `frontend/admin.html`:
```css
:root {
    --bg-primary: #0a0e27;
    --accent-primary: #00f5d4;
    --accent-secondary: #00bbf9;
}
```

#### Change Port
Update `.env` file:
```env
PORT=8080
```

## 🐛 Troubleshooting

### Database Connection Error
**Problem:** Can't connect to MySQL database

**Solution:**
1. Verify MySQL is running: `sudo systemctl status mysql`
2. Check credentials in `.env` file
3. Ensure database exists: `SHOW DATABASES;`

### Camera Not Working
**Problem:** Barcode scanner can't access camera

**Solution:**
1. Use HTTPS or localhost (required for camera access)
2. Grant camera permissions in browser
3. Check if another app is using the camera
4. Use manual entry as alternative

### Port Already in Use
**Problem:** Port 5000 is already in use

**Solution:**
1. Change port in `.env` file to 5001 or 8080
2. Or stop the process using port 5000

### Module Not Found Error
**Problem:** Python module import errors

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r backend/requirements.txt
```

## 📊 Database Schema

### students Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| barcode_id | VARCHAR(50) | Unique barcode identifier |
| name | VARCHAR(100) | Student name |
| class | VARCHAR(50) | Class/section |
| email | VARCHAR(100) | Email address |
| phone | VARCHAR(20) | Phone number |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

### attendance Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| student_id | INT | Foreign key to students |
| date | DATE | Attendance date |
| time | TIME | Attendance time |
| status | ENUM | present/absent/late |
| created_at | TIMESTAMP | Record creation time |

## 🧪 Testing

### Sample Data
The database comes with 15 sample students. Test with these barcodes:
- STU2026001 - Amit Kumar
- STU2026002 - Priya Sharma
- STU2026003 - Rahul Verma
- ... (12 more)

### Creating Test Barcodes
1. Visit: https://barcode.tec-it.com/en
2. Select "Code 128" or "QR Code"
3. Enter barcode ID (e.g., STU2026001)
4. Generate and print
5. Test with the scanner

## 🚀 Production Deployment

### Security Checklist
- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False`
- [ ] Use strong database passwords
- [ ] Create dedicated database user (not root)
- [ ] Enable HTTPS
- [ ] Implement user authentication
- [ ] Add rate limiting
- [ ] Regular security audits

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ for educational purposes

## 🙏 Acknowledgments

- Flask framework
- Html5-Qrcode library
- MySQL community
- All contributors

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Note:** This is a demonstration project. For production use, implement proper authentication, security measures, and error handling.