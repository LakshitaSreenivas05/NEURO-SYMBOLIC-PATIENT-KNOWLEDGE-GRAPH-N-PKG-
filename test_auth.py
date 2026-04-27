import sys
from neo4j_handler import KnowledgeGraphManager

def test_auth():
    print("Initializing KnowledgeGraphManager...")
    kg = KnowledgeGraphManager()
    
    if not kg.driver:
        print(" Failed to connect to Neo4j. Check database status.")
        sys.exit(1)
        
    print("\n--- Testing Patient Registration ---")
    success, key_or_err = kg.register_user("patient", "test_patient", "testpass123", "Test Patient")
    if success:
        print(f" Patient registered. Access Key: {key_or_err}")
    else:
        print(f" Patient registration info: {key_or_err} (Might already exist)")

    print("\n--- Testing Doctor Registration ---")
    success, err = kg.register_user("doctor", "test_doctor", "testpass123", "Dr. Test")
    if success:
        print(f" Doctor registered.")
    else:
        print(f" Doctor registration info: {err} (Might already exist)")

    print("\n--- Testing Patient Auth ---")
    user_data, error = kg.authenticate_user("patient", "test_patient", "testpass123")
    if error:
        print(f" Auth Failed: {error}")
    else:
        print(f" Patient Auth Success: {user_data}")

    print("\n--- Testing Doctor Auth ---")
    user_data, error = kg.authenticate_user("doctor", "test_doctor", "testpass123")
    if error:
        print(f" Auth Failed: {error}")
    else:
        print(f" Doctor Auth Success: {user_data}")

    kg.close()

if __name__ == "__main__":
    test_auth()
