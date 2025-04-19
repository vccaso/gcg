# 🤖 OrishAI Built-in Agent Examples

This guide provides YAML workflow examples for each built-in agent available in the OrishAI framework. These agents can be chained using workflow steps and are configured via the `agent` and `input` keys.

---

## 📁 `GitHubCloneOrUpdateRepoAgent`
```yaml
- name: clone_repo
  type: git
  agent: GitHubCloneOrUpdateRepoAgent
  input:
    repo_url: https://github.com/username/my-repo.git
    local_repo_dir: ./workspace/my-repo
```

---

## 🌱 `GitHubCheckoutBranchAgent`
```yaml
- name: checkout_branch
  type: git
  agent: GitHubCheckoutBranchAgent
  input:
    source_branch: dev
    local_repo_dir: ${local_repo_dir}
```

---

## 📦 `RequirementsExtractorAgent`
```yaml
- name: extract_requirements
  type: git
  agent: RequirementsExtractorAgent
  input:
    repo_path: ${local_repo_dir}
    key: requirements
```

---

## 💾 `SaveToFileAgent`
```yaml
- name: save_requirements
  type: utils
  agent: SaveToFileAgent
  input:
    content_from: extract_requirements.requirements
    file_path: ./workspace/requirements.txt
```

---

## 🧠 `RAGDatabaseBuilderAgent`
```yaml
- name: build_vector_db
  type: rag
  agent: RAGDatabaseBuilderAgent
  input:
    source_files:
      - ./docs/intro.txt
      - ./docs/specs.txt
    collection_name: docs_collection
    storage_path: rag_dbs
    model: all-MiniLM-L6-v2
```

---

## 🔁 `RAGDatabaseUpdaterAgent`
```yaml
- name: update_vector_db
  type: rag
  agent: RAGDatabaseUpdaterAgent
  input:
    new_docs:
      - ./docs/changelog.txt
    collection_name: docs_collection
    storage_path: rag_dbs
```

---

## 🧲 `RAGQueryAgent`
```yaml
- name: query_knowledge
  type: rag
  agent: RAGQueryAgent
  input:
    collection_name: docs_collection
    user_query: What features were introduced in version 2?
    storage_path: rag_dbs
```

---

## 🔗 `RAGAttachAgent`
```yaml
- name: attach_docs_collection
  type: rag
  agent: RAGAttachAgent
  input:
    collection_name: docs_collection
    alias: default_docs
    storage_path: rag_dbs
```

---

## 🧾 `GoCRUDAgent` (example code generation agent)
```yaml
- name: generate_go_crud
  type: llm
  agent: GoCRUDAgent
  input:
    final_prompt: Generate CRUD handlers in Go for a model called "Project" with fields: id, name, deadline.
```

---

## 💬 `ChatAgent`
```yaml
- name: ask_question
  type: llm
  agent: ChatAgent
  input:
    prompt: What are the benefits of microservices?
    save_to_file: true
    file_name: ./output/chat_log.txt
```

---

Feel free to mix and match agents using `content_from` or `vars` to form powerful, repeatable AI workflows!

