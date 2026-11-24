# Multi-Agent Market Research & Report Generator

A multi-agent market research application built with CrewAI, Python, OpenAI, Tavily, Pandas, and ReportLab.

The system uses hierarchical agent orchestration to research market trends, analyze financial data, and generate professional research reports.

## Features

- **Hierarchical AI orchestration:** A manager LLM coordinates three specialized agents.
- **Market research:** Tavily-powered web search for companies, financial information, and industry trends.
- **Financial analysis:** Pandas-based statistical analysis, including mean, standard deviation, minimum, and maximum.
- **Report generation:** Professional PDF and Markdown reports.
- **Benchmarking:** Execution time and task-routing history stored in JSON.
- **Automated testing:** Pytest tests for financial analysis, PDF generation, Markdown generation, and benchmarking.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Application development |
| CrewAI | Multi-agent orchestration |
| OpenAI | Language models |
| Tavily | Web research |
| Pandas | Financial data analysis |
| ReportLab | PDF generation |
| Pytest | Automated testing |

## Project Structure

```text
multi-agent-market-research/
│
├── config/
│   ├── settings.py
│   └── __init__.py
│
├── crew/
│   ├── agents.py
│   ├── tasks.py
│   ├── crew.py
│   └── __init__.py
│
├── tools/
│   ├── web_search_tool.py
│   ├── financial_data_tool.py
│   └── __init__.py
│
├── services/
│   ├── benchmark.py
│   ├── markdown_generator.py
│   ├── report_generator.py
│   └── __init__.py
│
├── tests/
│   ├── test_financial_data.py
│   ├── test_report_generator.py
│   ├── test_markdown_generator.py
│   └── test_benchmark.py
│
├── data/
│   └── sample_financial_data.csv
│
├── output/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yeswanth-k15/multi-agent-market-research.git
cd multi-agent-market-research
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

Copy `.env.example` to `.env`.

Windows CMD:

```cmd
copy .env.example .env
```

Configure the following values in `.env`:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
SERPER_API_KEY=

MODEL_NAME=gpt-4o-mini
MANAGER_MODEL=gpt-4o
```

Never commit `.env` or expose API keys publicly.

## Running the Application

Run the market research workflow:

```bash
python main.py --query "Tech Sector Q3 Analysis"
```

Another example:

```bash
python main.py --query "Artificial Intelligence Market Trends"
```

## Generated Outputs

After a successful execution:

```text
output/
├── market_report.pdf
└── market_report.md

benchmarks.json
```

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Run individual tests:

```bash
python -m pytest tests/test_financial_data.py -v
python -m pytest tests/test_report_generator.py -v
python -m pytest tests/test_markdown_generator.py -v
python -m pytest tests/test_benchmark.py -v
```

## Benchmarking

The benchmark tracker records:

- Research query
- Workflow execution time
- Number of recorded tasks
- Assigned agent information
- Task execution status
- Task timestamps

Results are stored in `benchmarks.json`.

## Security

- Store credentials in `.env`.
- Keep `.env` out of version control.
- Never expose API keys in source code, prompts, or public repositories.
- Rotate credentials if they are accidentally exposed.

## License

This project is developed for educational and assessment purposes.