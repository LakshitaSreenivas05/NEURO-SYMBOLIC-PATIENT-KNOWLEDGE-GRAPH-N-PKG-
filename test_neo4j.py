from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

print("Step 1: Loading environment variables...")
uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")
print(f"  URI: {uri}")
print(f"  User: {user}")
print(f"  Password loaded: {'Yes' if password else 'No'}")

print("Step 2: Connecting to Neo4j...")
driver = GraphDatabase.driver(uri, auth=(user, password))

print("Step 3: Testing connection...")
try:
    with driver.session() as session:
        print("Step 4: Session opened...")
        result = session.run("RETURN 'Connected!' AS message")
        record = result.single()
        print("Step 5: Query ran...")
        
        if record:
            print(f"SUCCESS: {record['message']}")
        else:
            print("Query returned nothing")
            
except Exception as e:
    print(f"ERROR: {e}")

finally:
    driver.close()
    print("Step 6: Connection closed")
