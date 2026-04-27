import sys
import json
import os

print("===  INITIALIZING N-PKG PIPELINE IMPORTS ===")
try:
    from live_audio import transcribe_live
    from extract_entities import extract_entities
    from structure_with_llm import structure_entities
    from neo4j_handler import KnowledgeGraphManager # <-- New Import!
    from llm_validator import validate # <-- Validator Import
    print(" All modules imported successfully!")
except ImportError as e:
    print(f"\n IMPORT ERROR: {e}")
    sys.exit(1)

def main():
    print("\n" + "="*50)
    print("  N-PKG: CLINICAL AUDIO INGESTION PIPELINE")
    print("="*50)
    
    # --- STEP 1: AUDIO TO TEXT ---
    print("\n[STEP 1] Audio Capture & Whisper Transcription")
    try:
        duration = int(input("Enter seconds to record (recommended 15-20): "))
    except ValueError:
        print("Invalid input. Defaulting to 15 seconds.")
        duration = 15
        
    transcript = transcribe_live(duration=duration)
    
    if not transcript or transcript.strip() == "":
        print(" No transcript generated. Exiting pipeline.")
        return

    # --- STEP 2: NER EXTRACTION ---
    print("\n[STEP 2] Medical Entity Extraction (scispaCy)")
    entities = extract_entities(transcript)
    
    if not entities:
        print(" No entities found. Proceeding to structuring anyway.")
        entities = []

    # --- STEP 3: LLM STRUCTURING ---
    print("\n[STEP 3] JSON Structuring (BioMistral)")
    raw_llm_response = structure_entities(transcript, entities)
    
    if not raw_llm_response:
        print("\n Failed to generate structured data from BioMistral.")
        return

    # --- STEP 4 & 5: PARSE, SAVE, AND PUSH TO KNOWLEDGE GRAPH ---
    print("\n[STEP 4] Parsing Data & Pushing to Neo4j")
    output_filename = "extracted_patient_data.json"
    
    try:
        # Convert string to Python dictionary
        parsed_json = json.loads(raw_llm_response)
        
        # Save physical backup
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(parsed_json, f, indent=4)
        print(f" Local backup saved: {output_filename}")
        
        # ---> Push to Neo4j <---
        print("\n[STEP 5] Integrating into Knowledge Graph...")
        kg = KnowledgeGraphManager()
        kg.store_patient(parsed_json)
        kg.close()
            
        print("\n===  PATIENT SAVED  ===")
        patient_name = parsed_json.get('patient_name', 'Unknown')
        print(f"Patient '{patient_name}' is now stored in the Graph!")
        # --- NEW STEP: DICTATE PRESCRIPTION AND VALIDATE ---
        print("\n" + "="*50)
        print("  [STEP 6] Dictate Prescription & Validate")
        print("="*50)
        
        dictate_rx = input("\nWould you like to dictate a prescription for this patient now? (y/n): ").strip().lower()
        if dictate_rx == 'y':
            try:
                rx_duration = int(input("Enter seconds to record prescription (recommended 10-15): "))
            except ValueError:
                print("Invalid input. Defaulting to 15 seconds.")
                rx_duration = 15
            
            print(f"\n Dictating prescription for {patient_name}...")
            prescription_text = transcribe_live(duration=rx_duration)
            
            if not prescription_text or prescription_text.strip() == "":
                print(" No prescription dictated.")
            else:
                print(f"\n Dictated Prescription: '{prescription_text.strip()}'")
                print(f"\n Validating prescription against {patient_name}'s medical history...")
                
                validation_result = validate(patient_name, prescription_text.strip())
                
                print("\n" + "="*50)
                print("  VALIDATION RESULT ")
                print("="*50)
                print(json.dumps(validation_result, indent=4))
                print("\n===  PIPELINE COMPLETE  ===")
        else:
            print("\n Skipping transcription. Pipeline Complete.")
    except json.JSONDecodeError:
        print("\n  BioMistral did not return perfect JSON. Saving raw output instead.")
        with open("raw_output.txt", "w", encoding="utf-8") as f:
            f.write(raw_llm_response)
        print(" Could not push to Neo4j because the format was invalid.")

if __name__ == "__main__":
    main()