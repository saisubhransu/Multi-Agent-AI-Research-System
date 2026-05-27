# ResearchMind 🔬

An elegant, multi-agent research pipeline that automates the process of searching, reading, writing, and reviewing research reports on any topic. Powered by **LangChain** and **Groq**.

## Features

- **Search Agent**: Searches the web using the Tavily API for fresh, reliable facts.
- **Reader Agent**: Scrapes and parses top resource URLs for deeper reading.
- **Writer Chain**: Synthesizes the information into a structured, professional report.
- **Critic Chain**: Reviews the final report and provides a critique and score.
- **Interactive UI**: A modern, responsive Streamlit dashboard tracking the execution in real time.

---

## Project Structure

```text
├── .env.example       # Template for API keys
├── .gitignore         # Ignores secrets and environments
├── agents.py          # LLM definitions & agent creation
├── app.py             # Streamlit application UI
├── pipeline.py        # Pipeline workflow coordinator
├── requirements.txt   # Project dependencies
└── tools.py           # Tavily search & BeautifulSoup scraper tools
```
