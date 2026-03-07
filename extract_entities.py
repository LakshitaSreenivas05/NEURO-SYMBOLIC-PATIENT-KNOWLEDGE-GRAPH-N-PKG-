import spacy

print("Loading scispaCy model...")
nlp = spacy.load("en_core_sci_sm")
print("✅ scispaCy ready!")

def extract_entities(text):
    print("\n→ Extracting medical entities...")
    
    # Process the text
    doc = nlp(text)
    
    # Extract all entities
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })
    
    # Print what was found
    if entities:
        print(f"✅ Found {len(entities)} medical entities:")
        for ent in entities:
            print(f"  → {ent['text']} ({ent['label']})")
    else:
        print("⚠️ No entities found")
    
    return entities
