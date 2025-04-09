from flask import Flask,render_template_string,request
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
                # """WITH $grid AS grid
                # FOREACH(cell IN grid | CREATE (c:Cell {id: cell.id, alive: cell.alive, neighbours: cell.neighbours}))""", 
                # grid = grid,
                # database_="neo4j",
                # ).summary
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
        driver
        return records
query = """  WITH c
            Call()
            {
            MATCH (c)
            UNWIND split(substring(c.neighbours,0,size(c.neighbours)),",") as n
            WITH c,n
            MATCH (c1:CELL{id: toInteger(n)}) 
            CREATE (c)-[:NEIGHBOUR]->(c1)}
            WITH c
            REMOVE c.neighbours"""


    #old_create = """
    #                 CREATE (c:Cell {id: $id, alive: $alive, neighbours: $neighbours})
    #                 WITH c
    #                 UNWIND split(substring(c.neighbours,1,size(c.neighbours)-2),",") as n
    #                 CREATE (c)-[:NEIGHBOUR]->(c1{id: toInteger(n)})
    #                 WITH c
    #                 REMOVE c.neighbours
    #                 """,
    #                 id = each['id'],
    #                 alive = each['alive'],
#                 neighbours = ",".join([str(i) for i in each['neighbours']]),
#                 database_="neo4j", 
#   """
# """WITH $grid AS document
# UNWIND grid
# FOREACH(cell IN grid | CREATE (c:Cell {id: cell.id, alive: cell.alive, neighbours: cell.neighbours}))""", grid = grid

kill_revive_cells_query = """MATCH (c)-[:NEIGHBOUR]->(q{alive:TRUE})
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
    RETURN collect(c.id) as alive"""