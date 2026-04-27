import os
import json
import hashlib
import random
import string
from datetime import datetime
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_access_key(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class KnowledgeGraphManager:
    def __init__(self):
        print("Step 1: Connecting to Neo4j...")
        try:
            uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            user = os.getenv("NEO4J_USER", "neo4j")
            pwd = os.getenv("NEO4J_PASSWORD", "password")
            
            self.driver = GraphDatabase.driver(
                uri,
                auth=(user, pwd)
            )
            self.driver.verify_connectivity()
            print("[OK] Neo4j connected successfully!")
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            self.driver = None
    def close(self):
        if self.driver:
            self.driver.close()
            print("-> Neo4j connection closed")

    def store_patient(self, patient_data):
        if not self.driver:
            print("[ERROR] Cannot store: No database connection.")
            return

        patient_name = patient_data.get('patient_name', 'Unknown')
        patient_username = patient_data.get('patient_username', None)
        print(f"\n-> Storing patient: {patient_name} in a single transaction...")

        # A single, highly optimized Cypher query using FOREACH to iterate over lists
        if patient_username:
            match_clause = "MATCH (p:Patient {username: $username})"
        else:
            match_clause = "MERGE (p:Patient {name: $name})"

        query = f"""
        {match_clause}
        SET p.age = $age, p.gender = $gender

        // Create Diseases
        FOREACH (disease IN $diseases | 
            MERGE (d:Disease {{name: disease}})
            MERGE (p)-[:HAS_CONDITION]->(d)
        )
        // Create Medications
        FOREACH (medication IN $medications | 
            MERGE (m:Medication {{name: medication}})
            MERGE (p)-[:PRESCRIBED]->(m)
        )
        // Create Allergies
        FOREACH (allergy IN $allergies | 
            MERGE (a:Allergy {{name: allergy}})
            MERGE (p)-[:ALLERGIC_TO]->(a)
        )
        // Create Symptoms
        FOREACH (symptom IN $symptoms | 
            MERGE (s:Symptom {{name: symptom}})
            MERGE (p)-[:EXHIBITS]->(s)
        )
        // Create Dates
        FOREACH (date IN $important_dates | 
            MERGE (dt:Date {{value: date}})
            MERGE (p)-[:HAS_APPOINTMENT]->(dt)
        )
        // Create Warnings
        FOREACH (warning IN $warnings | 
            MERGE (w:Warning {{text: warning}})
            MERGE (p)-[:HAS_WARNING]->(w)
        )
        // Create Scheduled Tests
        FOREACH (test IN $scheduled_tests | 
            MERGE (t:Test {{name: test}})
            MERGE (p)-[:HAS_TEST]->(t)
        )
        """

        # We pass the data dictionary, defaulting to empty lists if keys are missing
        parameters = {
            "name": patient_name,
            "username": patient_username,
            "age": patient_data.get('age'),
            "gender": patient_data.get('gender'),
            "diseases": patient_data.get('diseases') or [],
            "medications": patient_data.get('medications') or [],
            "allergies": patient_data.get('allergies') or [],
            "symptoms": patient_data.get('symptoms') or [],
            "important_dates": patient_data.get('important_dates') or [],
            "warnings": patient_data.get('warnings') or [],
            "scheduled_tests": patient_data.get('scheduled_tests') or []
        }

        try:
            with self.driver.session() as session:
                # execute_write is the modern, safe way to handle write transactions in Neo4j
                session.execute_write(lambda tx: tx.run(query, **parameters))
            print(f"[OK] Patient {patient_name} fully stored to Knowledge Graph!")
        except Exception as e:
            print(f"[ERROR] Failed to store patient: {e}")

    def get_patient(self, patient_identifier, by_username=False, accessed_by=None):
        print(f"\n-> Retrieving patient memory map: {patient_identifier}...")
        
        if by_username:
            match_clause = "MATCH (p:Patient {username: $identifier})"
        else:
            match_clause = "MATCH (p:Patient {name: $identifier})"

        query = f"""
        {match_clause}
        OPTIONAL MATCH (p)-[:HAS_CONDITION]->(d:Disease)
        OPTIONAL MATCH (p)-[:PRESCRIBED]->(m:Medication)
        OPTIONAL MATCH (p)-[:ALLERGIC_TO]->(a:Allergy)
        OPTIONAL MATCH (p)-[:EXHIBITS]->(s:Symptom)
        OPTIONAL MATCH (p)-[:HAS_APPOINTMENT]->(dt:Date)
        OPTIONAL MATCH (p)-[:HAS_WARNING]->(w:Warning)
        OPTIONAL MATCH (p)-[:HAS_TEST]->(t:Test)
        RETURN p, 
               collect(distinct d.name) as diseases,
               collect(distinct m.name) as medications,
               collect(distinct a.name) as allergies,
               collect(distinct s.name) as symptoms,
               collect(distinct dt.value) as dates,
               collect(distinct w.text) as warnings,
               collect(distinct t.name) as tests
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, identifier=patient_identifier)
                record = result.single()
                
                if record and record['p']:
                    print("[OK] Patient found in Knowledge Graph!")
                    # Log access if a doctor username was provided
                    if accessed_by:
                        self._log_access(accessed_by, patient_identifier, by_username)
                    return {
                        "patient_name": record['p'].get('name'),
                        "patient_username": record['p'].get('username'),
                        "access_key": record['p'].get('access_key'),
                        "age": record['p'].get('age'),
                        "gender": record['p'].get('gender'),
                        "diseases": record['diseases'],
                        "medications": record['medications'],
                        "allergies": record['allergies'],
                        "symptoms": record['symptoms'],
                        "important_dates": record['dates'],
                        "warnings": record['warnings'],
                        "scheduled_tests": record['tests']
                    }
                else:
                    print("[ERROR] Patient not found")
                    return None
        except Exception as e:
            print(f"[ERROR] Retrieval failed: {e}")
            return None

    def log_event(self, doctor_username, patient_identifier, action, by_username=True):
        """Logs a specific action (e.g., PII_REVEALED) to the audit graph."""
        if by_username:
            match_patient = "MATCH (p:Patient {username: $patient_id})"
        else:
            match_patient = "MATCH (p:Patient {name: $patient_id})"

        query = f"""
        MATCH (d:Doctor {{username: $doctor}})
        {match_patient}
        CREATE (log:AuditLog {{
            action: $action,
            timestamp: datetime(),
            doctor_username: $doctor,
            patient_identifier: $patient_id
        }})
        CREATE (d)-[:PERFORMED]->(log)
        CREATE (log)-[:ACCESSED]->(p)
        """
        try:
            with self.driver.session() as session:
                session.execute_write(lambda tx: tx.run(query, doctor=doctor_username, patient_id=patient_identifier, action=action))
            print(f"[LOG] Audit log: {doctor_username} {action} for {patient_identifier}")
        except Exception as e:
            print(f"[WARN] Audit log failed: {e}")

    def _log_access(self, doctor_username, patient_identifier, by_username=False):
        """Creates an AuditLog node linked to both the Doctor and Patient.
        Fire-and-forget — a failure here does NOT block the clinical workflow."""
        if by_username:
            match_patient = "MATCH (p:Patient {username: $patient_id})"
        else:
            match_patient = "MATCH (p:Patient {name: $patient_id})"

        query = f"""
        MATCH (d:Doctor {{username: $doctor}})
        {match_patient}
        MERGE (d)-[:PERFORMED]->(log:AuditLog {{
            action: 'PATIENT_RECORD_ACCESSED',
            doctor_username: $doctor,
            patient_identifier: $patient_id
        }})
        MERGE (log)-[:ACCESSED]->(p)
        ON CREATE SET 
            log.access_count = 1, 
            log.first_access = datetime(), 
            log.last_access = datetime()
        ON MATCH SET 
            log.access_count = log.access_count + 1, 
            log.last_access = datetime()
        """
        try:
            with self.driver.session() as session:
                session.execute_write(
                    lambda tx: tx.run(query, doctor=doctor_username, patient_id=patient_identifier)
                )
            print(f"[LOG] Audit log: {doctor_username} accessed {patient_identifier}")
        except Exception as e:
            print(f"[WARN] Audit log failed (non-blocking): {e}")

    def register_user(self, role, username, password, name):
        if not self.driver:
            return False, "Database not connected"
            
        hashed_pw = hash_password(password)
        
        try:
            with self.driver.session() as session:
                if role == "doctor":
                    result = session.run("MATCH (u:Doctor {username: $username}) RETURN u", username=username)
                    if result.single():
                        return False, "Username already exists"
                        
                    session.run(
                        "CREATE (d:Doctor {username: $username, password: $password, name: $name})",
                        username=username, password=hashed_pw, name=name
                    )
                    return True, None
                    
                elif role == "patient":
                    result = session.run("MATCH (u:Patient {username: $username}) RETURN u", username=username)
                    if result.single():
                        return False, "Username already exists"
                        
                    access_key = generate_access_key()
                    session.run(
                        "CREATE (p:Patient {username: $username, password: $password, name: $name, access_key: $access_key})",
                        username=username, password=hashed_pw, name=name, access_key=access_key
                    )
                    return True, access_key
        except Exception as e:
            return False, str(e)
            
    def authenticate_user(self, role, username, password):
        if not self.driver:
            return None, "Database not connected"
            
        hashed_pw = hash_password(password)
        try:
            with self.driver.session() as session:
                if role == "doctor":
                    result = session.run(
                        "MATCH (d:Doctor {username: $username, password: $password}) RETURN d.name as name",
                        username=username, password=hashed_pw
                    )
                    record = result.single()
                    if record:
                        return {"role": "doctor", "username": username, "name": record["name"]}, None
                    return None, "Invalid credentials"
                elif role == "patient":
                    result = session.run(
                        "MATCH (p:Patient {username: $username, password: $password}) RETURN p.name as name, p.access_key as access_key",
                        username=username, password=hashed_pw
                    )
                    record = result.single()
                    if record:
                        return {"role": "patient", "username": username, "name": record["name"], "access_key": record["access_key"]}, None
                    return None, "Invalid credentials"
        except Exception as e:
            return None, str(e)

    def link_doctor_patient(self, doctor_username, patient_access_key):
        if not self.driver:
            return False, "Database not connected"
            
        try:
            with self.driver.session() as session:
                result = session.run("MATCH (p:Patient {access_key: $access_key}) RETURN p.username as username, p.name as name", access_key=patient_access_key)
                record = result.single()
                if not record:
                    return False, "Invalid access key or patient not found"
                    
                patient_name = record["name"]
                session.run(
                    """
                    MATCH (d:Doctor {username: $doctor_username})
                    MATCH (p:Patient {access_key: $access_key})
                    MERGE (d)-[:TREATS]->(p)
                    """,
                    doctor_username=doctor_username, access_key=patient_access_key
                )
                return True, f"Successfully linked patient: {patient_name}"
        except Exception as e:
            return False, str(e)

    def get_patients_for_doctor(self, doctor_username):
        if not self.driver:
            return []
            
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (d:Doctor {username: $doctor_username})-[:TREATS]->(p:Patient)
                    RETURN p.username as username, p.name as name ORDER BY p.name
                    """,
                    doctor_username=doctor_username
                )
                return [{"username": record["username"], "name": record["name"]} for record in result]
        except Exception as e:
            print(f"Error fetching treated patients: {e}")
            return []

    def get_patient_audit_logs(self, patient_identifier, by_username=False):
        if not self.driver:
            return []
            
        if by_username:
            match_patient = "MATCH (p:Patient {username: $patient_id})"
        else:
            match_patient = "MATCH (p:Patient {name: $patient_id})"
            
        query = f"""
        {match_patient}
        MATCH (log:AuditLog)-[:ACCESSED]->(p)
        RETURN log.action AS action,
               log.doctor_username AS doctor_username,
               log.timestamp AS timestamp,
               log.first_access AS first_access,
               log.last_access AS last_access,
               log.access_count AS access_count
        ORDER BY coalesce(log.timestamp, log.last_access) DESC
        """
        
        try:
            with self.driver.session() as session:
                result = session.run(query, patient_id=patient_identifier)
                logs = []
                for record in result:
                    logs.append({
                        "action": record["action"],
                        "doctor_username": record["doctor_username"],
                        "timestamp": str(record["timestamp"]) if record["timestamp"] else None,
                        "first_access": str(record["first_access"]) if record["first_access"] else None,
                        "last_access": str(record["last_access"]) if record["last_access"] else None,
                        "access_count": record["access_count"]
                    })
                return logs
        except Exception as e:
            print(f"Error fetching audit logs: {e}")
            return []

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