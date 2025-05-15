# 🧠 AI Assistant API

This project is a modular Python application that provides an AI-powered assistant service using FastAPI. The project is structured according to SOLID principles and emphasizes extensibility. Queries from the user are processed, an appropriate model is selected, and a formatted prompt is used to generate a response.

You can get answers to your data questions. Make requests to your backend URLs with Token (you can make the necessary adjustments from the data section of the project). You can also get answers to your instruction-based questions.

## 📁 Folder and File Structure

```bash
app/
├── __init__.py
├── main.py # Entry point of the application
├── requirements.txt # List of required dependencies
├── api/
│ ├── __init__.py
│ └── routes.py # FastAPI route definitions

├── core/
│ ├── __init__.py
│ ├── ai_models.py # AI model implementations
│ ├── config.py # Configuration settings
│ ├── interfaces.py # Definition of AI model interfaces
│ └── memory.py # Assistant's temporary memory (context)

├── data/
│ ├── __init__.py
│ ├── data_creator.py # Data creation operations
│ ├── data_provider.py # Data provisioning, loading, and preprocessing
│ └── dataframe_builder.py # JSON to DataFrame conversions

├── schemas/
│ ├── __init__.py
│ └── query.py # Pydantic schemas for API requests

├── services/
│ ├── __init__.py
│ ├── ai_service.py # High-level AI business logic
│ ├── model_factory.py # Model creation and management
│ ├── ollama_client.py # Communication with Ollama API
│ └── query_handler.py # Service managing user queries

├── utils/
│ ├── __init__.py
│ ├── compact_data_handler.py # Compresses long/data-heavy content
│ ├── ollama_utils.py # Ollama service status and helper functions
│ └── prompt_formatter.py # Prompt formatting operations
```

## 🚀 Getting Started

1. Decide for the model to use in the project and continue

#### &emsp;2. 🚀 Using Ollama

&emsp;&emsp;2.1. For <code>Ollama</code>, visit [Ollama Download Page](https://ollama.com/download) and download

&emsp;&emsp;2.2.  After downloading Ollama, run these commands:

     ```bash
     ollama pull gemma3
     ollama run gemma3
     ```

&emsp;&emsp;2.3. From the config file, change <code>USING_MODEL</code> variable to "gemma3"

&emsp;&emsp;2.4. Find your localhost Ollama URL and change <code>OLLAMA_URL</code> variable 

#### &emsp;2. 🚀 Using Gemini, ChatGPT or Another Model

&emsp;&emsp;2.1. Get your API key for the model that is using

&emsp;&emsp;2.2. Depending on the model connected, get your key from [Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key) or [ChatGPT API Key](https://platform.openai.com/api-keys) (or create a new model and get its API key)

&emsp;&emsp;2.3. Change API_KEY variable from the config file

3. Install the required packages:
   
   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   uvicorn main:app --reload
   ```
   
5. Connect the uvicorn URL with Swagger UI (generally it is like that: http://0.0.0.0:xxxx/docs)

6. Submit your questions and get answers with the token.

## 📌 About the Layers

   ```bash
   api/: Contains FastAPI route definitions.
   core/: Houses AI models, interfaces, configuration, and memory components.
   data/: Modules for data creation, processing, and analysis.
   schemas/: Pydantic data schemas for API requests.
   services/: Includes assistant service logic, model management, and external service connections.
   utils/: Helper tools like prompt formatting, data compression, and service checks.
   ```

## 🎯 Purpose

This project is developed to establish an easily extendable and customizable AI assistant infrastructure. It can work with various models, generate data-supported responses, and provide user-centric performance.

## 📦 License

This project is licensed under the [GNU General Public License v3.0 (GPL-3.0)](LICENSE). Contributions are welcome under these terms.
