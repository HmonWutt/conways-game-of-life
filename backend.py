from flask import Flask,render_template_string,request
from driver import driver
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route("/getAliveCells")
def get_alive_cells():
    driver.execute_query(
    """
    MATCH (c:Cell)
    with c,
    CASE 
    WHEN count{(c)-[:NEIGHBOUR]->(q{alive:TRUE})}=2 AND c.alive=TRUE THEN TRUE
    WHEN count{(c)-[:NEIGHBOUR]->(q{alive:TRUE})} = 3 THEN TRUE
    ELSE FALSE
    END as life
    SET c.alive = life
    """,
        database_="neo4j",
    )
    records = driver.execute_query(
    """MATCH (d{alive:TRUE})   
    RETURN collect(distinct d.id) as alive""").records
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
        print("Created {nodes_created} nodes and {rels_created} relationships in {time} ms.".format(
        nodes_created=summary.counters.nodes_created,
        rels_created = summary.counters.relationships_created,
        time=summary.result_available_after
        ))
        return records

@app.route("/reset")
def reset():
    driver.execute_query(
    """
    MATCH (c)
    DETACH DELETE c
    """,
    database_="neo4j")
    return "OK"