import json
import re
import sys
from langchain_ollama import OllamaLLM
from neo4j_handler import KnowledgeGraphManager

# ==========================================
# KNOWN ALLERGY DRUG FAMILIES
# ==========================================
ALLERGY_FAMILIES = {
    "penicillin":    ["penicillin", "amoxicillin", "ampicillin", "flucloxacillin",
                      "co-amoxiclav", "piperacillin", "tazobactam"],
    "sulfa":         ["sulfamethoxazole", "trimethoprim", "bactrim", "septra", "sulfadiazine"],
    "aspirin":       ["aspirin", "ibuprofen", "naproxen", "diclofenac", "celecoxib"],
    "codeine":       ["codeine", "morphine", "tramadol", "oxycodone", "fentanyl"],
    "erythromycin":  ["erythromycin", "azithromycin", "clarithromycin"],
    "tetracycline":  ["tetracycline", "doxycycline", "minocycline"],
    "cephalosporin": ["cephalexin", "cefuroxime", "ceftriaxone", "cefadroxil"],
}

# ==========================================
# VERIFIED DRUG CLASSES (For Duplicate Therapy)
# ==========================================
VERIFIED_DRUG_CLASSES = {
    "ACE Inhibitor": ["lisinopril", "enalapril", "ramipril", "benazepril", "captopril"],
    "NSAID":         ["ibuprofen", "naproxen", "diclofenac", "aspirin", "celecoxib"],
    "Beta Blocker":  ["metoprolol", "atenolol", "propranolol", "bisoprolol"],
    "Statin":        ["atorvastatin", "simvastatin", "rosuvastatin", "pravastatin"]
}

# ==========================================
# VERIFIED CONTRAINDICATIONS
# ==========================================
VERIFIED_CONTRAINDICATIONS = {
    "kidney":        ["ibuprofen", "naproxen", "diclofenac", "metformin",
                      "nsaid", "aspirin", "gentamicin", "vancomycin"],
    "liver":         ["metformin", "paracetamol", "acetaminophen", "statins",
                      "isoniazid", "amiodarone", "ketoconazole"],
    "heart failure": ["ibuprofen", "naproxen", "verapamil", "diltiazem",
                      "thiazolidinedione", "pioglitazone"],
    "asthma":        ["aspirin", "ibuprofen", "naproxen", "propranolol",
                      "atenolol", "beta blocker"],
    "epilepsy":      ["tramadol", "bupropion", "clozapine", "mefloquine",
                      "fluoroquinolone", "ciprofloxacin"],
    "copd":          ["propranolol", "atenolol", "metoprolol", "beta blocker"],
    "hypertension":  ["pseudoephedrine", "ephedrine", "decongestant"],
    "pregnancy":     ["warfarin", "lisinopril", "enalapril", "methotrexate",
                      "isotretinoin", "ace inhibitor"],
    "peptic ulcer":  ["ibuprofen", "naproxen", "aspirin", "diclofenac", "nsaid"],
    "gout":          ["aspirin", "furosemide", "hydrochlorothiazide"],
    "diabetes":      ["prednisolone", "prednisone", "dexamethasone", "corticosteroid"],
}

# ==========================================
# STEP 1: FETCH PATIENT HISTORY FROM NEO4J
# ==========================================

def get_patient_context(patient_name):
    print(f"\n-> Fetching patient history from Neo4j: {patient_name}")
    kg = KnowledgeGraphManager()
    patient = kg.get_patient(patient_name)
    kg.close()

    if not patient:
        print(f"  Patient {patient_name} not found in Knowledge Graph")
        return None

    print(f" Patient history retrieved!")
    return patient

# ==========================================
# STEP 2: LLM SCANS THE PRESCRIPTION
# ==========================================

