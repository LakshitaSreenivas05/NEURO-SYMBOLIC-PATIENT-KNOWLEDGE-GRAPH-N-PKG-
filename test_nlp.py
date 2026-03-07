import spacy

nlp = spacy.load("en_core_sci_sm")

sample_note = """Patient John Matthews, 58M, presents with chronic kidney disease 
and hypertension. Current medications include Lisinopril 10mg daily. 
Avoid NSAIDs including Ibuprofen due to kidney condition."""

doc = nlp(sample_note)

print("Medical entities found:")
for ent in doc.ents:
    print(f"  → {ent.text} ({ent.label_})")