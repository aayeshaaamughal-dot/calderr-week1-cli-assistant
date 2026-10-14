\# Week 2 — Code Review Agent



\## Overview

An AI-powered Python code review tool built using Groq API, Pydantic v2, and Python.



\## Features

\- Reviews code for bugs, security issues, style, and performance.

\- Produces structured JSON reports using Pydantic.

\- Generates a readable Markdown report.

\- Includes five sample test cases.

\- Identifies potential runtime errors and hard-coded credentials.



\## Requirements

\- Python 3.10+

\- groq

\- pydantic

\- python-dotenv



\## Setup



1\. Clone or download the project.

2\. Activate your Python virtual environment.

3\. Install dependencies:



&#x20;  `pip install groq pydantic python-dotenv`



4\. Create a `.env` file in the project root and add your Groq API key:



&#x20;  `GROQ\_API\_KEY=your\_groq\_api\_key\_here`



&#x20;  Never upload your real API key to GitHub.



\## Run the Agent



`python code\_review\_agent.py`



Paste Python code into the terminal and enter `END` on a separate line to review it. Enter `EXIT` to quit.



\## Run Tests



`python test\_code\_review.py`



The test script submits five code samples to the AI reviewer. Results can vary, and they should be checked manually.



\## Security Note

AI-generated reviews are advisory only. Review the findings manually and use dedicated security and testing tools for production code.

