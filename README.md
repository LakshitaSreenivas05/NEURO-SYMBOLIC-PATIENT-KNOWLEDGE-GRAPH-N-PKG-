# NEURO-SYMBOLIC PATIENT KNOWLEDGE GRAPH (N-PKG)

## Overview

The **Neuro-Symbolic Patient Knowledge Graph (N-PKG)** is an intelligent medical data extraction and storage system that converts clinical audio notes into a structured knowledge graph. It combines:

- **Audio Transcription** - Converts spoken clinical notes to text using OpenAI Whisper
- **Medical Entity Extraction** - Identifies diseases, medications, and symptoms using scispaCy
- **LLM Structuring** - Organizes extracted data using BioMistral language model
- **Knowledge Graph Storage** - Stores patient information in Neo4j for relationship-based querying

## Features

✅ **Real-time Audio Capture** - Records patient notes directly from microphone  
✅ **Medical NER** - Specialized entity recognition for medical terms  
✅ **Intelligent Structuring** - Uses LLMs to create organized JSON from unstructured text  
✅ **Graph Database Integration** - Stores and queries patient relationships via Neo4j  
✅ **Patient-Centric Data Model** - Links patients to diseases, medications, and symptoms  

## Project Structure

```
├── pipeline.py                 # Main orchestration pipeline
├── live_audio.py              # Audio capture and transcription (Whisper)
├── extract_entities.py        # Medical entity extraction (scispaCy)
├── structure_with_llm.py      # LLM-based data structuring (BioMistral)
├── neo4j_handler.py           # Knowledge graph management
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration (Neo4j credentials)
├── extracted_patient_data.json # Sample output data
└── documentation/             # Project documentation and planning
```

## Installation

### Prerequisites
- Python 3.9+
- Neo4j Database (local or cloud instance)
- Microphone for audio input

### Setup Neo4j (Local)

1. **Download and Install [Neo4j Desktop](https://neo4j.com/download/)**.
2. **Create a New Project** and click **Add -> Local DBMS**.
3. Set the password for your database (make note of it for the `.env` file).
4. **Start the DBMS**. Ensure the Bolt port is `7687`.

### Application Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/LakshitaSreenivas05/NEURO-SYMBOLIC-PATIENT-KNOWLEDGE-GRAPH-N-PKG-.git
   cd "NEURO-SYMBOLIC-PATIENT-KNOWLEDGE-GRAPH-N-PKG-"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On macOS/Linux: source venv/bin/activate
   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   Create a `.env` file in the root directory with your Neo4j credentials:
   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password
   ```

5. **Download spaCy models**
   ```bash
   python -m spacy download en_core_sci_md
   ```

## Usage

### Run the Web Interface (Streamlit)

The main entry point for doctors and patients is the Streamlit web application.

```bash
streamlit run app.py
```

This will launch a local server and open the interface in your web browser (typically at `http://localhost:8501`).

### Run the Command-line Pipeline (Optional)

If you wish to test the extraction workflow without the UI:
```bash
python pipeline.py
```

**Pipeline Steps:**

1. **Audio Input** - Records for specified duration (recommended 15-20 seconds)
2. **Transcription** - Converts audio to text using Whisper
3. **Entity Extraction** - Identifies medical entities (diseases, medications, symptoms)
4. **Structuring** - Organizes data into JSON format via LLM
5. **Knowledge Graph** - Pushes structured data to Neo4j

### Example Output

```json
{
  "patient_name": "John Doe",
  "age": 65,
  "gender": "Male",
  "diseases": ["Hypertension", "Type 2 Diabetes"],
  "medications": ["Metformin", "Lisinopril"],
  "symptoms": ["Fatigue", "Increased Thirst"]
}
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `langchain` | LLM orchestration framework |
| `langchain-groq` | Groq API integration |
| `ollama` | Local LLM support |
| `neo4j` | Graph database driver |
| `spacy` + `scispacy` | Medical entity recognition |
| `openai-whisper` | Audio transcription |
| `python-dotenv` | Environment configuration |
| `streamlit` | Web interface (optional) |
| `pandas` | Data processing |

## Configuration

### Neo4j Connection

Update `.env` with your Neo4j instance details:
- **Local**: `bolt://localhost:7687`
- **Cloud**: Use your Aura connection string

### LLM Models

- **Default**: BioMistral (via Groq/Ollama)
- **Fallback**: OpenAI GPT models

## Data Model

### Entity Relationships in Neo4j

```
Patient
├── HAS_CONDITION → Disease
├── TAKES_MEDICATION → Medication
└── EXHIBITS_SYMPTOM → Symptom
```

## Development

### Testing

Check medical entity extraction:
```bash
python test_nlp.py
```

Test Neo4j connectivity:
```bash
python test_neo4j.py
```

### Project Files

- `audio input.py` - Input audio handling utilities
- `paitent_notes.py` - Patient data models
- `extracted_patient_data.json` - Sample extracted data
