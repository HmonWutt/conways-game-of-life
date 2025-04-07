from flask import Flask,render_template_string
from driver import driver
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route("/")
def get_alive_cells():
    records, summary, keys = driver.execute_query(
    
    """MATCH (c)-[:NEIGHBOUR]->(q{alive:TRUE})
    with c, size(collect(q)) as neighbours
    CALL (*) {
    SET c.alive = 
        CASE neighbours
        WHEN 2 THEN TRUE
        WHEN 3 THEN TRUE
        ELSE FALSE
        END 
    }
    MATCH (c)   
    WHERE c.alive = TRUE
    RETURN collect(c.id) as alive
    """,
        database_="neo4j",
    )
    return records[0].data()['alive']