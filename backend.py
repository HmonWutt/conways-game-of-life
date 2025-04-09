from flask import Flask,render_template_string,request
from driver import driver
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route("/getAliveCells")
def get_alive_cells():
    records, summary, keys = driver.execute_query(
    """
    MATCH (c)-[:NEIGHBOUR]->(q{alive:TRUE})
    with c, size(collect(q)) as neighbours
    CALL (*) {
    SET c.alive = 
        CASE 
        WHEN neighbours = 2 AND c.alive=TRUE THEN TRUE
        WHEN neighbours = 3 THEN TRUE
        ELSE FALSE
        END 
    }
    MATCH (d)   
    WHERE d.alive = TRUE
    RETURN collect(distinct d.id) as alive
    """,
        database_="neo4j",
    )
    return records[0].data()['alive']


@app.route("/createNodesAndRelationships",methods=['POST'])
def create_nodes_and_relationships():
    if request.method == 'POST':
        data = request.get_json()
        grid = data.get('grid')
        for each in grid:
            records,summary, keys = driver.execute_query(
            """
            CREATE (c:Cell {id: $id, alive: $alive, neighbours: $neighbours})
            WITH c
            UNWIND split(c.neighbours, ",") AS n
            MATCH (c1:Cell {id: toInteger(n)})
            CREATE (c)-[:NEIGHBOUR]->(c1)-[:NEIGHBOUR]->(c)
            with c,c1
            REMOVE c.neighbours,c1.neighbours
            """,
            id = each['id'],
            alive = each['alive'],
        neighbours = each['neighbours'],
        database_="neo4j"
            )
        return records
