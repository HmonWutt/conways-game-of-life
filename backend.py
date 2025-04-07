from flask import Flask,render_template_string
from driver import driver
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route("/")
def hello_world():
    records, summary, keys = driver.execute_query(
    
    """MATCH (c)-[:NEIGHBOUR]->(q{alive:TRUE})
    with c, size(collect(q)) as neighbours
    SET c.alive = 
    CASE neighbours
    WHEN 2 THEN TRUE
    WHEN 3 THEN TRUE
    ELSE FALSE
    END 
    RETURN collect(c.alive) as alive, collect(c.id) as id""",
        database_="neo4j",
    )
    lst = []
    for record in records:
        lst+=record.data()['id']
    print("backend",lst)
    return lst