# 🚀 ITSM AI-Powered Workflow Automation

A **Generative AI-powered ITSM automation system** that allows users to request IT support tasks (e.g., **password reset, incident creation, BitLocker recovery**) using **natural language**. The system **automatically detects the request type, triggers the correct workflow, and executes the automation**.

---

## 📌 How It Works

- **User Prompt:** The user enters an IT request in the terminal (e.g., *“Reset my password”*).
- **Intent Detection:** Azure OpenAI via Semantic Kernel interprets the user's request.
- **Knowledge Base Check:** The system first checks for a relevant solution in the Emirates Knowledge Base using Azure AI Search.
- **Workflow Routing:** If the request matches a known workflow (password resets, incident creation, etc.), it is routed to the appropriate function in `sk_plugins/`.
- **Clarification:** If the prompt is ambiguous, the system will ask for more details or present choices.
- **Staff ID Verification:** Although a staff ID check is implemented (and will later be replaced with SSO), for now the system assumes the staff ID is already known.
- **Execution and Feedback:** The appropriate function executes the task and returns real-time feedback to the user.

---

## 📌 How It Works

1️⃣ **User enters an IT request** in the UI (e.g., *“Reset my Aviva password”*).  
2️⃣ **Azure OpenAI detects the intent** (e.g., *Password Reset* or *Disk Cleanup*).  
3️⃣ **Semantic Kernel (SK) routes the request** to the correct workflow.  
4️⃣ **Workflow executes the task** (API call or mock response).  
5️⃣ **User receives real-time feedback** in the UI.  

---

## 📌 Project Structure

```
aiops-itsm-sk/
├── app.py                   # Main application entry point (interactive chat)
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (API keys, endpoints)
└── sk_plugins/              # SK-powered workflow plugins
├── ai_search.py         # Azure AI Search integration for knowledge base articles
├── aviva_password_reset.py  # Aviva password reset workflow
├── bitlocker_recovery.py      # BitLocker recovery key retrieval
├── etech_log_pin_reset.py     # Etech Log PIN reset workflow
├── generic_password_reset.py  # Generic password reset workflow
├── incident_creation.py       # IT support incident creation workflow
└── staff_id_verification.py   # Staff ID verification (mocked for now)
```

---

## 📌 Setup Instructions

#### 0. Prerequisites
- Python (3.8+ recommended)
- Git

#### 1. Clone the Repository

```bash
git clone https://your-repo-url
cd aiops-itsm-sk
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Your `.env` File

Create a `.env` file in the root folder and add the following:

```ini

# Azure OpenAI SDK Configuration
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2025-01-01-preview

# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://your-search-resource.search.windows.net
AZURE_SEARCH_INDEX=your-index-name
AZURE_SEARCH_API_KEY=your-search-api-key

# Mock API Configuration (For Testing)
CHECK_GROUP_API=https://your-api-endpoint.com/check_group
```

### 5️⃣ Run the Streamlit UI

```bash
python app.py
```

---

## 📌 SK Features Used

| SK Feature              | How We Use It |
|-------------------------|--------------|
| ✅ **Function Calling** | SK routes user requests to the correct workflow function in sk_plugins/. |
| ✅ **Sequential Execution** | SK ensures multi-step workflows execute in order. |
| ✅ **Asynchronous Execution** | SK handles long-running API requests without blocking. |
| ✅ **Modular Workflow Execution** | Each workflow is implemented as an independent function, making the system scalable. |

---

## Future Enhancements

- Integrate Real ITSM APIs: Replace mock implementations with actual IT support integrations.
- Improve the UI: Consider developing a user-friendly UI (e.g., using Streamlit) for enhanced interaction.
- SSO Integration: Replace the current staff ID verification with SSO to automatically verify user credentials.


```
