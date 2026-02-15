-- Student Attendance System Database Schema
-- MySQL Database

-- Create database
CREATE DATABASE IF NOT EXISTS student_attendance;
USE student_attendance;

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barcode_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    class VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_barcode (barcode_id),
    INDEX idx_class (class)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    status ENUM('present', 'absent', 'late') DEFAULT 'present',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    INDEX idx_student (student_id),
    INDEX idx_date (date),
    INDEX idx_status (status),
    UNIQUE KEY unique_attendance (student_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Admin users table (optional for future authentication)
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample students
INSERT INTO students (barcode_id, name, class, email, phone) VALUES
('STU2026001', 'Amit Kumar', 'Computer Science - A', 'amit.kumar@example.com', '9876543210'),
('STU2026002', 'Priya Sharma', 'Computer Science - A', 'priya.sharma@example.com', '9876543211'),
('STU2026003', 'Rahul Verma', 'Computer Science - A', 'rahul.verma@example.com', '9876543212'),
('STU2026004', 'Sneha Desai', 'Computer Science - B', 'sneha.desai@example.com', '9876543213'),
('STU2026005', 'Vikram Khan', 'Computer Science - A', 'vikram.khan@example.com', '9876543214'),
('STU2026006', 'Anjali Patel', 'Computer Science - B', 'anjali.patel@example.com', '9876543215'),
('STU2026007', 'Rohan Singh', 'Computer Science - A', 'rohan.singh@example.com', '9876543216'),
('STU2026008', 'Meera Joshi', 'Computer Science - B', 'meera.joshi@example.com', '9876543217'),
('STU2026009', 'Karan Mehta', 'Computer Science - A', 'karan.mehta@example.com', '9876543218'),
('STU2026010', 'Neha Gupta', 'Computer Science - C', 'neha.gupta@example.com', '9876543219'),
('STU2026011', 'Sanjay Reddy', 'Computer Science - B', 'sanjay.reddy@example.com', '9876543220'),
('STU2026012', 'Divya Nair', 'Computer Science - C', 'divya.nair@example.com', '9876543221'),
('STU2026013', 'Arjun Kapoor', 'Computer Science - A', 'arjun.kapoor@example.com', '9876543222'),
('STU2026014', 'Pooja Iyer', 'Computer Science - B', 'pooja.iyer@example.com', '9876543223'),
('STU2026015', 'Ravi Malhotra', 'Computer Science - C', 'ravi.malhotra@example.com', '9876543224');

-- Insert sample attendance records for today
INSERT INTO attendance (student_id, date, time, status) VALUES
(1, CURDATE(), '09:15:00', 'present'),
(2, CURDATE(), '09:12:00', 'present'),
(3, CURDATE(), '09:10:00', 'present'),
(4, CURDATE(), '09:08:00', 'present'),
(5, CURDATE(), '09:05:00', 'present'),
(6, CURDATE(), '09:03:00', 'present'),
(7, CURDATE(), '09:00:00', 'present');

-- View to get attendance summary
CREATE OR REPLACE VIEW attendance_summary AS
SELECT 
    s.id,
    s.barcode_id,
    s.name,
    s.class,
    COUNT(a.id) as total_days_present,
    MAX(a.date) as last_attendance_date
FROM students s
LEFT JOIN attendance a ON s.id = a.student_id
GROUP BY s.id, s.barcode_id, s.name, s.class;

-- View to get today's attendance
CREATE OR REPLACE VIEW todays_attendance AS
SELECT 
    a.id,
    s.barcode_id,
    s.name,
    s.class,
    a.date,
    a.time,
    a.status,
    a.created_at
FROM attendance a
INNER JOIN students s ON a.student_id = s.id
WHERE a.date = CURDATE()
ORDER BY a.time DESC;