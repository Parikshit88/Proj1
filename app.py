from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database connection parameters
DB_HOST = "bl-ocp-prd-enterprisedb-nlb-112d71f98002ac93.elb.ap-south-1.amazonaws.com"
DB_NAME = "modules"
DB_USER = ""
DB_PASS = ""

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/data', methods=['GET'])
def fetch_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nbf.frar_requirement')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convert the data to a list of dictionaries
    data = []
    for row in rows:
        data.append({
            'column1': row[0],
            'column2': row[1],
            # Add more columns as needed
        })
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
