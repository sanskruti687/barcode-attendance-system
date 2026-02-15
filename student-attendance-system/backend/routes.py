"""
API routes for Student Attendance System
"""
from flask import Blueprint, request, jsonify
from models import Student, Attendance
from datetime import datetime, date

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')


# ==================== STUDENT ROUTES ====================

@api.route('/students', methods=['GET'])
def get_students():
    """Get all students"""
    try:
        students = Student.get_all()
        return jsonify({
            'success': True,
            'data': students
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get student by ID"""
    try:
        student = Student.get_by_id(student_id)
        if student:
            return jsonify({
                'success': True,
                'data': student
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/students/barcode/<barcode_id>', methods=['GET'])
def get_student_by_barcode(barcode_id):
    """Get student by barcode ID"""
    try:
        student = Student.get_by_barcode(barcode_id)
        if student:
            return jsonify({
                'success': True,
                'data': student
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/students', methods=['POST'])
def create_student():
    """Create new student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['barcode_id', 'name', 'class']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        student_id = Student.create(
            data['barcode_id'],
            data['name'],
            data['class'],
            data.get('email'),
            data.get('phone')
        )
        
        return jsonify({
            'success': True,
            'message': 'Student created successfully',
            'student_id': student_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update student information"""
    try:
        data = request.get_json()
        
        # Check if student exists
        student = Student.get_by_id(student_id)
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
        
        Student.update(
            student_id,
            data.get('barcode_id', student['barcode_id']),
            data.get('name', student['name']),
            data.get('class', student['class']),
            data.get('email', student['email']),
            data.get('phone', student['phone'])
        )
        
        return jsonify({
            'success': True,
            'message': 'Student updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete student"""
    try:
        # Check if student exists
        student = Student.get_by_id(student_id)
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
        
        Student.delete(student_id)
        
        return jsonify({
            'success': True,
            'message': 'Student deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/students/search', methods=['GET'])
def search_students():
    """Search students"""
    try:
        keyword = request.args.get('q', '')
        if not keyword:
            return jsonify({
                'success': False,
                'message': 'Search keyword required'
            }), 400
        
        students = Student.search(keyword)
        return jsonify({
            'success': True,
            'data': students
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ==================== ATTENDANCE ROUTES ====================

@api.route('/attendance', methods=['POST'])
def mark_attendance():
    """Mark attendance for a student"""
    try:
        data = request.get_json()
        
        # Validate required field
        if 'barcode_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Barcode ID required'
            }), 400
        
        # Get student by barcode
        student = Student.get_by_barcode(data['barcode_id'])
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
        
        # Mark attendance
        status = data.get('status', 'present')
        attendance_id = Attendance.mark_attendance(student['id'], status)
        
        return jsonify({
            'success': True,
            'message': 'Attendance marked successfully',
            'data': {
                'attendance_id': attendance_id,
                'student': student,
                'status': status
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/attendance/today', methods=['GET'])
def get_today_attendance():
    """Get today's attendance"""
    try:
        attendance = Attendance.get_today_attendance()
        return jsonify({
            'success': True,
            'data': attendance
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/attendance/date/<date_str>', methods=['GET'])
def get_attendance_by_date(date_str):
    """Get attendance for specific date (format: YYYY-MM-DD)"""
    try:
        # Parse date
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        attendance = Attendance.get_by_date(target_date)
        
        return jsonify({
            'success': True,
            'data': attendance
        }), 200
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Invalid date format. Use YYYY-MM-DD'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/attendance/student/<int:student_id>', methods=['GET'])
def get_student_attendance(student_id):
    """Get all attendance records for a student"""
    try:
        # Check if student exists
        student = Student.get_by_id(student_id)
        if not student:
            return jsonify({
                'success': False,
                'message': 'Student not found'
            }), 404
        
        attendance = Attendance.get_by_student(student_id)
        
        return jsonify({
            'success': True,
            'data': {
                'student': student,
                'attendance': attendance
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/attendance/statistics', methods=['GET'])
def get_statistics():
    """Get attendance statistics"""
    try:
        stats = Attendance.get_statistics()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api.route('/attendance/report', methods=['GET'])
def get_report():
    """Get attendance report for date range"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({
                'success': False,
                'message': 'start_date and end_date required (format: YYYY-MM-DD)'
            }), 400
        
        # Parse dates
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if start > end:
            return jsonify({
                'success': False,
                'message': 'start_date must be before end_date'
            }), 400
        
        report = Attendance.get_date_range_report(start, end)
        
        return jsonify({
            'success': True,
            'data': {
                'start_date': start_date,
                'end_date': end_date,
                'report': report
            }
        }), 200
        
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Invalid date format. Use YYYY-MM-DD'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# ==================== HEALTH CHECK ====================

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'API is running',
        'timestamp': datetime.now().isoformat()
    }), 200