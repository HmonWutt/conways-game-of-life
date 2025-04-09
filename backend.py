from flask import Flask,render_template_string,request
from driver import driver
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route("/getAliveCells", methods = ['POST'])
def get_alive_cells():
    if request.method == 'POST':
        data = request.get_json()
        limit = data["limit"]
        records, summary, keys = driver.execute_query(
        
        """MATCH (c)-[:NEIGHBOUR]-(q{alive:TRUE})
        WHERE c.id <= $limit
        with c, size(collect(q)) as neighbours
        CALL (*) {
        SET c.alive = 
            CASE neighbours
            WHEN 2 THEN TRUE
            WHEN 3 THEN TRUE
            ELSE FALSE
            END 
        }
        MATCH (d)   
        WHERE d.alive = TRUE
        RETURN collect(d.id) as alive
        """,
            database_="neo4j",
            limit = limit
        )
        return records[0].data()['alive']

@app.route("/killAll")
def kill_all():
     records,summary, keys = driver.execute_query(
        """MATCH (c) 
            FOREACH(cell IN c | SET c.alive = FALSE)""",database_="neo4j")
     return records

@app.route("/createRelationships",methods=['POST'])
def create_relationships():
    if request.method == 'POST':
        data = request.get_json()
        grid = data.get('grid')
        records,summary, keys = driver.execute_query(
                """WITH $grid AS grid
                FOREACH(cell IN grid | CREATE (c:Cell {id: cell.id, alive: cell.alive, neighbours: cell.neighbours}))
                with grid
                MATCH (c)
                UNWIND split(c.neighbours, ",") AS n
                MATCH (c1:Cell {id: toInteger(n)})
                CREATE (c)-[:NEIGHBOUR]->(c1)
                REMOVE c.neighbours
                """, 
                grid = grid,
                database_="neo4j",
                )
        # for each in grid:
        #     records,summary, keys = driver.execute_query(
        #         # """WITH $grid AS grid
        #         # FOREACH(cell IN grid | CREATE (c:Cell {id: cell.id, alive: cell.alive, neighbours: cell.neighbours}))""", 
        #         # grid = grid,
        #         # database_="neo4j",
        #         # ).summary
        #  """
        #     CREATE (c:Cell {id: $id, alive: $alive, neighbours: $neighbours})
        #     WITH c
        #     UNWIND split(c.neighbours, ",") AS n
        #     MATCH (c1:Cell {id: toInteger(n)})
        #     CREATE (c)-[:NEIGHBOUR]->(c1)
        #     REMOVE c.neighbours
        #     """,
        #     id = each['id'],
        #     alive = each['alive'],
        # neighbours = each['neighbours'],
        # database_="neo4j"
        #     )
        return records
    
@app.route("/giveLife",methods=['POST'])
def giveLife():
    if request.method == "POST":
        data= request.get_json()
        alive = data["alive"]
        records, summary, keys = driver.execute_query(
        """WITH $alive AS alive
        FOREACH(cell IN alive| SET cell.alive = TRUE)
        """, database_="neo4j")
        return records

