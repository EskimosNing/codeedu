# 🤖 CodeEdu Crew — Multi-Agent Coding Education AI Platform
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

**CodeEdu Crew** is a multi-agent Coding Education system built with [CrewAI](https://github.com/joaomdmoura/crewai), exposed via a Flask backend with a streaming-capable API. It allows AI agents to collaborate on complex tasks such as Python code execution, report writing, research, and education.

**🧠 What It Can Do**
🧑‍🏫 Explain complex tech topics with code examples

👨‍💻 Analyze, execute, and improve uploaded Python files

📊 Generate summaries and structured reports

🤝 Autonomously assign agents and tasks via planner

📂 Stream logs, thoughts, and outputs to your frontend

---

## 📁 Project Structure

```
src/
└── codeedu/
    ├── main.py                    # Entry Flask App
    ├── config/
    │   ├── agents.yaml
    │   ├── tasks.yaml
    │   └── paths.py
    ├── core/
    │   ├── executor.py
    │   ├── stream.py
    │   ├── registry.py
    │   └── output.py
    ├── routes/
    │   ├── chat.py
    │   ├── upload.py
    │   └── conversation.py
    ├── tools/
    │   ├── custom_tool.py
    ├── utils/
    │   ├── session.py
    │   ├── intention.py
    │   └── log_queues.py
    ├── agent_pool.py
    ├── task.py
    ├── conversations/           # Will be created at runtime
    ├── output/                  # Will be created at runtime
```

---

## 🚀 Getting Started

### Requirements

Python >= 3.10 and < 3.13

Docker (for running .py file or container deployment)

### 1. Install dependencies

```bash
git clone https://github.com/your-org/codeedu.git
cd codeedu/src/codeedu
pip install -r requirements.txt
```

### 2. Run the Flask backend

```bash
python main.py
```

By default, it will start on `http://localhost:5000`.

---

## 🐳 Docker Setup

### ✅ Quick Build & Run

```bash
./build_and_run.sh
```

Then visit: http://localhost:5000

## 🔧 Manual
```bash
docker build -t codeedu-backend .
docker run -d -p 5000:5000 \
  -e PROJECT_ROOT="/app/src/codeedu" \
  --name codeedu-app \
  codeedu-backend
```

## 🔐 Environment Variables

Create a `.env` file or export these before running:

```env
MODEL=your-llm-model                            e.g. openai/gpt-4o-mini
OPENAI_API_KEY=your-api-key
OPENROUTER_API_KEY=your-api-key                 (optional)
BASE_URL=https://api.openai.com/v1              (optional)
SERPER_API_KEY=optional 
PROJECT_ROOT=/home/user/.../codeedu/src/codeedu
STORAGE_PATH=${PROJECT_ROOT}/conversations      (conversation history)
OUTPUT_PATH=${PROJECT_ROOT}/output              (output file)
OTHER_MODEL=other-tool-model                    (optional)
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
|-----------------------------------|------------|
| ✅ MAS coordination              | Completed ✅ |
| ✅ Flask API with streaming      | Completed ✅ |
| ✅ File upload + code execution  | Completed ✅ |
| ✅ Agent auto-assignment         | Completed ✅ |
| ✅ LLM summarization of thought  | Completed ✅ |
| ✅Frontend log visualization     | Completed ✅ |
| 🔄 LangGraph integration         | In Progress |

---

## 📦 Output & Downloads

All generated reports, fixed code files, and result documents are saved in the `/output` directory and can be downloaded via:

```
GET /output/<filename>
```

## 👥 Team Roles & Contributions

| Name                                                                                                     | Role                                      | Description                                                                                                                                                   |
|----------------------------------------------------------------------------------------------------------|-------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  [**Jianing ZHAO**](https://github.com/EskimosNing)                                                  | Backend Architect & AI Agent Designer     | Led the entire backend system architecture and implementation. Designed and built all AI agents, task flows, session management, streaming, and API layers.   |
| [**ACCFOOL**](https://github.com/ACCFOOL)                                                              | Frontend Developer                        | Responsible for designing and implementing the frontend interface, enabling seamless interaction between users and the multi-agent system.                   |
|  [**YIN Jianing**](https://github.com/yinlaetitia)                                                     | Frontend Developer                     | Responsible for designing and implementing the frontend interface, enabling seamless interaction between users and the multi-agent system.                                 |
| [**Try1234567**](https://github.com/Try1234567)                                                       | Co-Designer                  | Contributed in the early stage of the project, helping design agent roles and task planning. Provided conceptual input to the overall architecture direction. |

---

## All Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/EskimosNing"><img src="https://avatars.githubusercontent.com/u/52128671?v=4?s=100" width="100px;" alt="Jianing ZHAO"/><br /><sub><b>Jianing ZHAO</b></sub></a><br /><a href="https://github.com/EskimosNing/codeedu/commits?author=EskimosNing" title="Code">💻</a> <a href="#design-EskimosNing" title="Design">🎨</a> <a href="#projectManagement-EskimosNing" title="Project Management">📆</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ACCFOOL"><img src="https://avatars.githubusercontent.com/u/115349095?v=4?s=100" width="100px;" alt="ACCFOOL"/><br /><sub><b>ACCFOOL</b></sub></a><br /><a href="https://github.com/EskimosNing/codeedu/commits?author=ACCFOOL" title="Code">💻</a> <a href="#design-ACCFOOL" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/yinlaetitia"><img src="https://avatars.githubusercontent.com/u/72556180?v=4?s=100" width="100px;" alt="YIN Jianing"/><br /><sub><b>YIN Jianing</b></sub></a><br /><a href="https://github.com/EskimosNing/codeedu/commits?author=yinlaetitia" title="Code">💻</a> <a href="#design-yinlaetitia" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Try1234567"><img src="https://avatars.githubusercontent.com/u/105978749?v=4?s=100" width="100px;" alt="Try1234567"/><br /><sub><b>Try1234567</b></sub></a><br /><a href="#design-Try1234567" title="Design">🎨</a> <a href="https://github.com/EskimosNing/codeedu/commits?author=Try1234567" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
