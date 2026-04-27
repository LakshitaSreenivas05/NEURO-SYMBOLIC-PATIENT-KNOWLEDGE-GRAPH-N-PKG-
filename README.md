# NEURO-SYMBOLIC PATIENT KNOWLEDGE GRAPH (N-PKG)

## Overview

The **Neuro-Symbolic Patient Knowledge Graph (N-PKG)** is an intelligent medical data extraction and storage system that converts clinical audio notes into a structured knowledge graph. It combines:

- **Audio Transcription** - Converts spoken clinical notes to text using OpenAI Whisper
- **Medical Entity Extraction** - Identifies diseases, medications, and symptoms using scispaCy
- **LLM Structuring** - Organizes extracted data using BioMistral language model
- **Knowledge Graph Storage** - Stores patient information in Neo4j for relationship-based querying

## Features

- **Real-time Audio Capture** - Records patient notes directly from microphone  
- **Medical NER** - Specialized entity recognition for medical terms  
- **Intelligent Structuring** - Uses LLMs to create organized JSON from unstructured text  
- **Graph Database Integration** - Stores and queries patient relationships via Neo4j  
- **Patient-Centric Data Model** - Links patients to diseases, medications, and symptoms  

## Security Features

The N-PKG system is built with patient privacy and data security as core priorities:
- **Patient Data Redaction**: Automatically identifies and redacts sensitive PII (Personally Identifiable Information) before processing notes through LLMs or storing them.
- **Audit Logging**: Every access to patient records by a medical professional is securely logged in the Neo4j database, ensuring a complete and immutable trail of who viewed what and when.
- **Patient Key**: A secure, unique access key assigned to each patient, required for authenticating and accessing their specific medical history and audit logs.

## Project Structure

```text
├── app.py                     # Streamlit application entry point
├── auth.py                    # User authentication
├── doctor_interface.py        # UI for doctors
├── doctor_view.py             # Doctor dashboard logic
├── paitent_interface.py       # UI for patients
├── paitent_notes.py           # Data schemas for notes
├── pipeline.py                # Main orchestration pipeline
├── live_audio.py              # Whisper transcription
├── audio_input.py             # Audio recording utilities
├── extract_entities.py        # scispaCy NER
├── structure_with_llm.py      # BioMistral/Llama3.2 LLM structuring
├── llm_validator.py           # Output validation
├── neo4j_handler.py           # Neo4j database interactions
├── test_auth.py               # Authentication tests
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration
└── extracted_patient_data.json # Sample output data
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

### Setup Ollama (Local LLM)

1. **Download and Install [Ollama](https://ollama.com/download)** for your operating system.
2. **Start the Ollama application**.
3. **Pull the required models**. Open your terminal or command prompt and run:
   ```bash
   ollama pull biomistral
   ollama pull llama3.2
   ```
   *(Note: This will download the models. It may take some time depending on your internet connection.)*
4. **Serve the model**. Ensure the Ollama server is running so the application can communicate with it. You can start the server by running:
   ```bash
   ollama serve
   ```

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
5. **Validation** - Validates the structured output against a predefined schema to ensure accuracy and completeness
6. **Knowledge Graph** - Pushes the validated structured data to Neo4j

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

### Project Files Description

Here is a detailed breakdown of what each file in the project structure does:

- **`app.py`**: The main entry point for the Streamlit application. It handles routing between the doctor and patient interfaces.
- **`auth.py`**: Manages user authentication, including patient key generation, validation, and session state management.
- **`doctor_interface.py`**: The frontend UI where doctors can record audio, process patient notes, and trigger the extraction pipeline.
- **`doctor_view.py`**: A specialized view for doctors to search the knowledge graph, view patient history, and retrieve medical records.
- **`paitent_interface.py`**: The frontend UI for patients. Allows them to log in using their Patient Key and view their medical history and access audit logs.
- **`paitent_notes.py`**: Contains Pydantic data models and schemas used for structuring the extracted medical data.
- **`pipeline.py`**: The core orchestration script that ties together audio recording, transcription, extraction, structuring, validation, and database storage.
- **`live_audio.py`**: Handles real-time audio capture and uses OpenAI's Whisper model to transcribe the speech to text.
- **`audio_input.py`**: Provides utility functions for handling audio input, potentially supporting file uploads or alternative microphone capture methods.
- **`extract_entities.py`**: Uses `scispaCy` to perform Medical Named Entity Recognition (NER) to pull out diseases, medications, and symptoms from the transcribed text.
- **`structure_with_llm.py`**: Interfaces with local LLMs (like BioMistral or Llama3.2) via Ollama/Groq to format the extracted entities and text into a structured JSON payload.
- **`llm_validator.py`**: Validates the LLM-generated JSON to ensure it adheres strictly to the required schema before it gets saved.
- **`neo4j_handler.py`**: Manages all database operations, including creating patient nodes, relating them to medical entities, and writing audit logs for access tracking.
- **`test_auth.py`**: Unit tests for the authentication and key generation functions.
- **`requirements.txt`**: Lists all Python packages and dependencies required to run the project.
- **`.env`**: Stores sensitive environment variables such as Neo4j credentials and API keys.
- **`extracted_patient_data.json`**: A sample output file demonstrating the format of the structured data after a successful pipeline run.
