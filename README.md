# 🤖 CodeEdu Crew — Multi-Agent AI Platform (Flask Version)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

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




<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-BADGE:END -->
...
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-LIST:END -->


---

## 📬 Contact & Resources

- [CrewAI Docs](https://github.com/joaomdmoura/crewai)
- [GitHub Issues](https://github.com/joaomdmoura/crewai/issues)
- [Join Discord](https://discord.gg/crewai)




## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Try1234567"><img src="https://avatars.githubusercontent.com/u/105978749?v=4?s=100" width="100px;" alt="Try1234567"/><br /><sub><b>Try1234567</b></sub></a><br /><a href="https://github.com/EskimosNing/codeedu/commits?author=Try1234567" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!