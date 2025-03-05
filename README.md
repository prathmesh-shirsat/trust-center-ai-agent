# AI Compliance Document Extraction Agent

## Overview
This AI-powered agent automates the extraction of compliance documents from Trust Center URLs. It navigates websites, identifies relevant documents, and categorizes them as public or private while handling authentication barriers and Cloudflare verification.

## Features
- Extracts compliance documents (SOC2, HIPAA, etc.) from Trust Center URLs.
- Categorizes documents into **public** and **private**.
- Uses **LangChain** with OpenAI for intelligent decision-making.
- Automates browser interactions using **browser-use**.
- Runs asynchronously for efficiency.
- Outputs structured JSON results.
- Containerized with Docker.

## Installation
### Prerequisites
This project requires **Python 3.11 or higher**. If you do not have it installed, follow the steps below:

#### macOS:
1. Install Python via Homebrew:
   ```bash
   brew install python@3.11
   ```
2. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```
3. Verify installation:
   ```bash
   python3 --version
   ```


### 1. Clone the repository
```bash
git clone https://github.com/your-repo/ai-agent.git
cd ai-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory and add necessary credentials, e.g.:
```env
OPENAI_API_KEY=your_openai_api_key
```

### 4. Run the AI agent
```bash
python src/main.py
```

## Input Task Format (`config/tasks.json`)
```json
[
    {
        "organization": {
            "id": "1",
            "name": "Asana",
            "domain": "asana.com",
            "url": "https://asana.com/trust"
        },
        "keywords": ["SOC2", "HIPAA"]
    }
]
```

## Output Format
```json
{
    "status": "success",
    "organization": {
        "id": "",
        "name": "Asana",
        "domain": "asana.com",
        "trust_center_url": "https://asana.com/trust"
    },
    "documents": {
        "public": [
            {
                "id": "doc-12345",
                "title": "Asana SOC 2 Type II Report",
                "type": "SOC2",
                "url": "https://asana.com/trust/documents/soc2.pdf"
            }
        ],
        "private": [
            {
                "id": "doc-67890",
                "title": "Asana HIPAA Compliance Report",
                "type": "HIPAA",
                "url": "https://asana.com/trust/documents/hipaa.pdf"
            }
        ]
    }
}
```

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m 'Added new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License.

