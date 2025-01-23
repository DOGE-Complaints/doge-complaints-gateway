# **DOGEcomplaints System**

## **Project Overview**
DOGEcomplaints is an advanced complaint management system designed to collect, process, and analyze user-submitted complaints. The system ensures structured data handling, legal analysis, and actionable recommendations based on local and international legal frameworks. 

This project includes:
- **Frontend**: A custom GPT interface for collecting complaints.
- **Backend**: A Python Flask server for processing and storing complaints.
- **Database**: Supabase-based structure for managing complaint data.
- **Legal Module**: Automated legal analysis of complaints.
- **Text Vectorization**: Uses a Supabase Edge Function for generating text embeddings.

---

## **Features**
- **Dynamic Complaint Intake**: Accepts complaints in natural language and structures them into JSON format.
- **Validation**: Ensures completeness and correctness of user-submitted data.
- **Geolocation Processing**: Identifies complaint locations using OpenCage and OpenStreetMap APIs.
- **Text Vectorization**: Embeds text data for further classification and analysis via Supabase Edge Function.
- **Legal Analysis**: Matches complaints to national and international laws, providing tailored recommendations.
- **Database Management**: Stores complaints, locations, and categories for analysis and reporting.

---

## **Directory Structure**
├── proces_complaint.py # Main module for processing complaints ├── ai_helper.py # AI-related utilities (e.g., text embeddings) ├── enumerators.py # Enumerations for categories, statuses, and other constants ├── geocoding.py # Handles geolocation using external APIs ├── db.sql # SQL schema for the database ├── complaint-input-demo.json # Example JSON input for testing ├── README.md # Documentation for developers

---

## **Setup Instructions**

### **1. Requirements**
- Python 3.8+
- PostgreSQL (for Supabase integration)
- Supabase Edge Function enabled for text vectorization
- Dependencies listed in `requirements.txt`

### **2. Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/DOGE-Complaints/doge-complaints-gateway.git
   cd DOGEcomplaints

2. Install dependencies:

  ```bash
  pip install -r requirements.txt
```

3. Configure environment variables:

Create a .env file and set the following:

```bash
  OPENCAGE_API_KEY=<open-cage-api-key>
  SUPABASE_URL=<your-supabase-url>
  SUPABASE_KEY=<your-supabase-key>
  SUPABASE_FUNCTION_URL=<url-of-your-supabase-edge-function>
  SUPABASE_JWT_SECRET=<your-supabase-jwt-secret>
```

Replace <url-of-your-supabase-edge-function> with the URL of the deployed function (e.g., https://<your-project-id>.functions.supabase.co The code of this function is located in /supabase/functions/vectorize and is explained further in the document.

Set up the database:

Use db.sql to initialize your database schema.

Start the Flask server:

```bash
python3 run.py
```

## **Text Vectorization with Supabase Edge Function**
### **Edge Function Details**
The system uses a Supabase Edge Function for text vectorization. The function generates embeddings from user-provided text using a pre-trained model. The embeddings are used to classify and analyze complaints efficiently.

### **Edge Function Code**
This is the deployed function code in JavaScript:

```python
import 'jsr:@supabase/functions-js/edge-runtime.d.ts';

const session = new Supabase.ai.Session('gte-small');

Deno.serve(async (req) => {
  const { input } = await req.json();
  const embedding = await session.run(input, {
    mean_pool: true,
    normalize: true,
  });

  return new Response(
    JSON.stringify({ embedding }),
    { headers: { 'Content-Type': 'application/json' } }
  );
});
```

### **Usage in Python**
In ai_helper.py, the vectorization function makes a request to the Edge Function:

```python
def vectorize_text(text: str):
    print(f"Vectorizing text: {text}")
    headers = {
        "Authorization": f"Bearer {get_cached_jwt()}",
        "Content-Type": "application/json",
    }
    payload = {"input": text}
    try:
        response = requests.post(os.getenv('SUPABASE_FUNCTION_URL'), json=payload, headers=headers)
        if response.status_code == 200:
            embeddings = response.json().get("embedding")
            return embeddings
        else:
            print(f"Error: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
```

### **Environment Variable**
**Variable	Description**

SUPABASE_FUNCTION_URL	URL of the deployed Supabase Edge Function
**Usage**
1. Submitting a Complaint
Complaints are submitted to the Flask endpoint /submit-complaint via a POST request. The payload must follow the JSON structure demonstrated in complaint-input-demo.json.

2. Text Vectorization
The system automatically calls the Supabase Edge Function to generate embeddings for complaint descriptions and categories.

### *Testing*
1. Testing Edge Function
Use a tool like curl to send a test request to the Supabase Edge Function:

```bash
curl -X POST "<SUPABASE_FUNCTION_URL>" \
-H "Content-Type: application/json" \
-d '{"input": "Test text for embedding"}'
```

2. Unit Tests
Run tests for the vectorization function and other modules:


# **Contributing**
Fork the repository and create a feature branch.
Follow the coding standards outlined in CONTRIBUTING.md (if available).
Create a pull request with detailed information about your changes.

## **License**
This project is licensed under the MIT License. See LICENSE for details.

## **Support**
For issues, contact the project team at zeya.metsapuu@gmail.com or create an issue in the repository.
