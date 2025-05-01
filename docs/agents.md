# 📄 agents.md

## Supported Agents

| Agent                      | Description                                   | Tags                            |
|----------------------------|-----------------------------------------------|---------------------------------|
| **ChatAgent**              | Q&A, content generation                       | [AI]                            |
| **GoCRUDAgent**            | Full-stack Go CRUD                            | [AI], [Go]                      |
| **GoCRUDModelAgent**       | Go structs only                               | [AI], [Go]                      |
| **GoCRUDDataAgent**        | Go SQL DAO                                    | [AI], [Go]                      |
| **GoSwaggerAgent**         | Swagger docs                                  | [AI], [Swagger]                 |
| **AngularAppAgent**        | Angular frontend code                         | [AI], [Frontend]                |
| **Dalle3Agent**            | Text-to-image                                 | [AI], [Image]                   |
| **AudioAgent**             | Audio TTS/STT                                 | [AI], [Audio]                   |
| **SaveToFileAgent**        | Save output to files                          | [Utility]                       |
| **GitHub Agents**          | Git automation tasks                          | [GitHub]                        |
| **SegmentedAudioAgent**    | Segment-wise TTS from structured scripts      | [AI], [Audio], [Multimodal]     |
| **SegmentedImageAgent**    | Generate images per script section            | [AI], [Image], [DALL-E]         |
| **SegmentedVideoAssemblerAgent** | Assemble video from segmented audio+image  | [AI], [Video], [Multimodal]     |
| **SegmentedSubtitleGeneratorAgent** | Generate SRT subtitles for segmented video | [AI], [Subtitle], [Utility]     |

---

### ✨ Extending Agents

1. Add a new class in `agents/`
2. Register it in `agent_registry.py`
3. Define:
   - `type`
   - `short_description`
   - `detailed_description`
   - `tags`

Agents can support types:
- `ai`, `ai-image`, `ai-audio`, `tool`, `rag`, etc.


---

Dynamic agent and model catalog available in the **Streamlit UI**!

