# Architecture

## Target architecture

```text
                         ┌──────────────────┐
                         │     Employee     │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     Web UI       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   API Gateway    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  AWS Lambda      │
                         │  Python backend  │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
             ┌────────────┐ ┌───────────┐ ┌────────────┐
             │  Bedrock   │ │ Knowledge │ │  Tools     │
             │   Model    │ │   Base    │ │            │
             └────────────┘ └─────┬─────┘ └─────┬──────┘
                                  │             │
                                  ▼             ▼
                             ┌─────────┐   ┌────────────┐
                             │   S3    │   │ DynamoDB   │
                             └─────────┘   └────────────┘
```

## Security principles

- Least privilege IAM
- No credentials in Git
- Validate tool inputs
- Restrict available tools
- Human approval for sensitive actions
- Avoid real personal/company data
- Log actions safely

## Evolution

### Version 1

```text
User → Python → LLM → Answer
```

### Version 2

```text
User → Python → RAG → LLM → Answer + sources
```

### Version 3

```text
User → API → Bedrock → Knowledge Base
                    ↓
                  Tools
                    ↓
                Ticket DB
```

### Version 4

```text
AWS deployment + Docker + CI/CD + evaluation + security controls
```
