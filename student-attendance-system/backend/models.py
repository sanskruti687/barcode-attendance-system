"""
Database models and operations for Student Attendance System
"""
import mysql.connector
from mysql.connector import Error, pooling
from datetime import datetime, date
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config


class Database:
    """Database connection handler using connection pooling"""
    
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls):
        """Initialize connection pool"""
        try:
            cls._connection_pool = pooling.MySQLConnectionPool(
                **Config.get_db_config()
            )
            print("✓ Database connection pool created successfully")
        except Error as e:
            print(f"✗ Error creating connection pool: {e}")
            raise
    
    @classmethod
    def get_connection(cls):
        """Get connection from pool"""
        if cls._connection_pool is None:
            cls.initialize_pool()
        return cls._connection_pool.get_connection()
    
    @classmethod
    def execute_query(cls, query, params=None, fetch=True):
        """Execute a query and return results"""
        connection = None
        cursor = None
        try:
            connection = cls.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.lastrowid
                
        except Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


class Student:
    """Student model"""
    
    @staticmethod
    def get_all():
        """Get all students"""
        query = "SELECT * FROM students ORDER BY name"
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(student_id):
        """Get student by ID"""
        query = "SELECT * FROM students WHERE id = %s"
        result = Database.execute_query(query, (student_id,))
        return result[0] if result else None
    
    @staticmethod
    def get_by_barcode(barcode_id):
        """Get student by barcode ID"""
        query = "SELECT * FROM students WHERE barcode_id = %s"
        result = Database.execute_query(query, (barcode_id,))
        return result[0] if result else None
    
    @staticmethod
    def create(barcode_id, name, class_name, email=None, phone=None):
        """Create new student"""
        query = """
            INSERT INTO students (barcode_id, name, class, email, phone)
            VALUES (%s, %s, %s, %s, %s)
        """
        return Database.execute_query(
            query, 
            (barcode_id, name, class_name, email, phone),
            fetch=False
        )
    
    @staticmethod
    def update(student_id, barcode_id, name, class_name, email=None, phone=None):
        """Update student information"""
        query = """
            UPDATE students 
            SET barcode_id = %s, name = %s, class = %s, email = %s, phone = %s
            WHERE id = %s
        """
        Database.execute_query(
            query,
            (barcode_id, name, class_name, email, phone, student_id),
            fetch=False
        )
        return True
    
    @staticmethod
    def delete(student_id):
        """Delete student"""
        query = "DELETE FROM students WHERE id = %s"
        Database.execute_query(query, (student_id,), fetch=False)
        return True
    
    @staticmethod
    def search(keyword):
        """Search students by name, barcode, or class"""
        query = """
            SELECT * FROM students 
            WHERE name LIKE %s OR barcode_id LIKE %s OR class LIKE %s
            ORDER BY name
        """
        search_term = f"%{keyword}%"
        return Database.execute_query(query, (search_term, search_term, search_term))


class Attendance:
    """Attendance model"""
    
    @staticmethod
    def mark_attendance(student_id, status='present'):
        """Mark attendance for a student"""
        today = date.today()
        current_time = datetime.now().time()
        
        # Check if already marked today
        check_query = """
            SELECT id FROM attendance 
            WHERE student_id = %s AND date = %s
        """
        existing = Database.execute_query(check_query, (student_id, today))
        
        if existing:
            # Update existing record
            query = """
                UPDATE attendance 
                SET time = %s, status = %s
                WHERE student_id = %s AND date = %s
            """
            Database.execute_query(query, (current_time, status, student_id, today), fetch=False)
            return existing[0]['id']
        else:
            # Insert new record
            query = """
                INSERT INTO attendance (student_id, date, time, status)
                VALUES (%s, %s, %s, %s)
            """
            return Database.execute_query(
                query,
                (student_id, today, current_time, status),
                fetch=False
            )
    
    @staticmethod
    def get_today_attendance():
        """Get today's attendance records"""
        query = """
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
            ORDER BY a.time DESC
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_date(target_date):
        """Get attendance records for a specific date"""
        query = """
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
            WHERE a.date = %s
            ORDER BY a.time DESC
        """
        return Database.execute_query(query, (target_date,))
    
    @staticmethod
    def get_by_student(student_id):
        """Get all attendance records for a student"""
        query = """
            SELECT 
                a.id,
                a.date,
                a.time,
                a.status,
                a.created_at
            FROM attendance a
            WHERE a.student_id = %s
            ORDER BY a.date DESC, a.time DESC
        """
        return Database.execute_query(query, (student_id,))
    
    @staticmethod
    def get_statistics():
        """Get attendance statistics"""
        queries = {
            'today_count': "SELECT COUNT(*) as count FROM attendance WHERE date = CURDATE()",
            'total_students': "SELECT COUNT(*) as count FROM students",
            'today_rate': """
                SELECT 
                    COALESCE((COUNT(a.id) * 100.0 / NULLIF((SELECT COUNT(*) FROM students), 0)), 0) as rate
                FROM attendance a
                WHERE a.date = CURDATE()
            """
        }
        
        stats = {}
        for key, query in queries.items():
            result = Database.execute_query(query)
            if key == 'today_rate':
                stats[key] = round(result[0]['rate'], 2) if result[0]['rate'] else 0
            else:
                stats[key] = result[0]['count']
        
        return stats
    
    @staticmethod
    def get_date_range_report(start_date, end_date):
        """Get attendance report for date range"""
        query = """
            SELECT 
                s.barcode_id,
                s.name,
                s.class,
                COUNT(a.id) as days_present,
                GROUP_CONCAT(DATE_FORMAT(a.date, '%Y-%m-%d') ORDER BY a.date) as dates
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id 
                AND a.date BETWEEN %s AND %s
            GROUP BY s.id, s.barcode_id, s.name, s.class
            ORDER BY s.name
        """
        return Database.execute_query(query, (start_date, end_date))


# Initialize database pool when module is imported
try:
    Database.initialize_pool()
except Exception as e:
    print(f"Warning: Could not initialize database pool: {e}")