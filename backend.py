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
    CALL (*) {
    SET c.alive = 
        CASE neighbours
        WHEN 2 THEN TRUE
        WHEN 3 THEN TRUE
        ELSE FALSE
        END 
    }
    with c
    MATCH (c)   
    WHERE c.alive = TRUE
    RETURN collect(c.id) as alive
    """,
        database_="neo4j",
    )
    lst = []
    lst+=records
    print("record",records[0].data()['alive'],type(records))

    # for record in records:
    #     #lst+=record.data()['']
    #     print(record.data()['alive'])
    return lst