def llm_scan_prescription(patient_context, new_prescription):
    print("\n-> Loading BioMistral...")
    
    #  FIX: Initialize BioMistral INSIDE the function so it doesn't crash Streamlit on boot
    try:
        llm = OllamaLLM(
            model="cniongolo/biomistral",
            temperature=0.0,
            format="json"
        )
    except Exception as e:
        print(f" BioMistral failed to load: {e}")
        return None

    print("-> Sending to BioMistral for clinical reasoning...")

    prompt = f"""<s>[INST]
    You are an expert clinical pharmacist AI.
    Your task is to cross-check the new prescription against patient history for contradictions and allergies. 

    CRITICAL INSTRUCTIONS:
    1. ONLY identify contradictions, drug-drug interactions, or drug-disease contradictions.
    2. DO NOT recommend any alternative medications.
    3. DO NOT suggest different dosages.
    4. Focus ONLY on why the CURRENT prescription might be unsafe.

    --- VERIFIED PATIENT HISTORY ---
    Conditions: {patient_context.get('diseases', [])}
    Allergies: {patient_context.get('allergies', [])}
    Current Medications: {patient_context.get('medications', [])}

    --- NEW PRESCRIPTION ---
    {new_prescription}

    Return ONLY this exact JSON:
    {{
        "verdict": "APPROVED or CONFLICT",
        "severity": "NONE or LOW or HIGH or CRITICAL",
        "conflicts_found": [
            {{
                "type": "CONTRAINDICATION or ALLERGY or DRUG_INTERACTION",
                "drug": "the drug name",
                "condition_or_allergy": "the cause",
                "reason": "clinical explanation"
            }}
        ],
        "reasoning": "Clinical reasoning behind the alerts found"
    }}
    [/INST]</s>"""

    try:
        raw = llm.invoke(prompt)
        print(" BioMistral responded!")
        return raw
    except Exception as e:
        print(f" BioMistral failed: {e}")
        return None

# ==========================================
# STEP 3: PARSE LLM OUTPUT
# ==========================================

def parse_llm_output(raw):
    try:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        print(" No JSON found in LLM response")
        return None
    except Exception as e:
        print(f" JSON parse error: {e}")
        return None

# ==========================================
# STEP 4: NEO4J HARD ALLERGY CHECK
# ==========================================

def neo4j_allergy_check(patient_allergies, prescription_text):
    print("\n-> Running Neo4j hard allergy check...")
    prescription_lower = prescription_text.lower()
    allergy_conflicts  = []

    for allergy in patient_allergies:
        allergy_lower = allergy.lower()

        for family_name, family_drugs in ALLERGY_FAMILIES.items():
            if family_name in allergy_lower or allergy_lower in family_name:
                for drug in family_drugs:
                    if drug in prescription_lower:
                        allergy_conflicts.append({
                            "type":                "ALLERGY",
                            "drug":                drug.title(),
                            "condition_or_allergy": allergy.title(),
                            "reason":              f"Patient is allergic to {allergy.title()}. "
                                                   f"{drug.title()} belongs to the same drug family "
                                                   f"({family_name.title()}) and will trigger an allergic reaction.",
                            "neo4j_verified":      True,
                            "source":              "NEO4J_HARD_CHECK"
                        })
                        print(f"  ALLERGY HARD BLOCK: {allergy} -> {drug} found in prescription!")

    if not allergy_conflicts:
        print("   No allergy conflicts found")

    return allergy_conflicts

# ==========================================
# STEP 4.5: NEO4J DUPLICATE THERAPY CHECK
# ==========================================

def check_duplicate_therapy(patient_meds, prescription_text):
    print("\n-> Running duplicate therapy check...")
    conflicts = []
    prescription_lower = prescription_text.lower()
    
    for med in patient_meds:
        med_lower = med.lower()
        for class_name, drugs in VERIFIED_DRUG_CLASSES.items():
            # If patient is taking a drug in this class
            patient_taking = any(d in med_lower for d in drugs)
            if patient_taking:
                # If prescription contains another drug in this class
                for p_drug in drugs:
                    if p_drug in prescription_lower and p_drug not in med_lower:
                        conflicts.append({
                            "type": "DUPLICATE_THERAPY",
                            "drug": p_drug.title(),
                            "condition_or_allergy": med.title(),
                            "reason": f"Patient is already taking {med.title()} ({class_name}). Adding {p_drug.title()} causes duplicate therapy risk.",
                            "neo4j_verified": True,
                            "source": "NEO4J_HARD_CHECK"
                        })
                        print(f"   DUPLICATE THERAPY: {med} + {p_drug} ({class_name})")
    
    if not conflicts:
        print("  No duplicate therapy conflicts found")
        
    return conflicts

# ==========================================
# STEP 5: CONFIDENCE FILTER
# ==========================================

