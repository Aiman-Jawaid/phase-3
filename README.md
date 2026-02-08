🚀 Phase III — Todo AI Chatbot (Spec-Driven Full Stack)

An AI-powered Todo Dashboard chatbot built with FastAPI, OpenAI Agents SDK, MCP tools, and Neon PostgreSQL.
Users manage tasks using natural language like:

“Add a task to buy groceries”
“Show pending tasks”
“Mark task 3 complete”

The chatbot converts messages into structured task operations through MCP tools — all while keeping conversation history in the database.

🎯 Objective

Build a stateless AI chatbot backend that:

✅ Manages todos using natural language
✅ Uses OpenAI Agents SDK for reasoning
✅ Uses MCP tools for task operations
✅ Stores conversations in database
✅ Works with frontend UI
✅ Survives server restarts

🧠 Architecture Overview
Frontend (Chat UI)
        │
        ▼
FastAPI Chat Endpoint
        │
        ▼
OpenAI Agent Runner
        │
        ▼
MCP Tools Server
        │
        ▼
Neon PostgreSQL Database

Database stores:

Tasks

Conversations

Chat messages

Server remains stateless — all state lives in DB.

🛠 Technology Stack
Component	Technology
Frontend	Chat UI (Next.js / React)
Backend	FastAPI
AI Logic	OpenAI Agents SDK
Tool Layer	MCP Server
Database	Neon PostgreSQL
ORM	SQLModel
Auth	Better Auth
📂 Project Structure
phase-3/
│
├── backend/
│   ├── main.py
│   ├── agent/
│   ├── mcp_tools/
│   ├── models/
│   ├── database.py
│
├── frontend/
│   ├── chat-ui/
│
├── specs/
│   ├── agent_spec.md
│   ├── mcp_spec.md
│
└── README.md

⚙ Installation & Setup
1️⃣ Clone project
git clone <repo-url>
cd phase-3

2️⃣ Backend Setup

Create virtual environment:

python -m venv venv
venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt

3️⃣ Environment Variables

Create .env file:

OPENAI_API_KEY=your_key
BETTER_AUTH_SECRET=your_secret
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=your_neon_db_url

4️⃣ Run Backend
uvicorn main:app --reload


Backend runs at:

http://localhost:8000

5️⃣ Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs at:

http://localhost:3000

🤖 Chat API Endpoint
Send message to chatbot
POST /api/{user_id}/chat

Request
{
  "conversation_id": 1,
  "message": "Add task to buy milk"
}

Response
{
  "conversation_id": 1,
  "response": "Task added successfully!",
  "tool_calls": [...]
}

🧰 MCP Tools Supported

The AI agent can use:

➕ add_task

Create new todo

📋 list_tasks

View tasks (all/pending/completed)

✅ complete_task

Mark task complete

❌ delete_task

Remove task

✏ update_task

Modify task details

💬 Example Commands

User can say:

✔ “Add task to call mom”
✔ “Show pending tasks”
✔ “Delete task 2”
✔ “What did I complete?”

Agent automatically selects correct MCP tool.

🔄 Stateless Conversation Flow

Receive message

Fetch chat history

Run AI agent

Execute MCP tool

Store messages

Return response

No server memory required.

✅ Features

Natural language task management

Persistent chat history

Tool-based AI reasoning

Database-backed conversations

Frontend integration

Error handling

Stateless backend architecture

🧪 Testing

Test API with:

POSTMAN / Thunder Client


Try commands like:

Add task to buy groceries
Show completed tasks
Mark task 1 done

🚀 Future Improvements

Voice chatbot support

Smart reminders

Multi-user analytics

Task priority AI suggestions

🏁 Deliverables

✔ Working AI chatbot backend
✔ MCP tool integration
✔ Database persistence
✔ Frontend chat UI
✔ Spec-driven architecture

👩‍💻 Author

Built as part of Hackathon Phase III — Spec-Driven Development
