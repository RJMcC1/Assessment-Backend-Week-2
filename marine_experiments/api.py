"""An API for handling marine experiments."""

from datetime import datetime

from flask import Flask, jsonify, request
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

from database_functions import get_db_connection


app = Flask(__name__)

"""
For testing reasons; please ALWAYS use this connection. 

- Do not make another connection in your code
- Do not close this connection

If you do not understand this instructions; as a coach to explain
"""
conn = get_db_connection("marine_experiments")


@app.get("/")
def home():
    """Returns an informational message."""
    return jsonify({
        "designation": "Project Armada",
        "resource": "JSON-based API",
        "status": "Classified"
    })

@app.route("/experiment", methods = ['GET'])
def experiment_get():
    args = request.args.to_dict()
    type = args.get("type")
    score = args.get("score_over")
    if type:
        type = type.lower()
    valid_types = ["intelligence", "obedience" , "aggression"]
    if type and type not in valid_types:
        return {"error": "Invalid value for 'type' parameter"}, 400

    
    if score is not None:
        try:
            score = int(score)
            if score < 1 or score > 100:
                raise ValueError
        except ValueError:
            return {"error": "Invalid value for 'score_over' parameter"}, 400

    

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('''SELECT 
        e.experiment_id,
        e.subject_id,
        ROUND((e.score / et.max_score) * 100, 2) AS score,
        TO_CHAR(e.experiment_date, 'YYYY-MM-DD') as experiment_date,
        et.type_name AS experiment_type,
        s.species_name AS species
    FROM experiment AS e
    JOIN experiment_type AS et USING (experiment_type_id)
    JOIN subject AS sub USING (subject_id)
    JOIN species AS s USING (species_id)
    ORDER BY experiment_date DESC''')
    results = cursor.fetchall()

    if type:
        results = [e for e in results if e['experiment_type'] == type]

    if score:
        results = [e for e in results if e['score'] > score]

    return jsonify(results), 200


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
