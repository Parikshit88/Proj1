from flask import Flask, jsonify
import psycopg2
from psycopg2 import OperationalError
app = Flask(__name__)
# Database connection parameters
DB_HOST = "bl-ocp-prd-enterprisedb-nlb-112d71f98002ac93.elb.ap-south-1.amazonaws.com"
DB_PORT = 9999  # Default PostgreSQL port
DB_NAME = "modules"
DB_USER = "as_parikshitpardeshi"
DB_PASS = "Par!kshit$2024"
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except OperationalError as e:
        print(f"Error: {e}")
        return None
@app.route('/data', methods=['GET'])
def fetch_data():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    cursor.execute('SELECT policy_or_proposal_number, application_number, requirement_code, document_name, modified_by, modified_date, uploaded_status FROM nbf.frar_requirement LIMIT 10')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convert the data to a list of dictionaries
    data = []
    for row in rows:
        data.append({
            'policy_or_proposal_number': row[0],
            'application_number': row[1],
            'requirement_code': row[2],
            'document_name': row[3],
            'modified_by': row[4],
            'modified_date': row[5],
            'uploaded_status': row[6]

        })
    
    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True)
