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
        cursor.execute("SELECT STAFFID, STAFFNAME, CURRENTSHIFT, BUILDINGNAME FROM Staff ORDER BY STAFFID")
        rows = cursor.fetchall()
        staff_list = [{'id': row[0], 'name': row[1], 'shift': row[2], 'building': row[3]} for row in rows]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': staff_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/staff', methods=['POST'])
def add_staff():
    """Add new staff member"""
    conn = None
    cursor = None
    try:
        data = request.json
        staff_id = data.get('staffId')
        staff_name = data.get('staffName')
        current_shift = data.get('currentShift')
        building_name = data.get('buildingName')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Staff (STAFFID, STAFFNAME, CURRENTSHIFT, BUILDINGNAME) VALUES (:1, :2, :3, :4)",
            [staff_id, staff_name, current_shift, building_name]
        )
        conn.commit()
        return jsonify({'success': True, 'message': 'Staff added successfully'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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

@app.route('/api/bins', methods=['GET'])
def get_bins():
    """Get all bins"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT BINID, BINLOCATION, BUILDINGNAME, WASTETYPEID FROM Collection_Bin ORDER BY BINID")
        rows = cursor.fetchall()
        bins = [{'id': row[0], 'location': row[1], 'building': row[2], 'wasteTypeId': row[3]} for row in rows]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': bins})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/bins', methods=['POST'])
def add_bin():
    """Add new bin"""
    conn = None
    cursor = None
    try:
        data = request.json
        bin_id = data.get('binId')
        bin_location = data.get('binLocation')
        building_name = data.get('buildingName')
        waste_type_id = data.get('wasteTypeId')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Collection_Bin (BINID, BINLOCATION, BUILDINGNAME, WASTETYPEID) VALUES (:1, :2, :3, :4)",
            [bin_id, bin_location, building_name, waste_type_id]
        )
        conn.commit()
        return jsonify({'success': True, 'message': 'Bin added successfully'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/bins/<int:bin_id>', methods=['DELETE'])
def delete_bin(bin_id):
    """Delete bin"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Collection_Bin WHERE BINID = :id", {'id': bin_id})
        conn.commit()
        rows_affected = cursor.rowcount
        
        if rows_affected > 0:
            return jsonify({'success': True, 'message': f'{rows_affected} bin(s) deleted'})
        else:
            return jsonify({'success': False, 'error': 'No bin found with that ID'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/buildings', methods=['GET'])
def get_buildings():
    """Get all buildings"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT BUILDINGNAME FROM Building ORDER BY BUILDINGNAME")
        rows = cursor.fetchall()
        buildings = [{'name': row[0]} for row in rows]
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'data': buildings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/collection-events', methods=['GET'])
def get_collection_events():
    """Get all collection events"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COLLECTIONID, COLLECTIONDATE, COLLECTIONWEIGHT, BINID, STAFFID, BUILDINGNAME
            FROM Collection_Event
            ORDER BY COLLECTIONDATE DESC, BUILDINGNAME
        """)
        rows = cursor.fetchall()
        events = [{
            'id': row[0],
            'date': row[1].strftime('%Y-%m-%d') if row[1] else 'N/A',
            'weight': float(row[2]) if row[2] else 0,
            'binId': row[3],
            'staffId': row[4],
            'building': row[5]
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
        collection_date = data.get('collectionDate')
        collection_weight = data.get('collectionWeight')
        bin_id = data.get('binId')
        staff_id = data.get('staffId')
        building_name = data.get('buildingName')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO Collection_Event 
            (COLLECTIONID, COLLECTIONDATE, COLLECTIONWEIGHT, BINID, STAFFID, BUILDINGNAME) 
            VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5, :6)
        """
        
        cursor.execute(sql, [collection_id, collection_date, collection_weight, bin_id, staff_id, building_name])
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Collection event added successfully'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/collection-events/<int:collection_id>', methods=['DELETE'])
def delete_collection_event(collection_id):
    """Delete collection event"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Collection_Event WHERE COLLECTIONID = :id",
            {'id': collection_id}
        )
        conn.commit()
        rows_affected = cursor.rowcount
        
        if rows_affected > 0:
            return jsonify({'success': True, 'message': f'{rows_affected} record(s) deleted'})
        else:
            return jsonify({'success': False, 'error': 'No collection event found with that ID'})
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
    # Populate initial data on startup
    print("\n" + "="*60)
    print("INITIALIZING DATABASE WITH SAMPLE DATA")
    print("="*60)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert Staff
        print("\nInserting staff members...")
        staff_data = [
            (17211, 'Alice Johnson', 'Morning', 'Murchie Science Building'),
            (17212, 'Michael Smith', 'Night', 'University Pavilion'),
            (17213, 'Fatima Ali', 'Night', 'Harding Mott University Center'),
            (17214, 'David Kwame', 'Morning', 'Frances Willson Thompson Library'),
            (17215, 'Joyce Mitchual', 'Morning', 'Recreation Center')
        ]
        
        for staff_id, name, shift, building in staff_data:
            try:
                cursor.execute("""
                    INSERT INTO Staff (STAFFID, STAFFNAME, CURRENTSHIFT, BUILDINGNAME)
                    VALUES (:1, :2, :3, :4)
                """, [staff_id, name, shift, building])
                print(f"  ✓ Added: {name} (ID: {staff_id})")
            except oracledb.IntegrityError:
                print(f"  ⚠ Staff {staff_id} already exists, skipping...")
        
        conn.commit()
        
        # Insert Bins
        print("\nInserting collection bins...")
        bin_data = [
            (101, 'Ground Floor Lobby', 'Murchie Science Building', 1),
            (102, 'Second Floor Corridor', 'University Pavilion', 2),
            (201, 'Main Entrance', 'Harding Mott University Center', 2),
            (202, 'Basement', 'Recreation Center', 4)
        ]
        
        for bin_id, location, building, waste_type in bin_data:
            try:
                cursor.execute("""
                    INSERT INTO Collection_Bin (BINID, BINLOCATION, BUILDINGNAME, WASTETYPEID)
                    VALUES (:1, :2, :3, :4)
                """, [bin_id, location, building, waste_type])
                print(f"  ✓ Added: Bin {bin_id} at {location}")
            except oracledb.IntegrityError:
                print(f"  ⚠ Bin {bin_id} already exists, skipping...")
        
        conn.commit()
        
        # Verify data
        cursor.execute("SELECT COUNT(*) FROM Staff")
        staff_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Collection_Bin")
        bin_count = cursor.fetchone()[0]
        
        print(f"\n✓ Database initialized successfully!")
        print(f"  Total Staff: {staff_count}")
        print(f"  Total Bins: {bin_count}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"⚠ Warning: Could not populate initial data: {e}")
        print("  You can still use the app - add data manually through the UI")
    
    print("="*60)
    print("STARTING FLASK SERVER")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)