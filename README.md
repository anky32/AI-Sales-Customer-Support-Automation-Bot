#  AI Sales & Customer Support Automation Bot

An AI-powered Sales & Customer Support Automation Platform that helps businesses automate customer interactions, qualify leads, generate sales emails, and manage customer data through a lightweight CRM system.

##  Features

###  AI Customer Support Chatbot

* AI-powered conversational chatbot
* Handles customer inquiries instantly
* Provides business and service information
* Supports natural language interactions

###  Lead Qualification System

* Collects customer information
* Evaluates lead quality based on budget
* Automatically categorizes leads as:

  *  Hot Lead
  *  Warm Lead
  *  Cold Lead

###  AI Email Generator

* Generates professional sales emails
* Creates personalized responses for prospects
* Automates customer communication

###  CRM Dashboard

* Stores customer leads in SQLite database
* Displays lead analytics
* Shows total, hot, warm, and cold leads
* Export leads as CSV

###  CRM Data Storage

* Customer information management
* Lead tracking and monitoring
* Persistent database storage

---

##  Tech Stack

* Python
* Streamlit
* Groq API (LLM)
* SQLite
* Pandas
* Python Dotenv

---

##  Project Structure

```text
AI_Sales_Bot/

├── app.py
├── chatbot.py
├── crm.py
├── database.py
├── email_generator.py
├── faq.py
├── lead_qualifier.py
├── sales_crm.db
├── .env
├── requirements.txt
└── README.md
```

---

##  Installation

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Sales-Bot.git

cd AI-Sales-Bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

### 5. Run Application

```bash
streamlit run app.py
```

---

##  Lead Qualification Logic

| Budget  | Score | Category  |
| ------- | ----- | --------- |
| ≥ $5000 | 90    | Hot Lead  |
| ≥ $2000 | 70    | Warm Lead |
| < $2000 | 40    | Cold Lead |

---

##  Example Workflow

1. Customer interacts with AI Chatbot.
2. Customer submits project requirements.
3. System qualifies the lead automatically.
4. Lead information is stored in CRM database.
5. AI generates a personalized sales email.
6. Sales team reviews leads from CRM Dashboard.

---



##  Future Improvements

* Conversation Memory
* RAG-based FAQ Search
* Vector Database Integration
* Lead Analytics Charts
* PDF Proposal Generation
* Admin Authentication
* Multi-Agent AI Workflow
* WhatsApp Integration
* Email Sending Automation
* Cloud Deployment

---

##  Resume Project Description

Developed an AI-powered Sales & Customer Support Automation platform leveraging Large Language Models (LLMs) for customer interaction, lead qualification, CRM management, and automated sales email generation. Implemented lead scoring, customer data storage, AI-powered communication workflows, and business process automation using Python, Streamlit, SQLite, and Groq API.

---

##  Author

**Arpan Pandey**

GitHub: https://github.com/anky32

Email: [pandeyarpan84@gmail.com](mailto:pandeyarpan84@gmail.com)
