# Game Master Meets AI: A Tutorial from Basic Chatbot to AI Agent

Welcome to this hands-on tutorial where we'll build a TTRPG Game Master Assistant from the ground up. This project was originally created for a friend who loves TTRPGs and is just getting started with AI. The goal is to provide a practical overview of the key concepts and technologies that an AI developer uses every day, without getting bogged down in the complexities of building LLMs from scratch, deploying LLM servers, or the associated MLOps.

## Scope and Prerequisites

This tutorial is designed for developers who have a basic understanding of Python and want to learn how to build applications with Large Language Models. You don't need any prior experience with AI or machine learning but we do expect you to know some python basics and asynchronous function calls (there are multiple tutorials and resources online on these).

**What We'll Cover:**

*   **Building a Minimal Full-Stack Application**: We'll use FastAPI for the backend, Streamlit for the frontend, and Docker to containerize our application.
*   **AI Agent Development**: We'll use LangChain to build an AI agent 
that can use tools to answer questions and perform tasks.
*   **Retrieval-Augmented Generation (RAG)**: We'll build a "Lore 
Keeper" agent that can answer questions about a specific knowledge base.
*   **Model Context Protocol (MCP)**: We'll explore how to build a more 
robust and scalable agentic architecture with MCP.*   **Direct LLM Integration**: We'll use the `google-generativeai` SDK to interact directly with Google's Gemini models, giving you a fundamental understanding of how to work with modern LLM APIs.
*   **AI Agent Development**: We'll build a sophisticated AI agent from scratch that can use multiple tools in a multi-step reasoning loop to answer complex questions and perform tasks.
*   **Retrieval-Augmented Generation (RAG)**: We'll build a "Lore Keeper" tool that can answer questions about a specific knowledge base.
*   **Model Context Protocol (MCP)**: We'll show how to expose an API as a set of tools for other AI agents to consume using the MCP standard and the `fastapi-mcp` library.

**What We Won't Cover:**

*   **Building LLMs**: We'll be using pre-trained models from Google. Training LLMs and other models is a deeply fascinating area that requires a lot of background and material that is out of scope of this tutorial, aimed to help people get started with AI dev than with ML Engineering.
*   **LLMOps and AIOps**: We'll focus on the application development side of things, but we'll provide some resources for further learning. You're highly recommended to learn about this topic as it is important for observability and deployments in a production system.

This tutorial was produced using Google Gemini for speed, with some minor corrections from me. This was by design: I want you to double-check the functions and obsess about the implementation as an exercise (this is in the style professors and books in Mathematics courses typically have "Show this as an exercise" questions).

For example, examine the code for the following questions:
- Can it be done more efficiently?
- Can I make it more maintainable?
- What would be the tests I should write for these functions? Check out [`deepeval`](https://github.com/confident-ai/deepeval).
- What if I had a lot of data?
- Can I create a new tool?
- Why does this code work?

With these questions, you will engage by searching for their use, reading documentation and also exercising the skill of trying to review code (see e.g. this [link](https://stackoverflow.blog/2019/09/30/how-to-make-good-code-reviews-better/) for example).

I also recommend the [Kaggle 5-Day Gen AI Intensive Course with Google](https://www.kaggle.com/learn-guide/5-day-genai) for a more in-depth discussion of some elements covered in this tutorial. The skill level required for it is higher, however.

## Technologies and Concepts

Throughout this tutorial, we'll be working with the following technologies and concepts:

| Technology | Description |
| --- | --- |
| **Python** | The primary programming language for this tutorial. |
| **FastAPI** | A modern, high-performance web framework for building APIs. |
| **Streamlit** | An open-source framework for building beautiful, custom web apps. |
| **Docker** | A platform for developing, shipping, and running applications in containers. |
| **Google Generative AI** | The official Python SDK for interacting with Google's Gemini family of models. |
| **Chroma DB** | An open-source embedding database for building AI applications with RAG. |
| **MCP & fastapi-mcp** | A protocol and library for exposing APIs as discoverable tools for AI agents. |

## Folder Structure

This repository is organized into five chapters, each one building on the concepts of the last. A key feature of this tutorial is that **each chapter is a self-contained, runnable application**.

```
dnd-ai-tutorial/
├── chapter1/  # Basic FastAPI + Streamlit + Docker Setup
├── chapter2/  # Structured Output (JSON) from an LLM
├── chapter3/  # Simple, single-tool agent (Dice Roller)
├── chapter4/  # Multi-tool agent with RAG (Lore Keeper)
└── chapter5/  # Exposing the API as tools with MCP and building a multi-step agent
```

Inside each chapter's folder, you will find everything needed to build and run that specific stage of the project, including its own `docker-compose.yaml` file, `Dockerfile`, and Python source code. The `backend` folder covers the beating heart of the applications, while `frontend.py` is always just a simple implementation of a chat interface.

## How to Use This Course

The best way to use this course is to go through the chapters in order, as each one introduces new concepts and technologies that are used in later chapters.

Because each chapter is a self-contained application, you can run them independently. To run a specific chapter, simply navigate to its directory in your terminal and run the `docker-compose up --build` command. Each chapter's `README.md` file contains detailed instructions and explanations of the new concepts introduced in that chapter.

## Getting Started

Before you can run the applications in this tutorial, you'll need to get a Google API key. This is required to use the generative AI models that power our TTRPG Game Master Assistant.

1.  **Get an API Key**: You can get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  **Set up your Environment**: Each chapter that requires an API key includes a `README.md` with instructions on how to set up a `.env` file to store your key.

## Additional Resources

To learn more about the topics that are not covered in this tutorial, check out these excellent introductory resources:

*   **MLOps**: [MLOps Community](https://mlops.community/)
*   **AIOps**: [What is AIOps?](https://www.redhat.com/en/topics/cloud-native-apps/what-is-aiops)
*   **Building LLMs**: [Andrej Karpathy's "Let's build GPT" YouTube series](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ)
