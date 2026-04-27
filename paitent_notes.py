patient_notes = [
    {
        "id": "P001",
        "name": "John Matthews",
        "age": 58,
        "note": """Patient John Matthews, 58M, presents with chronic kidney disease stage 3 
        and hypertension. Current medications include Lisinopril 10mg daily. 
        Patient reports mild fatigue. Blood pressure 145/90. 
        Next appointment scheduled for March 15, 2025. 
        Avoid NSAIDs including Ibuprofen due to kidney condition."""
    },
    {
        "id": "P002",
        "name": "Sarah Chen",
        "age": 34,
        "note": """Patient Sarah Chen, 34F, diagnosed with Type 2 Diabetes. 
        Prescribed Metformin 500mg twice daily with meals. 
        HbA1c level 7.8. Patient allergic to Penicillin. 
        Follow-up blood test required on April 2, 2025. 
        Advised low sugar diet and 30 minutes daily exercise."""
    },
    {
        "id": "P003",
        "name": "Robert Singh",
        "age": 72,
        "note": """Patient Robert Singh, 72M, presents with heart failure and atrial fibrillation. 
        On Warfarin 5mg daily for blood thinning. 
        Recent chest X-ray shows mild fluid retention. 
        Echocardiogram scheduled for March 20, 2025. 
        Avoid Aspirin due to bleeding risk with Warfarin."""
    },
    {
        "id": "P004",
        "name": "Emily Johnson",
        "age": 29,
        "note": """Patient Emily Johnson, 29F, presents with asthma and seasonal allergies. 
        Prescribed Salbutamol inhaler as needed and Cetirizine 10mg daily. 
        Allergy to Sulfa drugs noted. 
        Lung function test scheduled April 10, 2025. 
        Advised to avoid dust and pollen exposure."""
    },
    {
        "id": "P005",
        "name": "Michael Torres",
        "age": 45,
        "note": """Patient Michael Torres, 45M, newly diagnosed with Type 2 Diabetes and 
        hypertension. Prescribed Metformin 1000mg daily and Amlodipine 5mg daily. 
        Fasting glucose 180mg/dL. 
        Follow-up appointment March 28, 2025. 
        Referred to nutritionist for dietary counseling."""
    },
    {
        "id": "P006",
        "name": "Linda Patel",
        "age": 61,
        "note": """Patient Linda Patel, 61F, presents with osteoporosis and hypothyroidism. 
        On Levothyroxine 50mcg daily and Calcium supplements. 
        Recent bone density scan shows T-score of -2.8. 
        DEXA scan follow-up scheduled May 1, 2025. 
        Avoid taking Calcium within 4 hours of Levothyroxine."""
    },
    {
        "id": "P007",
        "name": "James Wilson",
        "age": 53,
        "note": """Patient James Wilson, 53M, presents with GERD and anxiety disorder. 
        Prescribed Omeprazole 20mg before breakfast and Sertraline 50mg daily. 
        Patient reports difficulty sleeping. 
        Psychiatry review scheduled April 5, 2025. 
        Advised to avoid caffeine and spicy foods."""
    },
    {
        "id": "P008",
        "name": "Priya Sharma",
        "age": 38,
        "note": """Patient Priya Sharma, 38F, 8 weeks pregnant, presents with gestational 
        hypertension. Prescribed Methyldopa 250mg twice daily. 
        Blood pressure 150/95. 
        Obstetric ultrasound scheduled March 25, 2025. 
        Avoid ACE inhibitors and ARBs during pregnancy."""
    },
    {
        "id": "P009",
        "name": "David Kim",
        "age": 67,
        "note": """Patient David Kim, 67M, presents with Parkinson's disease and depression. 
        On Levodopa 100mg three times daily and Escitalopram 10mg. 
        Patient reports increased tremors in the morning. 
        Neurology follow-up April 15, 2025. 
        Avoid Metoclopramide as it worsens Parkinson's symptoms."""
    },
    {
        "id": "P010",
        "name": "Maria Garcia",
        "age": 44,
        "note": """Patient Maria Garcia, 44F, presents with rheumatoid arthritis and 
        chronic kidney disease stage 2. 
        Prescribed Hydroxychloroquine 400mg daily. 
        Avoid high-dose NSAIDs due to kidney involvement. 
        Eye examination required every 6 months due to Hydroxychloroquine. 
        Next rheumatology appointment April 20, 2025."""
    },
    {
        "id": "P011",
        "name": "Thomas Brown",
        "age": 71,
        "note": """Patient Thomas Brown, 71M, presents with COPD and cardiovascular disease. 
        On Tiotropium inhaler daily and Atorvastatin 40mg at night. 
        Oxygen saturation 94%. 
        Pulmonary function test scheduled March 30, 2025. 
        Advised smoking cessation and pulmonary rehabilitation."""
    },
    {
        "id": "P012",
        "name": "Anjali Mehta",
        "age": 26,
        "note": """Patient Anjali Mehta, 26F, presents with epilepsy. 
        Prescribed Sodium Valproate 500mg twice daily. 
        Last seizure 3 months ago. 
        EEG scheduled April 8, 2025. 
        Avoid alcohol completely. 
        Patient counseled about contraception as Valproate affects fetal development."""
    },
    {
        "id": "P013",
        "name": "George Adams",
        "age": 55,
        "note": """Patient George Adams, 55M, presents with gout and hypertension. 
        Prescribed Allopurinol 300mg daily and Losartan 50mg daily. 
        Uric acid level 8.5 mg/dL. 
        Follow-up blood test April 12, 2025. 
        Advised to avoid red meat, shellfish, and alcohol."""
    },
    {
        "id": "P014",
        "name": "Susan Lee",
        "age": 49,
        "note": """Patient Susan Lee, 49F, presents with bipolar disorder and obesity. 
        On Lithium 400mg twice daily. 
        Lithium level 0.7 mEq/L within therapeutic range. 
        Thyroid and kidney function test required every 6 months. 
        Next psychiatry appointment May 10, 2025. 
        Advised to maintain adequate fluid intake."""
    },
    {
        "id": "P015",
        "name": "Raj Nair",
        "age": 63,
        "note": """Patient Raj Nair, 63M, presents with liver cirrhosis and Type 2 Diabetes. 
        On Insulin Glargine 20 units at bedtime. 
        Avoid Metformin due to liver disease risk of lactic acidosis. 
        Liver function test scheduled April 18, 2025. 
        Ultrasound abdomen every 6 months for liver monitoring."""
    },
    {
        "id": "P016",
        "name": "Fiona Gallagher",
        "age": 42,
        "note": """Patient Fiona Gallagher, 42F, presents with systemic lupus erythematosus (SLE) and migraine. 
        Prescribed Hydroxychloroquine 200mg daily and Sumatriptan as needed. 
        Reports photosensitivity. 
        Next rheumatology check-up May 15, 2025. 
        Avoid prolonged sun exposure and use high-SPF sunscreen."""
    },
    {
        "id": "P017",
        "name": "Kevin Zhang",
        "age": 65,
        "note": """Patient Kevin Zhang, 65M, diagnosed with Benign Prostatic Hyperplasia (BPH) and hypertension. 
        Prescribed Tamsulosin 0.4mg daily and Lisinopril 20mg. 
        PSA level 2.1 ng/mL. 
        Urology follow-up scheduled June 10, 2025. 
        Caution with over-the-counter decongestants as they may worsen BPH symptoms."""
    },
    {
        "id": "P018",
        "name": "Olivia Smith",
        "age": 31,
        "note": """Patient Olivia Smith, 31F, presents with Crohn's disease. 
        Currently on Adalimumab injections every two weeks. 
        Recent colonoscopy shows mild inflammation in the terminal ileum. 
        Blood work scheduled for April 22, 2025. 
        Avoid live vaccines while on biologic therapy."""
    },
    {
        "id": "P019",
        "name": "Ahmed Hassan",
        "age": 59,
        "note": """Patient Ahmed Hassan, 59M, presents with chronic obstructive pulmonary disease (COPD) and insomnia. 
        Prescribed Fluticasone/Salmeterol inhaler and Zolpidem 5mg as needed. 
        Oxygen saturation 92% on room air. 
        Sleep study scheduled for May 12, 2025. 
        Avoid beta-blockers as they can trigger bronchospasm in COPD patients."""
    },
    {
        "id": "P020",
        "name": "Elena Rossi",
        "age": 74,
        "note": """Patient Elena Rossi, 74F, presents with Alzheimer's disease and glaucoma. 
        On Donepezil 10mg at bedtime and Latanoprost eye drops. 
        MMSE score 22/30. 
        Next memory clinic appointment June 5, 2025. 
        Avoid anticholinergic medications as they antagonize the effects of Donepezil."""
    },
    {
        "id": "P021",
        "name": "Samuel Okoro",
        "age": 48,
        "note": """Patient Samuel Okoro, 48M, presents with HIV and hyperlipidemia. 
        On antiretroviral therapy (Biktarvy) and Atorvastatin 20mg. 
        Viral load undetectable. CD4 count 650. 
        Blood test for lipid profile April 30, 2025. 
        Avoid St. John's Wort as it significantly reduces antiretroviral efficacy."""
    },
    {
        "id": "P022",
        "name": "Isabella Dubois",
        "age": 37,
        "note": """Patient Isabella Dubois, 37F, presents with polycystic ovary syndrome (PCOS) and depression. 
        Prescribed Metformin 850mg twice daily and Fluoxetine 20mg. 
        Reports irregular menstrual cycles. 
        Endocrinology follow-up May 20, 2025. 
        Advised weight management and low-glycemic index diet."""
    },
    {
        "id": "P023",
        "name": "Victor Kravitz",
        "age": 80,
        "note": """Patient Victor Kravitz, 80M, presents with chronic heart failure and stage 4 chronic kidney disease. 
        Prescribed Furosemide 40mg daily and Carvedilol 6.25mg twice daily. 
        Ejection fraction 35%. 
        Kidney function monitoring April 14, 2025. 
        Avoid potassium-sparing diuretics due to high risk of hyperkalemia."""
    },
    {
        "id": "P024",
        "name": "Chloe Thompson",
        "age": 24,
        "note": """Patient Chloe Thompson, 24F, presents with Anorexia Nervosa and bradycardia. 
        Heart rate 45 bpm. 
        Referred to inpatient eating disorder program. 
        EKG scheduled for March 28, 2025. 
        Avoid strenuous physical activity due to cardiac risk."""
    },
    {
        "id": "P025",
        "name": "Marcus Aurelius",
        "age": 56,
        "note": """Patient Marcus Aurelius, 56M, presents with Psoriatic Arthritis. 
        Prescribed Methotrexate 15mg once weekly and Folic Acid 1mg daily. 
        Reports morning stiffness lasting 1 hour. 
        Liver function tests required every 2 months. 
        Avoid alcohol consumption entirely while taking Methotrexate due to hepatotoxicity."""
    },
    {
        "id": "P026",
        "name": "Sarah Jenkins",
        "age": 41,
        "note": """Patient Sarah Jenkins, 41F, presents with hyperthyroidism (Graves' disease). 
        Prescribed Methimazole 10mg daily. 
        Reports palpitations and heat intolerance. 
        Thyroid function test (TSH, Free T4) scheduled for May 12, 2025. 
        Avoid excessive iodine intake, including seaweed and certain cough syrups."""
    },
    {
        "id": "P027",
        "name": "Liam O'Connor",
        "age": 68,
        "note": """Patient Liam O'Connor, 68M, post-operative Day 4 following total hip replacement. 
        Prescribed Rivaroxaban 10mg daily for DVT prophylaxis and Oxycodone for pain. 
        Physical therapy session scheduled daily. 
        Follow-up with orthopedics on April 18, 2025. 
        Monitor for signs of bleeding or unusual bruising while on anticoagulants."""
    },
    {
        "id": "P028",
        "name": "Yuki Tanaka",
        "age": 22,
        "note": """Patient Yuki Tanaka, 22F, presents with generalized anxiety disorder and insomnia. 
        Prescribed Venlafaxine 75mg daily. 
        Reports increased heart rate. 
        Psychotherapy session scheduled for March 30, 2025. 
        Avoid St. John's Wort due to the risk of serotonin syndrome."""
    },
    {
        "id": "P029",
        "name": "Robert Miller",
        "age": 54,
        "note": """Patient Robert Miller, 54M, presents with Type 2 Diabetes and Peripheral Neuropathy. 
        Prescribed Metformin 1000mg and Gabapentin 300mg at night. 
        HbA1c level 8.2. 
        Podiatry appointment scheduled for June 2, 2025. 
        Daily foot inspections advised to prevent diabetic ulcers."""
    },
    {
        "id": "P030",
        "name": "Amira Al-Farsi",
        "age": 33,
        "note": """Patient Amira Al-Farsi, 33F, presents with Polycystic Kidney Disease (PKD) and hypertension. 
        Prescribed Telmisartan 40mg daily. 
        Creatinine level 1.4 mg/dL. 
        Renal ultrasound scheduled for May 20, 2025. 
        Avoid high-sodium foods and maintain high fluid intake to manage PKD symptoms."""
    },
    {
        "id": "P031",
        "name": "Daniel Katz",
        "age": 47,
        "note": """Patient Daniel Katz, 47M, presents with Ulcerative Colitis (UC). 
        Currently on Mesalamine 2.4g daily. 
        Reports mild abdominal cramping and frequent stools. 
        CRP levels elevated. Colonoscopy scheduled for June 15, 2025. 
        Avoid NSAIDs like Aspirin and Naproxen as they can trigger UC flares."""
    },
    {
        "id": "P032",
        "name": "Sophia Rossi",
        "age": 79,
        "note": """Patient Sophia Rossi, 79F, presents with Osteoarthritis and Atrial Fibrillation. 
        Prescribed Apixaban 5mg twice daily and Celecoxib 100mg as needed. 
        Reports knee pain. 
        Cardiology follow-up scheduled for April 25, 2025. 
        Use Celecoxib with caution due to potential interactions with anticoagulants."""
    },
    {
        "id": "P033",
        "name": "Ethan Wright",
        "age": 19,
        "note": """Patient Ethan Wright, 19M, presents with Type 1 Diabetes and Celiac Disease. 
        On Insulin Lispro and Insulin Glargine. 
        HbA1c level 7.1. 
        Nutritionist consultation for gluten-free management on May 5, 2025. 
        Strict gluten-free diet required to prevent intestinal damage and malabsorption."""
    },
    {
        "id": "P034",
        "name": "Grace Nguyen",
        "age": 62,
        "note": """Patient Grace Nguyen, 62F, presents with Glaucoma and Angina. 
        Prescribed Timolol eye drops and Isosorbide Mononitrate. 
        Intraocular pressure is 18 mmHg. 
        Ophthalmology review scheduled for June 12, 2025. 
        Avoid Sildenafil or similar medications while on nitrates due to severe hypotension risk."""
    },
    {
        "id": "P035",
        "name": "Arthur Pendragon",
        "age": 85,
        "note": """Patient Arthur Pendragon, 85M, presents with Heart Failure (HFrEF) and Gout. 
        On Spironolactone 25mg and Allopurinol 100mg. 
        Potassium level 4.9 mEq/L. 
        Echocardiogram scheduled for April 10, 2025. 
        Monitor potassium levels closely as Spironolactone can lead to hyperkalemia."""
    },
    {
        "id": "P036",
        "name": "Isabella Martinez",
        "age": 28,
        "note": """Patient Isabella Martinez, 28F, presents with Migraine with Aura and requested oral contraceptives. 
        History of frequent visual disturbances before headache onset. 
        Advised to avoid combined oral contraceptives (containing estrogen) due to significantly increased stroke risk in patients with migraine with aura. 
        Progestogen-only options discussed."""
    },
    {
        "id": "P037",
        "name": "Terrence Lewis",
        "age": 66,
        "note": """Patient Terrence Lewis, 66M, presents with Gout and Hypertension. 
        Prescribed Losartan 50mg and Allopurinol 100mg. 
        Avoid Hydrochlorothiazide as diuretics can increase uric acid levels and trigger gout flares. 
        Follow-up uric acid test scheduled for May 15, 2025."""
    },
    {
        "id": "P038",
        "name": "Nora Helmer",
        "age": 52,
        "note": """Patient Nora Helmer, 52F, presents with Rheumatoid Arthritis and Latent Tuberculosis. 
        Planned to start Adalimumab (TNF inhibitor). 
        Must complete at least 1 month of Isoniazid therapy before initiating biologic treatment. 
        Chest X-ray scheduled for April 10, 2025. 
        Monitor liver enzymes monthly."""
    },
    {
        "id": "P039",
        "name": "Victor Hugo",
        "age": 70,
        "note": """Patient Victor Hugo, 70M, presents with Benign Prostatic Hyperplasia (BPH) and Chronic Constipation. 
        Taking Tamsulosin 0.4mg. 
        Avoid Amitriptyline for insomnia as its anticholinergic effects can worsen urinary retention and constipation. 
        Referred to sleep clinic for non-pharmacological interventions."""
    },
    {
        "id": "P040",
        "name": "Clara Barton",
        "age": 45,
        "note": """Patient Clara Barton, 45F, presents with Iron Deficiency Anemia and GERD. 
        Prescribed Ferrous Sulfate and Omeprazole. 
        Advice: Do not take Iron supplements and Omeprazole at the same time; Iron requires an acidic environment for absorption. 
        Space medications by at least 2 hours. Recheck hemoglobin in 4 weeks."""
    },
    {
        "id": "P041",
        "name": "Julian Barnes",
        "age": 63,
        "note": """Patient Julian Barnes, 63M, presents with Heart Failure and Psoriasis. 
        On Carvedilol and Lisinopril. 
        Avoid Propranolol as non-selective beta-blockers can occasionally worsen psoriasis symptoms. 
        Recent BNP levels are stable. Physical exam shows no peripheral edema."""
    },
    {
        "id": "P042",
        "name": "Maya Angelou",
        "age": 82,
        "note": """Patient Maya Angelou, 82F, presents with Osteoporosis and Chronic Pain. 
        On Alendronate weekly. 
        Note: Patient must remain upright for 30 minutes after taking Alendronate to prevent esophageal erosions. 
        Avoid taking with mineral water or juice. 
        Bone density scan scheduled for June 2025."""
    },
    {
        "id": "P043",
        "name": "Silas Marner",
        "age": 58,
        "note": """Patient Silas Marner, 58M, presents with Chronic Kidney Disease Stage 4 and Hyperkalemia. 
        Potassium level 5.6 mEq/L. 
        Strictly avoid Salt Substitutes (which often contain potassium chloride). 
        Discontinue Spironolactone immediately. 
        Dietary review with renal dietitian scheduled for April 5, 2025."""
    },
    {
        "id": "P044",
        "name": "Emma Woodhouse",
        "age": 35,
        "note": """Patient Emma Woodhouse, 35F, presents with Hyperprolactinemia and PCOS. 
        On Cabergoline 0.25mg twice weekly. 
        Pregnancy test required before each dose if menses are delayed. 
        Monitor for symptoms of impulse control disorders, a known side effect of dopamine agonists. 
        Endocrinology follow-up in 3 months."""
    },
    {
        "id": "P045",
        "name": "Heathcliff Earnshaw",
        "age": 49,
        "note": """Patient Heathcliff Earnshaw, 49M, presents with Alcohol Use Disorder and Epilepsy. 
        On Phenytoin 300mg. 
        Note: Acute alcohol intake can increase phenytoin levels, while chronic use can decrease them. 
        Complete abstinence strongly advised. 
        Liver function tests and phenytoin trough levels scheduled for April 12, 2025."""
    },
    {
        "id": "P046",
        "name": "Jane Eyre",
        "age": 27,
        "note": """Patient Jane Eyre, 27F, presents with Acne Vulgaris and is planning pregnancy. 
        Requesting Isotretinoin. 
        Contraindication: Isotretinoin is highly teratogenic. 
        Must use two forms of contraception and have monthly pregnancy tests. 
        Patient opted for topical alternatives until pregnancy plans are deferred."""
    },
    {
        "id": "P047",
        "name": "Winston Smith",
        "age": 60,
        "note": """Patient Winston Smith, 60M, presents with Parkinson’s Disease and Orthostatic Hypotension. 
        Taking Levodopa/Carbidopa. 
        Avoid high-protein meals immediately before dosing as amino acids compete with Levodopa for absorption across the blood-brain barrier. 
        Increase fluid and salt intake for hypotension."""
    },
    {
        "id": "P048",
        "name": "Lisbeth Salander",
        "age": 32,
        "note": """Patient Lisbeth Salander, 32F, presents with Depression and Seasonal Allergies. 
        Taking Sertraline 100mg. 
        Caution with over-the-counter cough medicines containing Dextromethorphan due to the theoretical risk of Serotonin Syndrome. 
        Report any shivering or tremors immediately."""
    },
    {
        "id": "P049",
        "name": "Atticus Finch",
        "age": 55,
        "note": """Patient Atticus Finch, 55M, presents with Glaucoma and Bradycardia. 
        Prescribed Timolol eye drops. 
        Note: Beta-blocker eye drops can be systemically absorbed and worsen bradycardia. 
        Monitor heart rate. 
        Ophthalmology and Cardiology coordination required for long-term management."""
    },
    {
        "id": "P050",
        "name": "Hester Prynne",
        "age": 40,
        "note": """Patient Hester Prynne, 40F, presents with Myasthenia Gravis and Community-Acquired Pneumonia. 
        Avoid Telithromycin and use Fluoroquinolones (like Ciprofloxacin) with extreme caution as they can trigger a myasthenic crisis. 
        Prescribed Amoxicillin as a safer alternative. 
        Monitor respiratory effort closely."""
    }
]