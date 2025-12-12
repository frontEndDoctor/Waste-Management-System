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
        print(f"Retrieved {len(waste_list)} waste types")
        return jsonify({'success': True, 'data': waste_list})
    except Exception as e:
        print(f"Error getting waste: {str(e)}")
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
        print(f"Attempting to delete waste ID: {waste_id}")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if record exists
        cursor.execute("SELECT COUNT(*) FROM Waste WHERE WASTETYPEID = :id", {'id': waste_id})
        count = cursor.fetchone()[0]
        print(f"Found {count} records with ID {waste_id}")
        
        if count == 0:
            return jsonify({'success': False, 'error': f'No waste type found with ID {waste_id}'})
        
        # Perform delete
        cursor.execute(
            "DELETE FROM Waste WHERE WASTETYPEID = :id",
            {'id': waste_id}
        )
        conn.commit()
        rows_affected = cursor.rowcount
        print(f"Deleted {rows_affected} rows")
        
        if rows_affected > 0:
            return jsonify({'success': True, 'message': f'{rows_affected} record(s) deleted'})
        else:
            return jsonify({'success': False, 'error': 'Delete failed - no rows affected'})
    except Exception as e:
        print(f"Error deleting waste: {str(e)}")
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
        print(f"Attempting to delete staff ID: {staff_id}")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if record exists
        cursor.execute("SELECT COUNT(*) FROM Staff WHERE STAFFID = :id", {'id': staff_id})
        count = cursor.fetchone()[0]
        print(f"Found {count} records with ID {staff_id}")
        
        if count == 0:
            return jsonify({'success': False, 'error': f'No staff found with ID {staff_id}'})
        
        # Perform delete
        cursor.execute(
            "DELETE FROM Staff WHERE STAFFID = :id",
            {'id': staff_id}
        )
        conn.commit()
        rows_affected = cursor.rowcount
        print(f"Deleted {rows_affected} rows")
        
        if rows_affected > 0:
            return jsonify({'success': True, 'message': f'{rows_affected} staff member(s) deleted'})
        else:
            return jsonify({'success': False, 'error': 'Delete failed - no rows affected'})
    except Exception as e:
        print(f"Error deleting staff: {str(e)}")
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

@app.route('/api/reports/daily-waste', methods=['GET'])
def get_daily_waste_report():
    """Get total waste per day across all buildings"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COLLECTIONDATE, SUM(COLLECTIONWEIGHT) AS TOTALWASTE
            FROM Collection_Event
            GROUP BY COLLECTIONDATE
            ORDER BY COLLECTIONDATE DESC
        """)
        rows = cursor.fetchall()
        
        report_data = []
        grand_total = 0
        for date, total in rows:
            report_data.append({
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

@app.route('/api/collection-events', methods=['GET'])
def get_collection_events():
    """Get all collection events"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COLLECTIONID, BUILDINGNAME, COLLECTIONDATE, COLLECTIONWEIGHT
            FROM Collection_Event
            ORDER BY COLLECTIONDATE DESC, BUILDINGNAME
        """)
        rows = cursor.fetchall()
        events = [{
            'id': row[0],
            'building': row[1],
            'date': row[2].strftime('%Y-%m-%d') if row[2] else 'N/A',
            'weight': float(row[3]) if row[3] else 0
        } for row in rows]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': events})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/collection-events', methods=['POST'])
def add_collection_event():
    """Add new collection event"""
    conn = None
    cursor = None
    try:
        data = request.json
        collection_id = data.get('collectionId')
        building_name = data.get('buildingName')
        collection_date = data.get('collectionDate')
        collection_weight = data.get('collectionWeight')
        
        print(f"Adding collection event: ID={collection_id}, Building={building_name}, Date={collection_date}, Weight={collection_weight}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Try alternative syntax without TO_DATE if it's causing issues
        cursor.execute("""
            INSERT INTO Collection_Event 
            (COLLECTIONID, BUILDINGNAME, COLLECTIONDATE, COLLECTIONWEIGHT) 
            VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4)
        """, [collection_id, building_name, collection_date, collection_weight])
        
        conn.commit()
        print("Collection event added successfully")
        return jsonify({'success': True, 'message': 'Collection event added successfully'})
    except Exception as e:
        print(f"Error adding collection event: {str(e)}")
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/debug/table-structure', methods=['GET'])
def debug_table_structure():
    """Debug endpoint to see Collection_Event table structure"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT column_name, data_type 
            FROM user_tab_columns 
            WHERE table_name = 'COLLECTION_EVENT'
            ORDER BY column_id
        """)
        rows = cursor.fetchall()
        columns = [{'name': row[0], 'type': row[1]} for row in rows]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'columns': columns})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/collection-events/<int:collection_id>', methods=['DELETE'])
def delete_collection_event(collection_id):
    """Delete collection event"""
    conn = None
    cursor = None
    try:
        print(f"Attempting to delete collection event ID: {collection_id}")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Collection_Event WHERE COLLECTIONID = :id",
            {'id': collection_id}
        )
        conn.commit()
        rows_affected = cursor.rowcount
        print(f"Deleted {rows_affected} rows")
        
        if rows_affected > 0:
            return jsonify({'success': True, 'message': f'{rows_affected} record(s) deleted'})
        else:
            return jsonify({'success': False, 'error': 'No collection event found with that ID'})
    except Exception as e:
        print(f"Error deleting collection event: {str(e)}")
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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