# Project Specification

## Project name

AI IT Service Desk Agent

## Problem

Employees frequently ask IT support questions that are repetitive, documented, and suitable for guided troubleshooting.

The goal is to build a controlled AI assistant that can answer common questions from an approved knowledge base and automate low-risk service-desk workflows.

## Users

- Employee
- IT support analyst
- IT administrator

## Functional requirements

### FR1 — Ask a question

The user can submit an IT support question.

### FR2 — Classify

The system classifies the request.

### FR3 — Retrieve

The system retrieves relevant approved documentation.

### FR4 — Answer

The system generates a grounded answer.

### FR5 — Cite

The system identifies the knowledge sources used.

### FR6 — Ticket

The system can create a demo support ticket.

### FR7 — Ticket status

The system can retrieve the status of a demo ticket.

### FR8 — Escalation

The system can recommend human escalation.

### FR9 — Approval

Sensitive actions require explicit human approval.

### FR10 — Logging

Important application and tool events are logged without exposing secrets.

## Non-functional requirements

- Clear error handling
- Automated tests
- Secure credential handling
- Reproducible setup
- Documented architecture
- Reasonable AWS cost
- No production/company confidential data

## Out of scope

- Real company ticketing integration
- Real password resets
- Real account disabling
- Production employee data
- Autonomous security administration
- Unrestricted shell/terminal access by the AI
