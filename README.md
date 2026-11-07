# CodePilot — AI Project Analyst Agent

An AI-powered project analyst that helps developers understand, explore, and review their codebases.

CodePilot analyzes registered project folders and provides project explanations, architecture analysis, code reviews, structure analysis, and project reports using an AI-powered workflow.

## Features

- **Project Q&A:** Ask questions about your project and receive context-aware explanations.
- **Architecture Analysis:** Understand the architecture and components of your project.
- **Code Review:** Identify potential bugs, risks, and areas for improvement in your code.
- **Structure Analysis:** Explore your project's folder structure and organization.
- **Project Reports:** Generate reports covering project overview, strengths, weaknesses, technical risks, and recommendations.
- **Multi-Project Support:** Register and switch between multiple local project folders.
- **Interactive Dashboard:** Use a web-based interface to select projects and interact with the AI assistant.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API |
| LangGraph | AI workflow orchestration |
| NVIDIA AI API | Language model integration |
| OpenAI Python SDK | API communication |
| HTML, CSS, JavaScript | Frontend |
| Pydantic | Request validation |

## Project Architecture

```text
CodePilot/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── agent/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── graph.py
│   ├── schemas/
│   │   └── analysis.py
│   ├── services/
│   │   ├── project_scanner.py
│   │   ├── project_context.py
│   │   ├── project_qa.py
│   │   ├── architecture.py
│   │   ├── code_review.py
│   │   ├── review_validator.py
│   │   ├── structure_review.py
│   │   ├── project_report.py
│   │   ├── project_report_validator.py
│   │   ├── project_registry.py
│   │   └── llm.py
│   ├── config.py
│   └── main.py
│
├── Frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── sample_project/
├── another_project/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

CodePilot follows an AI-powered workflow:

1. The user selects a registered project.
2. The project scanner reads supported source files.
3. Project context is prepared for analysis.
4. The request classifier identifies the type of analysis.
5. LangGraph routes the request to the appropriate workflow.
6. The relevant service prepares the prompt and communicates with the NVIDIA AI model.
7. The response is returned to the frontend.

## Installation and Setup

### Prerequisites

- Python 3.11 or later
- Git
- NVIDIA API key

### 1. Clone the repository

```bash
git clone https://github.com/Prithvikalyan/CodePilot.git
cd CodePilot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure your NVIDIA API key and model settings.

```env
NVIDIA_API_KEY=your_nvidia_api_key
NVIDIA_MODEL=nvidia/nemotron-3-ultra-550b-a55b
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
```

Replace the placeholder with your own API key. Never upload your `.env` file or expose your API key publicly.

### 5. Start the backend

From the project root:

```bash
uvicorn app.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the frontend

Open a second terminal from the project root:

```bash
python -m http.server 5500 --directory Frontend
```

Open the dashboard:

```text
http://127.0.0.1:5500
```

Make sure the backend is running before using the frontend.

## Analysis Modes

| Mode | Description |
|---|---|
| Project Q&A | Ask questions about the selected project |
| Architecture Analysis | Understand project architecture |
| Code Review | Review source code for potential issues |
| Structure Analysis | Analyze project organization |
| Project Report | Generate a structured project report |

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/projects` | List registered projects |
| POST | `/projects/add` | Register a local project folder |
| GET | `/scan-project` | Scan a selected project |
| POST | `/analyze` | Run AI project analysis |

Interactive API documentation is available at `/docs`.

## Safety and Limitations

- CodePilot scans registered project folders rather than arbitrary locations.
- Project scanning is read-only.
- CodePilot does not automatically overwrite or modify source code.
- The local folder picker is intended for a locally running backend with desktop access.
- Analysis quality depends on the scanned files and the AI model's responses.
- Unsupported file types, oversized files, and ignored directories are excluded from scanning.

## Project Status

**Version:** V1  
**Status:** Completed

CodePilot V1 focuses on AI-powered project understanding and analysis through a simple web dashboard.

## Author

**Prithvi Kalyan**

GitHub: [@Prithvikalyan](https://github.com/Prithvikalyan)

---

If you find this project useful, consider giving the repository a star!