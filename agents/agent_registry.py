# agents/agent_registry.py

# Import all available agents
from agents.chat_agent import ChatAgent
from agents.code.go_crud_agent import GoCRUDAgent
from agents.code.go_crud_data_agent import GoCRUDDataAgent
from agents.code.go_swagger_agent import GoSwaggerAgent
from agents.code.angularapp_agent import AngularAppAgent
from agents.images.dalle3_agent import Dalle3Agent
from agents.images.dalle2_agent import Dalle2Agent
from agents.audio.audio_agent import AudioAgent
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
from agents.video.video_assembler_agent import VideoAssemblerAgent
from agents.video.subtitle_generator_agent import SubtitleGeneratorAgent
from agents.audio.audio_segmented_agent import SegmentedAudioAgent
from agents.images.segmented_image_agent import SegmentedImageAgent
from agents.video.segmented_video_assembler_agent import SegmentedVideoAssemblerAgent
from agents.video.segmented_subtitle_generator_agent import SegmentedSubtitleGeneratorAgent
from agents.images.image_agent import ImageAgent
from agents.validators.script_structure_validator_agent import ScriptStructureValidatorAgent
from agents.validators.script_feedback_validator_agent import ScriptFeedbackValidatorAgent
from agents.images.image_analysis_agent import ImageAnalysisAgent
from agents.notify.email_agent import GenericEmailAgent
from agents.notify.webhook_agent import WebhookAgent
from agents.notify.slack_agent import SlackAgent
from agents.utils.camera_capture_agent import CameraCaptureAgent

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
    "RAGDatabaseUpdaterAgent": RAGDatabaseUpdaterAgent,
    "VideoAssemblerAgent": VideoAssemblerAgent,
    "SubtitleGeneratorAgent": SubtitleGeneratorAgent,
    "SegmentedAudioAgent": SegmentedAudioAgent,
    "SegmentedImageAgent": SegmentedImageAgent,
    "SegmentedVideoAssemblerAgent": SegmentedVideoAssemblerAgent,
    "SegmentedSubtitleGeneratorAgent": SegmentedSubtitleGeneratorAgent,
    "ImageAgent": ImageAgent,
    "ScriptStructureValidatorAgent": ScriptStructureValidatorAgent,
    "ScriptFeedbackValidatorAgent": ScriptFeedbackValidatorAgent,
    "ImageAnalysisAgent": ImageAnalysisAgent,
    "GenericEmailAgent": GenericEmailAgent,
    "WebhookAgent": WebhookAgent,
    "SlackAgent": SlackAgent,
    "CameraCaptureAgent": CameraCaptureAgent
}

