from flask import Flask,render_template_string
from driver import driver
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route("/getAliveCells")
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

createNodes = """
summary = driver.execute_query(
    "CREATE (:Cell {id: $id, alive: $alive, neighbours: $neighbours})
    CALL(){
    MATCH (c) 
    UNWIND split(substring(c.neighbours,1,size(c.neighbours)-2),",") as n
    WITH c,n
    MATCH (c1:CELL{id: toInteger(n)}) 
    CREATE (c)-[:NEIGHBOUR]->(c1)}",
    id = each.id,
    alive = each.alive,
    neighbours = each.neighbours,
    database_="neo4j",
).summary
print("Created {nodes_created} nodes in {time} ms.".format(
    nodes_created=summary.counters.nodes_created,
    time=summary.result_available_after
))
"""

