chatbot/
├── contexts/                 ✅ Armazena vetores FAISS por tenant
│
├── core/                     ⚙️ Configurações e utilidades globais
│   ├── config.py             🔧 Carrega dotenv, define paths, etc.
│   └── utils.py              🔧 Funções auxiliares
├── ia/                       🧠 Processamento de IA (LangChain + OpenAI)
│   └── processor.py          💬 Cria/gera respostas com base em contexto
│
├── integrations/            🌐 Integrações com APIs externas
│   └── evolution_api.py      📤 Cliente HTTP da EvolutionAPI
│
├── tenants/                  🏢 Modelos de tenant
│   └── models.py             📋 Dados da empresa, API keys, etc.
│
├── whatsapp/                 💬 Canal de entrada das mensagens
│   ├── webhook.py            🔁 Recebe e processa mensagens (via FastAPI)
│   └── main.py               🚀 Instância da aplicação FastAPI