# ✅ Agent catalog for UI display
AGENT_CATALOG = {
    "OrchestratorAgent": {
        "type": "AI",
        "short_description": "Orchestrator Agent",
        "detailed_description": [
            "Not used"
        ],
        "tags": ["AI", "Orchestration"]
    },
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
        "tags": ["Utility", "File System", "Tool"]
    },
    "GitHubCreateBranchAgent": {
        "type": "Git",
        "short_description": "Creates new Git branches locally from workflows.",
        "detailed_description": [
            "Creates a new Git branch locally.",
            "Can be used for feature, hotfix, or release branch creation."
        ],
        "tags": ["GitHub", "Tool"]
    },
    "GitHubCommitAgent": {
        "type": "Git",
        "short_description": "Creates commits in a local Git repository.",
        "detailed_description": [
            "Creates a commit in a local Git repository.",
            "Supports customizable commit messages."
        ],
        "tags": ["GitHub", "Tool"]
    },
    "GitHubCheckoutBranchAgent": {
        "type": "Git",
        "short_description": "Checks out Git branches locally, creating them if needed.",
        "detailed_description": [
            "Checks out a Git branch locally.",
            "If the branch doesn't exist, attempts to create and track it from `origin`."
        ],
        "tags": ["GitHub", "Tool"]
    },
    "GitHubPRAgent": {
        "type": "Git",
        "short_description": "Creates GitHub Pull Requests automatically from workflows.",
        "detailed_description": [
            "Automates creating a Pull Request (PR) on GitHub.",
            "Useful for code review and collaboration workflows."
        ],
        "tags": ["GitHub", "Tool"]
    },
    "GitHubCloneOrUpdateRepoAgent": {
        "type": "Git",
        "short_description": "Clones or updates GitHub repositories from a URL.",
        "detailed_description": [
            "Clones a GitHub repository if missing or updates it (pull) if already cloned.",
            "Ensures local repositories are always synchronized."
        ],
        "tags": ["GitHub", "Tool"]
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
    "VideoAssemblerAgent": {
        "type": "video",
        "short_description": "Combining a single image and an audio narration into an MP4 video file.",
        "detailed_description": [
            "Takes a background image (image_path) which will serve as the static visual throughout the video.",
            "Takes an audio file (audio_path) which contains the narration or soundtrack.",
            "Combines them into a video of equal duration to the audio file.",
            "Optionally allows setting a custom duration (if shorter than the audio).",
            "Outputs a .mp4 video using standard encoding suitable for platforms like YouTube.",
            " ## Inputs:",
            "image_path (string): Path to the image file to use as video background.",
            "audio_path (string): Path to the audio file to include in the video.",
            "output_video_path (string): Destination file path for the generated video.",
            "duration (optional, float): Duration of the video in seconds (defaults to length of audio).",
            " ## Output:",
            "A dictionary indicating success or error, and the path to the generated video file if successful.",
            " ## Use Case Examples:",
            "Turning a narrated script and a thumbnail image into a publish-ready YouTube video.",
            "Creating static videos from podcast audio and a branded visual.",
            "Auto-generating social media content using AI-generated visuals and voiceovers.",
        ],
        "tags": ["Tool", "Video", "Audio"]
    },
    "SubtitleGeneratorAgent": {
        "type": "Utility",
        "short_description": "Generates .srt subtitles from a script and duration.",
        "detailed_description": [
            "Purpose: Automatically generate .srt subtitle files from a provided script and total video duration.",
            "This agent takes a block of script text (e.g. from a video narration), splits it into timed chunks based on the total video/audio duration, and outputs a valid .srt subtitle file with precise timestamps.",
            "# Each subtitle block includes:",
            " - A sequential number",
            " - Start and end timestamps",
            " - A text chunk (split by character length for readability)",
            " ## Example Use Case",
            " You have a video narration generated from AudioAgent and want to:",
            " Auto-generate matching subtitles",
            "Use those subtitles for accessibility, closed captions, or burning into the video"
        ],
        "tags": ["Tool", "Video", "Subtitle"],
    },
    "SegmentedAudioAgent": {
        "type": "AI-Audio",
        "short_description": "Generates separate audio files from structured script sections.",
        "detailed_description": [
            "This agent is typically used after generating a structured script.",
            "The output dictionary from the script generation step is passed to SegmentedAudioAgent, which then produces individual audio files for each script segment.",
            "These audio files can subsequently be used in video assembly or other multimedia applications."
        ],
        "tags": ["AI", "Audio"]
    },
    "SegmentedImageAgent": {
        "type": "AI-Image",
        "short_description": "Generates separate images for each section based on structured script prompts.",
        "detailed_description": [
            "This agent is typically used after generating a structured script with 'image_prompt' fields.",
            "The output dictionary from the script generation step is passed to SegmentedImageAgent, which uses each prompt to generate one image per section using a model like DALL·E.",
            "These images can be used for video thumbnails, scene illustrations, or any visual storytelling component."
        ],
        "tags": ["AI", "Image", "DALL-E", "Vision"]
    },
    "SegmentedVideoAssemblerAgent": {
        "type": "AI-Video",
        "short_description": "Assembles a complete video by combining per-section audio and images.",
        "detailed_description": [
            "This agent combines audio and image segments, typically generated by SegmentedAudioAgent and SegmentedImageAgent.",
            "For each script section (e.g., intro, scene1, etc.), it overlays the image with its corresponding audio.",
            "It produces short clips for each section and then concatenates them into a single video file.",
            "Ideal for automating YouTube video generation from structured scripts."
        ],
        "tags": ["AI", "Video", "Multimodal", "Assembly", "MoviePy"]
    },
    "SegmentedSubtitleGeneratorAgent": {
        "type": "Utility",
        "short_description": "Generates synchronized subtitle (.srt) files based on structured script and audio segments.",
        "detailed_description": [
            "This agent parses a structured script (YAML or dict) with sectioned text and uses corresponding audio segment durations to generate accurate subtitles.",
            "It outputs a single .srt file with timestamps aligned to the concatenated video timeline.",
            "Typically used alongside SegmentedAudioAgent and SegmentedVideoAssemblerAgent to enable accessible and captioned video workflows."
        ],
        "tags": ["AI", "Subtitle", "SRT", "Multimodal", "Video"]
    },
    "ImageAgent": {
        "type": "AI-Image",
        "short_description": "Generates a single image from a text prompt using the configured image model.",
        "detailed_description": [
            "This agent takes a text prompt and uses a model (like DALL·E or Stable Diffusion) to generate an image.",
            "The image is saved to the specified output path and can be used in video content, blogs, or design work.",
            "The model can be swapped (e.g. DALL·E via OpenAI or Stable Diffusion via Hugging Face or local instance) for flexible deployment."
        ],
        "tags": ["AI", "Image", "Text-to-Image", "Vision"]
    },
    "ScriptStructureValidatorAgent": {
        "type": "Validator",
        "short_description": "Checks if all expected sections are present in a structured script.",
        "detailed_description": [
            "Useful to validate LLM output structure before downstream tasks like TTS or image generation.",
            "Can help trigger retries or corrections if output is incomplete."
        ],
        "tags": ["Validation", "Script", "QA"]
    },
    "ScriptFeedbackValidatorAgent": {
        "type": "Validator",
        "short_description": "Evaluates script quality and suggests improvements.",
        "detailed_description": [
            "This agent analyzes a structured script and provides feedback to improve clarity, tone, and structure.",
            "Returns a numeric score from 1 to 100, a list of recommendations, and a revised prompt suggestion to regenerate the script.",
            "Useful for iterating toward higher-quality content before proceeding to audio/image generation."
        ],
        "tags": ["AI", "Validator", "Feedback", "Script"]
    },
    "ImageAnalysisAgent": {
        "type": "AI",
        "short_description": "Analyzes an image using GPT-4 Vision to extract insights or descriptions.",
        "detailed_description": [
            "This agent uses OpenAI's GPT-4 Vision model to analyze image content based on a provided natural language prompt.",
            "Ideal for extracting descriptions, summarizing visual scenes, or generating context-aware captions.",
            "Requires a valid local image path and a prompt."
        ],
        "tags": ["AI", "Vision", "Image Analysis", "GPT-4"]
    },
    "GenericEmailAgent": {
        "type": "Utility",
        "short_description": "Sends a plain text email via SMTP.",
        "detailed_description": [
            "Uses SMTP to send an email.",
            "Supports custom subject, sender, recipient, and body.",
            "Works with any SMTP-compatible provider."
        ],
        "tags": ["Utility", "Email"]
    },
    "WebhookAgent": {
        "type": "Utility",
        "short_description": "Sends a POST request to a webhook URL.",
        "detailed_description": [
            "Sends JSON payloads to external APIs or services.",
            "Useful for integrations, notifications, and serverless hooks."
        ],
        "tags": ["Utility", "Webhook"]
    },
    "SlackAgent": {
        "type": "Utility",
        "short_description": "Sends a message to a Slack channel via webhook.",
        "detailed_description": [
            "Posts formatted messages to Slack using an incoming webhook.",
            "Use for alerts, updates, and chatops workflows."
        ],
        "tags": ["Utility", "Slack"]
    },
    "CameraCaptureAgent": {
        "short_description": "Capture photo from system camera",
        "detailed_description": [
            "This utility agent uses the system's default camera (e.g., webcam) to capture a single image frame on-demand.",
            "It supports both Mac and Windows environments and uses OpenCV to access and operate the camera device.",
            "Captured images are saved with timestamped filenames in the specified output directory, and the full path is returned for downstream use."
        ],
        "tags": ["Utility", "Camera"]
    }
}
