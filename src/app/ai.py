import json
import os

import boto3
from dotenv import load_dotenv

from .schemas import HelpdeskResponse


load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-west-2")
MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    "amazon.nova-lite-v1:0"
)

KNOWLEDGE_BASE_ID = os.getenv(
    "BEDROCK_KNOWLEDGE_BASE_ID"
)


bedrock = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
)

bedrock_agent_runtime = boto3.client(
    "bedrock-agent-runtime",
    region_name=AWS_REGION,
)


def retrieve_knowledge(message: str):
    print("RAG: starting knowledge retrieval")
    print("RAG: knowledge base configured:", bool(KNOWLEDGE_BASE_ID))

    response = bedrock_agent_runtime.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={
            "text": message
        },
        retrievalConfiguration={
            "managedSearchConfiguration": {
                "numberOfResults": 3
            }
        }
    )

    print("RAG: retrieval successful")

    results = response.get("retrievalResults", [])

    if not results:
        return (
            "No relevant approved knowledge was found.",
            []
        )

    context_parts = []
    sources = []

    for result in results:
        content = result.get("content", {})
        text = content.get("text")

        if text:
            context_parts.append(text)

        location = result.get("location", {})

        if location.get("type") == "S3":
            s3_location = location.get("s3Location", {})
            source_uri = s3_location.get("uri")

            if source_uri:
                source_name = source_uri.split("/")[-1]

                if source_name not in sources:
                    sources.append(source_name)

    context = "\n\n".join(context_parts)

    return context, sources


def generate_helpdesk_response(message: str) -> HelpdeskResponse:
    knowledge_context, sources = retrieve_knowledge(message)

    prompt = f"""
You are an IT helpdesk assistant.

Your job is to analyse an employee's IT problem and provide guidance
using the approved IT knowledge provided below.

Approved IT knowledge:
{knowledge_context}

Employee problem:
{message}

Rules:

1. Base troubleshooting guidance primarily on the approved IT knowledge.
2. Do not invent company policies or procedures.
3. If the approved knowledge does not contain enough information,
   say so clearly and recommend human IT support when appropriate.
4. Never ask the employee for passwords.
5. Return ONLY valid JSON.
6. Do not include markdown.
7. Do not include ```json.
8. Do not include text before or after the JSON.

Use exactly these fields:

category
priority
summary
answer
needs_human

category:
Choose one of:
- Network
- Hardware
- Software
- Account
- Email
- Security
- Server
- Printer
- General IT

priority:
Choose exactly one:
- Low
- Medium
- High
- Critical

summary:
Write one short sentence summarising the issue.

answer:
Provide clear troubleshooting guidance based on the approved IT knowledge.

needs_human:
Return true when:
- the approved knowledge says escalation is required
- the problem is security-related
- multiple employees are affected
- administrator access is required
- the issue is critical
- there is not enough approved information to safely solve the problem

Otherwise return false.

Return JSON in this format:

{{
    "category": "Network",
    "priority": "Medium",
    "summary": "Employee cannot connect their laptop to Wi-Fi.",
    "answer": "Confirm Wi-Fi is enabled and airplane mode is disabled.",
    "needs_human": false
}}
"""

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ],
            }
        ],
        inferenceConfig={
            "maxTokens": 500,
            "temperature": 0.2,
        },
    )

    model_text = response["output"]["message"]["content"][0]["text"]

    data = json.loads(model_text)

    return HelpdeskResponse(
        category=data["category"],
        priority=data["priority"],
        summary=data["summary"],
        answer=data["answer"],
        needs_human=data["needs_human"],
        sources=sources,
    )