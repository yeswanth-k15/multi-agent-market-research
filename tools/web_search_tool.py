import json
import os
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import TavilyClient


class TavilySearchInput(BaseModel):
    """Input schema for the Tavily web search tool."""

    query: str = Field(
        ...,
        description="The company, financial metric, industry, or market topic to research.",
    )

    max_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum number of search results to return.",
    )


class TavilySearchTool(BaseTool):
    """Search the web and retrieve information using Tavily."""

    name: str = "Tavily Web Research Tool"

    description: str = (
        "Search the internet for company information, financial results, "
        "industry trends, market developments, and business news. "
        "Returns source titles, URLs, content, and relevance scores."
    )

    args_schema: Type[BaseModel] = TavilySearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        """Execute a Tavily search and return structured results."""

        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            return (
                "Error: TAVILY_API_KEY is missing. "
                "Configure it in the project's .env file."
            )

        try:
            client = TavilyClient(api_key=api_key)

            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_raw_content=True,
            )

            results = []

            for item in response.get("results", []):
                results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "content": item.get("content", ""),
                        "raw_content": item.get("raw_content", ""),
                        "score": item.get("score", 0),
                        "published_date": item.get("published_date", ""),
                    }
                )

            if not results:
                return f"No search results found for: {query}"

            return json.dumps(
                {
                    "query": query,
                    "total_results": len(results),
                    "results": results,
                },
                indent=2,
                ensure_ascii=False,
            )

        except Exception as exc:
            return f"Tavily search failed: {type(exc).__name__}: {exc}"