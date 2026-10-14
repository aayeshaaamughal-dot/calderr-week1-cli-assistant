

\# Intelligent CLI Assistant



\## Project Overview

A terminal-based AI assistant built with Python and the Groq API.

It supports conversational memory, topic management, formatted output,

and token usage reporting.



\## Features

\- AI-powered conversation using Groq

\- Conversation history during the current session

\- `/topic <name>` to change the conversation topic

\- `/topic` to display the current topic

\- `/clear` to clear conversation memory

\- `/help` to display available commands

\- `/exit` to close the assistant

\- Token usage reporting

\- Error handling for failed requests



\## Technologies

\- Python

\- Groq API

\- python-dotenv

\- Rich



\## Setup

1\. Create and activate a Python virtual environment.

2\. Install the required dependencies.

3\. Create a `.env` file in the project root.

4\. Add your Groq API key:



&#x20;     GROQ\_API\_KEY=your\_groq\_api\_key\_here



\## Run the Assistant

python cli\_assistant.py



\## Run Basic Evaluation

python evaluate\_cli.py



\## Evaluation

The current basic command evaluation contains seven checks.

All seven checks passed in the latest run.

This does not yet represent the required ten-turn conversation quality evaluation.



\## Security

Never commit the `.env` file or publish API keys.



