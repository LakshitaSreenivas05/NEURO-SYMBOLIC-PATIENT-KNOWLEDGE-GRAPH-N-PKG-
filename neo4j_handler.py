import os
import json
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class KnowledgeGraphManager:
    def __init__(self):
        print("Step 1: Connecting to Neo4j...")
        try:
            # We are ignoring os.getenv and forcing the credentials you used in test_neo4j.py
            self.driver = GraphDatabase.driver(
                "bolt://localhost:7687",
                auth=("neo4j", "password")
            )
            self.driver.verify_connectivity()
            print("✅ Neo4j connected successfully!")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            self.driver = None
    def close(self):
        if self.driver:
            self.driver.close()
            print("→ Neo4j connection closed")

    def store_patient(self, patient_data):
        if not self.driver:
            print("❌ Cannot store: No database connection.")
            return

        patient_name = patient_data.get('patient_name', 'Unknown')
        print(f"\n→ Storing patient: {patient_name} in a single transaction...")

        # A single, highly optimized Cypher query using FOREACH to iterate over lists
        query = """
        MERGE (p:Patient {name: $name})
        SET p.age = $age, p.gender = $gender

        // Create Diseases
        FOREACH (disease IN $diseases | 
            MERGE (d:Disease {name: disease})
            MERGE (p)-[:HAS_CONDITION]->(d)
        )
        // Create Medications
        FOREACH (medication IN $medications | 
            MERGE (m:Medication {name: medication})
            MERGE (p)-[:PRESCRIBED]->(m)
        )
        // Create Allergies
        FOREACH (allergy IN $allergies | 
            MERGE (a:Allergy {name: allergy})
            MERGE (p)-[:ALLERGIC_TO]->(a)
        )
        // Create Symptoms
        FOREACH (symptom IN $symptoms | 
            MERGE (s:Symptom {name: symptom})
            MERGE (p)-[:EXHIBITS]->(s)
        )
        // Create Dates
        FOREACH (date IN $important_dates | 
            MERGE (dt:Date {value: date})
            MERGE (p)-[:HAS_APPOINTMENT]->(dt)
        )
        // Create Warnings
        FOREACH (warning IN $warnings | 
            MERGE (w:Warning {text: warning})
            MERGE (p)-[:HAS_WARNING]->(w)
        )
        """

        # We pass the data dictionary, defaulting to empty lists if keys are missing
        parameters = {
            "name": patient_name,
            "age": patient_data.get('age'),
            "gender": patient_data.get('gender'),
            "diseases": patient_data.get('diseases') or [],
            "medications": patient_data.get('medications') or [],
            "allergies": patient_data.get('allergies') or [],
            "symptoms": patient_data.get('symptoms') or [],
            "important_dates": patient_data.get('important_dates') or [],
            "warnings": patient_data.get('warnings') or []
        }

        try:
            with self.driver.session() as session:
                # execute_write is the modern, safe way to handle write transactions in Neo4j
                session.execute_write(lambda tx: tx.run(query, **parameters))
            print(f"✅ Patient {patient_name} fully stored to Knowledge Graph!")
        except Exception as e:
            print(f"❌ Failed to store patient: {e}")

    def get_patient(self, patient_name):
        print(f"\n→ Retrieving patient memory map: {patient_name}...")
        
        query = """
        MATCH (p:Patient {name: $name})
        OPTIONAL MATCH (p)-[:HAS_CONDITION]->(d:Disease)
        OPTIONAL MATCH (p)-[:PRESCRIBED]->(m:Medication)
        OPTIONAL MATCH (p)-[:ALLERGIC_TO]->(a:Allergy)
        OPTIONAL MATCH (p)-[:EXHIBITS]->(s:Symptom)
        OPTIONAL MATCH (p)-[:HAS_APPOINTMENT]->(dt:Date)
        OPTIONAL MATCH (p)-[:HAS_WARNING]->(w:Warning)
        RETURN p, 
               collect(distinct d.name) as diseases,
               collect(distinct m.name) as medications,
               collect(distinct a.name) as allergies,
               collect(distinct s.name) as symptoms,
               collect(distinct dt.value) as dates,
               collect(distinct w.text) as warnings
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, name=patient_name)
                record = result.single()
                
                if record and record['p']:
                    print("✅ Patient found in Knowledge Graph!")
                    return {
                        "patient_name": record['p'].get('name'),
                        "age": record['p'].get('age'),
                        "gender": record['p'].get('gender'),
                        "diseases": record['diseases'],
                        "medications": record['medications'],
                        "allergies": record['allergies'],
                        "symptoms": record['symptoms'],
                        "important_dates": record['dates'],
                        "warnings": record['warnings']
                    }
                else:
                    print("❌ Patient not found")
                    return None
        except Exception as e:
            print(f"❌ Retrieval failed: {e}")
            return None


# ==========================================
# Testing the Fine-Tuned Setup
# ==========================================
if __name__ == "__main__":
    
    # Initialize our new manager class
    kg = KnowledgeGraphManager()
    
    # Sample BioMistral output from Step 1
    sample_patient = {
        "patient_name": "Sarah Chen",
        "age": 34,
        "gender": "female",
        "diseases": ["Type 2 Diabetes"],
        "medications": ["Metformin 500mg twice daily"],
        "allergies": ["Penicillin"],
        "symptoms": ["Frequent thirst", "Fatigue"],
        "important_dates": ["April 2nd 2025"],
        "warnings": ["Low sugar diet advised"]
    }
    
    # 1. Store the patient using the optimized FOREACH query
    kg.store_patient(sample_patient)
    
    # 2. Retrieve the patient memory map to verify
    print("\n=== VERIFYING GRAPH STORAGE ===")
    retrieved = kg.get_patient("Sarah Chen")
    
    if retrieved:
        print(json.dumps(retrieved, indent=2))
    
    # Clean up
    kg.close()