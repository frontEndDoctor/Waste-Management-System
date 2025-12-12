from flask import Flask, render_template, request, jsonify
import oracledb
from datetime import datetime

app = Flask(__name__)

# Database connection configuration
DB_CONFIG = {
    'user': 'oobadoni',
    'password': 'oobadoni',
    'dsn': 'oracle.umflint.edu:1521/csep'
}

def get_db_connection():
    """Create and return a database connection"""
    return oracledb.connect(**DB_CONFIG)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/waste', methods=['GET'])
def get_waste():
    """Get all waste types"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT WASTETYPEID, WASTENAME FROM Waste ORDER BY WASTETYPEID")
        rows = cursor.fetchall()
        waste_list = [{'id': row[0], 'name': row[1]} for row in rows]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': waste_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/waste', methods=['POST'])
def add_waste():
    """Add new waste type"""
    conn = None
    cursor = None
    try:
        data = request.json
        waste_id = data.get('wasteTypeID')
        waste_name = data.get('wasteName')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Waste (WASTETYPEID, WASTENAME) VALUES (:id, :name)",
            {'id': waste_id, 'name': waste_name}
        )
        conn.commit()
        return jsonify({'success': True, 'message': 'Waste type added successfully'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/waste/<int:waste_id>', methods=['DELETE'])
def delete_waste(waste_id):
    """Delete waste type"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Waste WHERE WASTETYPEID = :id",
            {'id': waste_id}
        )
        rows_affected = cursor.rowcount
        conn.commit()
        
        if rows_affected > 0:
            return jsonify({'success': True, 'message': f'{rows_affected} record(s) deleted'})
        else:
            return jsonify({'success': False, 'error': 'No record found with that ID'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/staff', methods=['GET'])
def get_staff():
    """Get all staff members"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT STAFFID, STAFFNAME FROM Staff ORDER BY STAFFID")
        rows = cursor.fetchall()
        staff_list = [{'id': row[0], 'name': row[1]} for row in rows]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': staff_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/staff/<int:staff_id>', methods=['PUT'])
def update_staff(staff_id):
    """Update staff member"""
    conn = None
    cursor = None
    try:
        data = request.json
        staff_name = data.get('staffName')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Staff SET STAFFNAME = :name WHERE STAFFID = :id",
            {'name': staff_name, 'id': staff_id}
        )
        rows_affected = cursor.rowcount
        conn.commit()
        
        if rows_affected > 0:
            return jsonify({'success': True, 'message': 'Staff updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'No staff found with that ID'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    """Delete staff member"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Staff WHERE STAFFID = :id",
            {'id': staff_id}
        )
        rows_affected = cursor.rowcount
        conn.commit()
        
        if rows_affected > 0:
            return jsonify({'success': True, 'message': f'{rows_affected} staff member(s) deleted'})
        else:
            return jsonify({'success': False, 'error': 'No staff found with that ID'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/reports/building-waste', methods=['GET'])
def get_building_waste_report():
    """Get total waste per building per day"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT BUILDINGNAME, COLLECTIONDATE, SUM(COLLECTIONWEIGHT) AS TOTALWASTE
            FROM Collection_Event
            GROUP BY BUILDINGNAME, COLLECTIONDATE
            ORDER BY COLLECTIONDATE DESC, BUILDINGNAME
        """)
        rows = cursor.fetchall()
        
        report_data = []
        grand_total = 0
        for building, date, total in rows:
            report_data.append({
                'building': building,
                'date': date.strftime('%Y-%m-%d') if date else 'N/A',
                'total': float(total) if total else 0
            })
            grand_total += float(total) if total else 0
        
        cursor.close()
        conn.close()
        return jsonify({
            'success': True, 
            'data': report_data,
            'grandTotal': grand_total
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# @app.route('/api/departments', methods=['GET'])
# def get_departments():
#     """Get all departments"""
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT DEPARTMENTID, DEPARTMENTNAME, PROGRAM, SUPERVISORNAME FROM Department ORDER BY DEPARTMENTID")
#         rows = cursor.fetchall()
#         dept_list = [{'id': row[0], 'name': row[1], 'program': row[2], 'supervisor': row[3]} for row in rows]
#         cursor.close()
#         conn.close()
#         return jsonify({'success': True, 'data': dept_list})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)