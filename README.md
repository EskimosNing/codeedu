# 🤖 CodeEdu Crew — Multi-Agent AI Platform (Flask Version)

**CodeEdu Crew** is a multi-agent AI system built with [CrewAI](https://github.com/joaomdmoura/crewai), exposed via a Flask backend with a streaming-capable API. It allows AI agents to collaborate on complex tasks such as Python code execution, report writing, research, and education.

---

## 📁 Project Structure

```
├── app.py                   # Flask main API entry point
├── src/
│   ├── codeedu/
│   │   ├── config/
│   │   │   ├── agents.yaml
│   │   │   └── tasks.yaml
│   │   ├── agents_pool.py   # Agent definitions
│   │   └── task.py          # Task definitions
├── output/                  # Output files (e.g., markdown reports)
├── conversations/           # Stored chat histories
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

Make sure you are using Python >=3.10 and <3.13.

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Flask backend

```bash
python app.py
```

By default, it will start on `http://localhost:5000`.

---

## 🔐 Environment Variables

Create a `.env` file or export these before running:

```env
OPENAI_API_KEY=your-api-key
OPENROUTER_API_KEY=your-api-key
BASE_URL=https://api.openai.com/v1
SERPER_API_KEY=optional
```

---

## 🔧 Available API Endpoints

| Endpoint                     | Method | Description                                  |
|-----------------------------|--------|----------------------------------------------|
| `/chat`                     | POST   | Multi-agent reasoning for custom input       |
| `/execute_code_snippet`     | POST   | Upload a Python file and get agent analysis  |
| `/upload_code`              | POST   | Inject a code snippet into session context   |
| `/output/<filename>`        | GET    | Download files produced by agents            |
| `/new_conversation`         | POST   | Start a new session                          |
| `/conversations`            | GET    | List all saved conversations                 |
| `/conversation/<cid>`       | GET    | Get full history of a specific conversation  |
| `/delete_conversation/<cid>`| DELETE | Delete a conversation and its history        |

---

## 🧪 Usage Example (via Postman or Frontend)

### Upload and run a Python script
```
POST /execute_code_snippet
Form-Data:
  - file: my_script.py
  - conversation_id: 1234-5678
```

### Ask a question (multi-agent planning)
```json
POST /chat
{
  "conversation_id": "1234-5678",
  "message": "Can you explain how binary search works with Python code?"
}
```

---

## 🧠 Agent Configuration Sample

```yaml
educator:
  role: "AI Educator"
  goal: "Explain technical concepts clearly with code examples"
  backstory: "You are a brilliant teacher known for simplifying complex ideas."
```

---



## 📌 Feature Board

| Feature                           | Status     |
|----------------------------------|------------|
| ✅ Flask API with streaming      | Completed ✅ |
| ✅ File upload + code execution  | Completed ✅ |
| ✅ Agent auto-assignment         | Completed ✅ |
| ✅ LLM summarization of thought  | Completed ✅ |
| 🔄 LangGraph integration         | In Progress |
| 🔲 Frontend log visualization    | Coming Soon |

---

## 📦 Output & Downloads

All generated reports, fixed code files, and result documents are saved in the `/output` directory and can be downloaded via:

```
GET /output/<filename>
```

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->