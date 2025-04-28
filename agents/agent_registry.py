# agents/agent_registry.py

# Import all available agents
from agents.chat_agent import ChatAgent
from agents.go_crud_agent import GoCRUDAgent
from agents.go_crud_data_agent import GoCRUDDataAgent
from agents.go_swagger_agent import GoSwaggerAgent
from agents.angularapp_agent import AngularAppAgent
from agents.dalle3_agent import Dalle3Agent
from agents.dalle2_agent import Dalle2Agent
from agents.audio_agent import AudioAgent
from agents.savetofile_agent import SaveToFileAgent
from agents.github.create_branch_agent import GitHubCreateBranchAgent
from agents.github.commit_agent import GitHubCommitAgent
from agents.github.checkout_branch_agent import GitHubCheckoutBranchAgent
from agents.github.pr_agent import GitHubPRAgent
from agents.github.clone_or_update_repo_agent import GitHubCloneOrUpdateRepoAgent
from agents.requirements.py_requirements_extractor_agent import RequirementsExtractorAgent
from agents.rag.database_builder_agent import RAGDatabaseBuilderAgent
from agents.rag.query_agent import RAGQueryAgent
from agents.rag.attach_agent import RAGAttachAgent
from agents.rag.database_updater_agent import RAGDatabaseUpdaterAgent

# ✅ Agent registry for loading agents dynamically
AGENT_REGISTRY = {
    "ChatAgent": ChatAgent,
    "GoCRUDAgent": GoCRUDAgent,
    "GoCRUDDataAgent": GoCRUDDataAgent,
    "GoSwaggerAgent": GoSwaggerAgent,
    "AngularAppAgent": AngularAppAgent,
    "Dalle3Agent": Dalle3Agent,
    "Dalle2Agent": Dalle2Agent,
    "AudioAgent": AudioAgent,
    "SaveToFileAgent": SaveToFileAgent,
    "GitHubCreateBranchAgent": GitHubCreateBranchAgent,
    "GitHubCommitAgent": GitHubCommitAgent,
    "GitHubCheckoutBranchAgent": GitHubCheckoutBranchAgent,
    "GitHubPRAgent": GitHubPRAgent,
    "GitHubCloneOrUpdateRepoAgent": GitHubCloneOrUpdateRepoAgent,
    "RequirementsExtractorAgent": RequirementsExtractorAgent,
    "RAGDatabaseBuilderAgent": RAGDatabaseBuilderAgent,
    "RAGQueryAgent": RAGQueryAgent,
    "RAGAttachAgent": RAGAttachAgent,
    "RAGDatabaseUpdaterAgent": RAGDatabaseUpdaterAgent

}