def confidence_filter(llm_conflicts, patient_conditions, patient_allergies):
    print("\n-> Running confidence filter on LLM conflicts...")

    verified     = []
    hallucinated = []

    conditions_lower = [c.lower() for c in patient_conditions]
    allergies_lower  = [a.lower() for a in patient_allergies]

    for conflict in llm_conflicts:
        drug      = conflict.get("drug", "").lower()
        condition = conflict.get("condition_or_allergy", "").lower()
        ctype     = conflict.get("type", "")

        is_verified = False

        if ctype == "ALLERGY":
            for allergy in allergies_lower:
                if allergy in condition or condition in allergy:
                    is_verified = True
                    break

        elif ctype in ["CONTRAINDICATION", "DRUG_INTERACTION"]:
            for known_condition, known_drugs in VERIFIED_CONTRAINDICATIONS.items():
                patient_has_condition = any(
                    known_condition in pat_cond
                    for pat_cond in conditions_lower
                )
                drug_is_contraindicated = any(
                    known_drug in drug
                    for known_drug in known_drugs
                )

                if patient_has_condition and drug_is_contraindicated:
                    is_verified = True
                    break

        if is_verified:
            conflict["neo4j_verified"] = True
            conflict["source"]         = "LLM_VERIFIED"
            verified.append(conflict)
            print(f"   VERIFIED   : {conflict.get('drug')} — clinically supported")
        else:
            conflict["neo4j_verified"] = False
            conflict["source"]         = "LLM_UNVERIFIED"
            hallucinated.append(conflict)
            print(f"    DOWNGRADED : {conflict.get('drug')} — not in verified facts (possible hallucination)")

    return verified, hallucinated

# ==========================================
# MASTER VALIDATION FUNCTION
# ==========================================

def validate(patient_data_or_name, new_prescription):
    if isinstance(patient_data_or_name, dict):
        patient_context = patient_data_or_name
        patient_name = patient_context.get("patient_name", "Unknown")
    else:
        patient_name = patient_data_or_name
        patient_context = get_patient_context(patient_name)
        
    if not patient_context:
        return {
            "verdict": "ERROR",
            "message": f"Patient {patient_name} not found. Store patient first."
        }

    conditions  = patient_context.get("diseases",    [])
    allergies   = patient_context.get("allergies",   [])

    raw_response = llm_scan_prescription(patient_context, new_prescription)
    if not raw_response:
        return {"verdict": "ERROR", "message": "BioMistral failed to respond."}

    llm_result = parse_llm_output(raw_response)
    if not llm_result:
        return {"verdict": "ERROR", "message": "Could not parse BioMistral response."}

    llm_conflicts = llm_result.get("conflicts_found", [])
    hard_allergy_conflicts = neo4j_allergy_check(allergies, new_prescription)
    duplicate_therapy_conflicts = check_duplicate_therapy(patient_context.get("medications", []), new_prescription)
    
    verified_conflicts, hallucinated_conflicts = confidence_filter(
        llm_conflicts, conditions, allergies
    )

    # Combine all verified hard facts
    all_real_conflicts = hard_allergy_conflicts + verified_conflicts + duplicate_therapy_conflicts

    if all_real_conflicts:
        has_critical = any(c.get("type") == "ALLERGY" for c in all_real_conflicts)
        has_high = any(c.get("type") == "CONTRAINDICATION" for c in all_real_conflicts)
        has_duplicate = any(c.get("type") == "DUPLICATE_THERAPY" for c in all_real_conflicts)
        
        if has_critical:
            final_verdict  = "CONFLICT"
            final_severity = "CRITICAL"
        elif has_high:
            final_verdict  = "CONFLICT"
            final_severity = "HIGH"
        elif has_duplicate:
            final_verdict  = "REVIEW"
            final_severity = "MODERATE"
        else:
            final_verdict  = "CONFLICT"
            final_severity = "HIGH"
            
        verification   = "NEO4J_CONFIRMED"

    elif hallucinated_conflicts:
        # If the LLM flagged something but we can't verify it in the graph,
        # we mark it as APPROVED but still pass the hallucinated conflicts
        # so the UI can display them as "Informational/Unverified Flags".
        final_verdict  = "APPROVED"
        final_severity = "NONE"
        verification   = "NEEDS_HUMAN_REVIEW"

    else:
        final_verdict  = "APPROVED"
        final_severity = "NONE"
        verification   = "FULLY_APPROVED"

    output = {
        "patient":             patient_name,
        "prescription":        new_prescription,
        "verdict":             final_verdict,
        "severity":            final_severity,
        "confirmed_conflicts": all_real_conflicts,
        "unverified_flags":    hallucinated_conflicts,
        "reasoning":           llm_result.get("reasoning", ""),
        "verification_status": verification,
        "verified_by":         "BioMistral 7B + Neo4j Knowledge Graph"
    }

    return output
