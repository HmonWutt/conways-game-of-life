from driver import driver
records, summary, keys = driver.execute_query(
    
"""MATCH (c)-[:NEIGHBOUR]->(q{alive:TRUE})
with c, size(collect(q)) as neighbours
SET c.alive = 
CASE neighbours
  WHEN 2 THEN TRUE
  WHEN 3 THEN TRUE
  ELSE FALSE
END 
RETURN collect({c.alive=TRUE}) as alive, collect(c.id) as id""",
    database_="neo4j",
)

# Loop through results and do something with them
for record in records:
    print(record.data()['id'])  # obtain record as dict

# Summary information
""" print("The query `{query}` returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after
)) """