# ✅ Agent catalog for UI display
AGENT_CATALOG = {
    "ChatAgent": {
        "type": "AI",
        "short_description": "General-purpose conversational AI for brainstorming, Q&A, and idea generation.",
        "detailed_description": [
            "General-purpose conversational AI.",
            "Ideal for brainstorming, answering questions, writing content, or summarization.",
            "Best choice for unstructured tasks or idea generation."
        ],
        "tags": ["AI"]
    },
    "GoCRUDAgent": {
        "type": "AI",
        "short_description": "Full-stack Go CRUD generator (models, data layer, API, routes).",
        "detailed_description": [
            "Full-stack Go CRUD code generator (Model + Data + API + Routes).",
            "Best for quickly scaffolding complete backend services."
        ]
        ,
        "tags": ["AI", "Go"]
    },
    "GoCRUDDataAgent": {
        "type": "AI",
        "short_description": "Generates Go data access (DAO) layer with SQL queries and CRUD operations.",
        "detailed_description": [
            "Generates only the SQL-based data access layer (DAO) for Go.",
            "Implements Create, Read, Update, Delete (CRUD) functions with real SQL."
        ],
        "tags": ["AI", "Go"]
    },
    "GoSwaggerAgent": {
        "type": "AI",
        "short_description": "Generates Swagger/OpenAPI documentation for Go REST APIs.",
        "detailed_description": [
            "Generates Swagger/OpenAPI documentation for Go services.",
            "Useful for API documentation and external integration."
        ],
        "tags": ["AI", "Go", "Swagger"]
    },
    "AngularAppAgent": {
        "type": "AI",
        "short_description": "Scaffolds Angular frontend application features, components, and services.",
        "detailed_description": [
            "Creates Angular frontend application code.",
            "Can scaffold features, components, services, and routing."
        ],
        "tags": ["AI", "Frontend", "Angular"]
    },
    "Dalle3Agent": {
        "type": "AI-Image",
        "short_description": "Generates images from text prompts using OpenAI DALL·E 3.",
        "detailed_description": [
            "Generates high-quality images from text prompts using DALL·E 3.",
            "Ideal for marketing visuals, UI mockups, creative content."
        ],
        "tags": ["AI", "Image"]
    },
    "Dalle2Agent": {
        "type": "AI-Image",
        "short_description": "Generates images from text prompts using OpenAI DALL·E 2.",
        "detailed_description": [
            "Generates high-quality images from text prompts using DALL·E 2.",
            "Ideal for marketing visuals, UI mockups, creative content."
        ],
        "tags": ["AI", "Image"]
    },
    "AudioAgent": {
        "type": "AI-Audio",
        "short_description": "Handles Text-to-Speech (TTS) and Speech-to-Text (STT) audio tasks.",
        "detailed_description": [
            "Handles both:",
            "Text-to-Speech (TTS): Convert text into audio files",
            "Speech-to-Text (STT): Transcribe audio files into text",
            "Useful for voice messages, podcasts, audio UIs."
        ],
        "tags": ["AI", "Audio"]
    },
    "SaveToFileAgent": {
        "type": "Utility",
        "short_description": "Saves output text into files. Useful for logging or exporting results.",
        "detailed_description": [
            "Allows saving generated content, prompts, or outputs into files.",
            "Helpful for logging, exporting, or audit purposes."
        ],
        "tags": ["Utility", "File System"]
    },
    "GitHubCreateBranchAgent": {
        "type": "Git",
        "short_description": "Creates new Git branches locally from workflows.",
        "detailed_description": [
            "Creates a new Git branch locally.",
            "Can be used for feature, hotfix, or release branch creation."
        ],
        "tags": ["GitHub"]
    },
    "GitHubCommitAgent": {
        "type": "Git",
        "short_description": "Creates commits in a local Git repository.",
        "detailed_description": [
            "Creates a commit in a local Git repository.",
            "Supports customizable commit messages."
        ],
        "tags": ["GitHub"]
    },
    "GitHubCheckoutBranchAgent": {
        "type": "Git",
        "short_description": "Checks out Git branches locally, creating them if needed.",
        "detailed_description": [
            "Checks out a Git branch locally.",
            "If the branch doesn't exist, attempts to create and track it from `origin`."
        ],
        "tags": ["GitHub"]
    },
    "GitHubPRAgent": {
        "type": "Git",
        "short_description": "Creates GitHub Pull Requests automatically from workflows.",
        "detailed_description": [
            "Automates creating a Pull Request (PR) on GitHub.",
            "Useful for code review and collaboration workflows."
        ],
        "tags": ["GitHub"]
    },
    "GitHubCloneOrUpdateRepoAgent": {
        "type": "Git",
        "short_description": "Clones or updates GitHub repositories from a URL.",
        "detailed_description": [
            "Clones a GitHub repository if missing or updates it (pull) if already cloned.",
            "Ensures local repositories are always synchronized."
        ],
        "tags": ["GitHub"]
    },
   "RequirementsExtractorAgent": {
        "type": "Utility",
        "short_description": "Extracts Python project dependencies (requirements) from a code repository.",
        "detailed_description": [
            "Scans a Python project and identifies all external libraries used.",
            "Generates a valid `requirements.txt` file automatically.",
            "Useful for preparing projects for deployment or packaging."
            ],
        "tags": ["Utility", "Requirements", "Python"]
    },
    "RAGDatabaseBuilderAgent": {
        "type": "RAG",
        "short_description": "Creates a new vector database by embedding and indexing documents for future retrieval (RAG setup step).",
        "detailed_description": [
            "Embeds documents and stores their vector representations into a database.",
            "Supports the first-time creation of a RAG (Retrieval-Augmented Generation) database.",
            "Essential for enabling fast, semantic document retrieval during inference."
        ],
        "tags": ["RAG", "Database"]
    },

    "RAGQueryAgent": {
        "type": "RAG",
        "short_description": "Queries the RAG vector database to retrieve relevant context documents based on user input.",
        "detailed_description": [
            "Performs similarity search against the RAG database based on a user's query.",
            "Returns top-matching documents to enhance AI responses with factual context.",
            "Optimized for semantic retrieval rather than simple keyword search."
        ],
        "tags": ["RAG", "Retrieval"]
    },

    "RAGAttachAgent": {
        "type": "RAG",
        "short_description": "Attaches document metadata and content to an existing RAG vector database without full rebuild.",
        "detailed_description": [
            "Adds new documents and embeddings to an existing RAG database incrementally.",
            "Avoids the need to rebuild the entire database from scratch.",
            "Useful for continuously updating knowledge bases without downtime."
        ],
        "tags": ["RAG", "Database"]
    },

    "RAGDatabaseUpdaterAgent": {
        "type": "RAG",
        "short_description": "Updates existing entries in a RAG vector database with new or corrected embeddings.",
        "detailed_description": [
            "Replaces or updates outdated document embeddings in an existing database.",
            "Ensures that updated documents reflect the latest content for retrieval.",
            "Maintains database accuracy without full re-ingestion."
        ],
        "tags": ["RAG", "Database"]
    },

}
