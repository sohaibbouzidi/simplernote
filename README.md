# AI Memory & Task Management Platform

A production-ready fullstack platform for AI-agent memory management, task orchestration, structured notes, and external agent integrations.

Designed as the foundational layer for autonomous AI workflows including planner agents, research agents, coding agents, reviewer agents, and future orchestration systems.

---

# Features

## Core Features

* User authentication
* Project management
* Structured notes system
* Task & subtask management
* Kanban workflow
* API key management
* Activity logs
* Markdown notes
* Tags & filtering
* REST API architecture
* Dockerized setup

---

# AI-Agent Ready Architecture

The platform is designed to support future autonomous AI workflows:

```text id="v3up3j"
User Prompt
    ↓
Planner Agent
    ↓
Memory Retrieval
    ↓
Research Agent
    ↓
Coding Agent
    ↓
Reviewer Agent
    ↓
Task + Notes Updates
```

External agents can securely communicate through API keys.

---

# Tech Stack

## Frontend

* Nuxt 3
* TypeScript
* Pinia
* TailwindCSS
* ShadCN Vue

## Backend

* FastAPI
* SQLAlchemy
* Pydantic
* Alembic
* JWT Authentication

## Database

* PostgreSQL 16

## Infrastructure

* Docker
* Docker Compose
* Redis (future workflows)

---

# Project Structure

```text id="7k8n6z"
apps/
├── frontend/
├── backend/
├── docker/
├── docs/
└── scripts/
```

---

# Main Modules

## Projects

Projects isolate:

* notes
* tasks
* memories
* logs

---

# Notes

Supports:

* markdown editor
* note types
* tagging
* search
* structured memory

Example note types:

* memory
* decision
* research
* issue
* workflow
* architecture

---

# Tasks

Supports:

* subtasks
* kanban workflow
* priorities
* task hierarchy
* agent assignment

Workflow example:

```text id="dh7jwf"
TODO → RESEARCH → CODING → REVIEW → DONE
```

---

# API Keys

Secure API keys allow external systems and AI agents to:

* create tasks
* store notes
* update workflows
* retrieve memories

Example:

```http id="pud9b3"
Authorization: Bearer sk_xxxxx
```

---

# Development Setup

## Requirements

* Docker
* Docker Compose

---

# Start Development Environment

```bash id="9aw3e0"
docker compose up --build
```

---

# Frontend

```text id="o5rzew"
http://localhost:3000
```

---

# Backend API

```text id="d2j4e5"
http://localhost:8000
```

---

# Planned Features

## Phase 2

* pgvector integration
* embeddings
* semantic search
* AI memory retrieval

## Phase 3

* LangGraph orchestration
* autonomous workflows
* multi-agent execution
* RAG pipelines
* knowledge graphs

---

# Architecture Goals

* Modular
* Scalable
* AI-agent ready
* API-first
* Future-proof
* Production-ready

---

# Future Vision

This platform is intended to become a complete AI operating memory layer capable of:

* autonomous planning
* persistent memory
* task orchestration
* contextual retrieval
* multi-agent collaboration
* long-running workflows

---

# License

MIT License
