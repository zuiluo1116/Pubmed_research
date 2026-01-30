"""
PubMed Search Tool for OpenWebUI

This tool enables LLM-driven literature searches on PubMed with advanced filtering.
It uses NCBI E-utilities API (esearch + efetch) to search and retrieve article data
including abstracts.

Author: ZuiLuo1116 using K-Dense Framework
Version: 1.0.0
"""

import requests
import xml.etree.ElementTree as ET
import time
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class Tools:
    """
    OpenWebUI Tool class for PubMed literature search.

    This tool allows the LLM to search PubMed for scientific literature
    with advanced filtering options including date range, author, journal,
    and publication type filters.
    """

    class Valves(BaseModel):
        """Configuration valves for the PubMed Search Tool."""
        NCBI_API_KEY: str = Field(
            default="",
            description="Optional NCBI API key for higher rate limits (10 req/sec vs 3 req/sec)"
        )
        NCBI_EMAIL: str = Field(
            default="",
            description="Email address for NCBI API identification (recommended)"
        )
        MAX_RESULTS: int = Field(
            default=10,
            description="Default maximum number of results to return",
            ge=1,
            le=100
        )

    def __init__(self):
        """Initialize the PubMed Search Tool."""
        self.valves = self.Valves()
        self.base_url_search = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.base_url_fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        self._last_request_time = 0
        self._min_request_interval = 0.34  # 3 requests per second max without API key

    def _rate_limit(self):
        """Ensure we don't exceed NCBI rate limits."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_request_interval:
            time.sleep(self._min_request_interval - elapsed)
        self._last_request_time = time.time()

    def _build_search_query(
        self,
        query: str,
        author: Optional[str] = None,
        journal: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        publication_type: Optional[str] = None
    ) -> str:
        """
        Build a PubMed search query with filters.

        Args:
            query: Main search terms
            author: Author name filter
            journal: Journal name/abbreviation filter
            date_from: Start date (YYYY/MM/DD or YYYY)
            date_to: End date (YYYY/MM/DD or YYYY)
            publication_type: Publication type (e.g., Review, Clinical Trial)

        Returns:
            Formatted PubMed query string
        """
        terms = [query]

        if author:
            terms.append(f"{author}[AU]")

        if journal:
            terms.append(f"{journal}[TA]")

        if publication_type:
            # Map common publication types to PubMed codes
            pt_mapping = {
                "review": "Review[PT]",
                "clinical trial": "Clinical Trial[PT]",
                "meta-analysis": "Meta-Analysis[PT]",
                "randomized controlled trial": "Randomized Controlled Trial[PT]",
                "case report": "Case Reports[PT]",
                "systematic review": "Systematic Review[PT]",
                "letter": "Letter[PT]",
                "editorial": "Editorial[PT]",
            }
            pt_lower = publication_type.lower()
            if pt_lower in pt_mapping:
                terms.append(pt_mapping[pt_lower])
            else:
                terms.append(f"{publication_type}[PT]")

        full_query = " AND ".join(terms)

        return full_query

    def _search_pubmed(
        self,
        query: str,
        max_results: int,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[str]:
        """
        Search PubMed and return list of PMIDs.

        Args:
            query: Search query
            max_results: Maximum number of results
            date_from: Minimum date filter
            date_to: Maximum date filter

        Returns:
            List of PMID strings
        """
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": "relevance"
        }

        if date_from:
            params["mindate"] = date_from
        if date_to:
            params["maxdate"] = date_to
        if date_from or date_to:
            params["datetype"] = "pdat"  # Publication date

        if self.valves.NCBI_API_KEY:
            params["api_key"] = self.valves.NCBI_API_KEY
        if self.valves.NCBI_EMAIL:
            params["email"] = self.valves.NCBI_EMAIL

        try:
            self._rate_limit()
            response = requests.get(self.base_url_search, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            id_list = data.get("esearchresult", {}).get("idlist", [])
            return id_list

        except Exception as e:
            raise Exception(f"PubMed search failed: {str(e)}")

    def _fetch_article_details(self, pmids: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch detailed article information including abstracts.

        Args:
            pmids: List of PubMed IDs

        Returns:
            List of article dictionaries
        """
        if not pmids:
            return []

        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "rettype": "abstract"
        }

        if self.valves.NCBI_API_KEY:
            params["api_key"] = self.valves.NCBI_API_KEY
        if self.valves.NCBI_EMAIL:
            params["email"] = self.valves.NCBI_EMAIL

        try:
            self._rate_limit()
            response = requests.get(self.base_url_fetch, params=params, timeout=60)
            response.raise_for_status()

            return self._parse_pubmed_xml(response.text)

        except Exception as e:
            raise Exception(f"Failed to fetch article details: {str(e)}")

    def _parse_pubmed_xml(self, xml_content: str) -> List[Dict[str, Any]]:
        """
        Parse PubMed XML response to extract article data.

        Args:
            xml_content: XML string from efetch

        Returns:
            List of article dictionaries
        """
        articles = []

        try:
            root = ET.fromstring(xml_content)

            for article_elem in root.findall(".//PubmedArticle"):
                article = {}

                # PMID
                pmid_elem = article_elem.find(".//PMID")
                article["pmid"] = pmid_elem.text if pmid_elem is not None else ""

                # Title
                title_elem = article_elem.find(".//ArticleTitle")
                article["title"] = title_elem.text if title_elem is not None else "No title available"

                # Authors
                authors = []
                for author_elem in article_elem.findall(".//Author"):
                    lastname = author_elem.find("LastName")
                    forename = author_elem.find("ForeName")
                    if lastname is not None:
                        name = lastname.text
                        if forename is not None:
                            name = f"{lastname.text} {forename.text}"
                        authors.append(name)
                article["authors"] = authors[:5]  # Limit to first 5 authors
                if len(authors) > 5:
                    article["authors"].append("et al.")

                # Journal
                journal_elem = article_elem.find(".//Journal/Title")
                article["journal"] = journal_elem.text if journal_elem is not None else ""

                # Publication Date
                pub_date = article_elem.find(".//PubDate")
                if pub_date is not None:
                    year = pub_date.find("Year")
                    month = pub_date.find("Month")
                    day = pub_date.find("Day")
                    date_parts = []
                    if year is not None:
                        date_parts.append(year.text)
                    if month is not None:
                        date_parts.append(month.text)
                    if day is not None:
                        date_parts.append(day.text)
                    article["pub_date"] = " ".join(date_parts) if date_parts else ""
                else:
                    article["pub_date"] = ""

                # Abstract
                abstract_texts = []
                for abstract_elem in article_elem.findall(".//AbstractText"):
                    label = abstract_elem.get("Label", "")
                    text = "".join(abstract_elem.itertext())
                    if label:
                        abstract_texts.append(f"**{label}**: {text}")
                    else:
                        abstract_texts.append(text)
                article["abstract"] = " ".join(abstract_texts) if abstract_texts else "No abstract available"

                # DOI
                for id_elem in article_elem.findall(".//ArticleId"):
                    if id_elem.get("IdType") == "doi":
                        article["doi"] = id_elem.text
                        break
                else:
                    article["doi"] = ""

                # PubMed URL
                article["url"] = f"https://pubmed.ncbi.nlm.nih.gov/{article['pmid']}/"

                articles.append(article)

        except ET.ParseError as e:
            raise Exception(f"Failed to parse PubMed XML: {str(e)}")

        return articles

    def _format_results(self, articles: List[Dict[str, Any]], query: str) -> str:
        """
        Format search results as Markdown for LLM consumption.

        Args:
            articles: List of article dictionaries
            query: Original search query

        Returns:
            Markdown formatted string
        """
        if not articles:
            return f"## PubMed Search Results\n\nNo articles found for query: **{query}**"

        output_parts = []

        # Header with summary
        output_parts.append(f"## PubMed Search Results\n")
        output_parts.append(f"**Query**: {query}\n")
        output_parts.append(f"**Results Found**: {len(articles)} articles\n")
        output_parts.append(f"**Retrieved**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output_parts.append("---\n")

        # Individual articles
        for i, article in enumerate(articles, 1):
            output_parts.append(f"### {i}. {article['title']}\n")

            # Metadata line
            authors_str = ", ".join(article["authors"]) if article["authors"] else "Unknown authors"
            output_parts.append(f"**Authors**: {authors_str}\n")
            output_parts.append(f"**Journal**: {article['journal']} ({article['pub_date']})\n")
            output_parts.append(f"**PMID**: [{article['pmid']}]({article['url']})")

            if article["doi"]:
                output_parts.append(f" | **DOI**: {article['doi']}\n")
            else:
                output_parts.append("\n")

            # Abstract
            output_parts.append(f"\n**Abstract**:\n{article['abstract']}\n")
            output_parts.append("\n---\n")

        return "\n".join(output_parts)

    def search_pubmed(
        self,
        query: str,
        max_results: int = 10,
        author: Optional[str] = None,
        journal: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        publication_type: Optional[str] = None
    ) -> str:
        """
        Search PubMed for scientific literature with advanced filtering options.

        This function searches the PubMed database using the NCBI E-utilities API
        and returns formatted results including titles, authors, abstracts, and links.

        Args:
            query: Main search terms (e.g., "CRISPR gene editing", "breast cancer treatment").
                   Use AND/OR for complex queries.
            max_results: Maximum number of results to return (1-100, default: 10).
            author: Filter by author name (e.g., "Smith J", "Zhang Wei").
            journal: Filter by journal name or abbreviation (e.g., "Nature", "Cell", "NEJM").
            date_from: Start date for publication filter in YYYY or YYYY/MM/DD format
                       (e.g., "2020" or "2023/01/01").
            date_to: End date for publication filter in YYYY or YYYY/MM/DD format
                     (e.g., "2024" or "2024/12/31").
            publication_type: Filter by publication type. Options include:
                              "Review", "Clinical Trial", "Meta-Analysis",
                              "Randomized Controlled Trial", "Case Report",
                              "Systematic Review", "Letter", "Editorial".

        Returns:
            A Markdown-formatted string containing search results with:
            - Article titles
            - Author names
            - Journal and publication date
            - PMID with link to PubMed
            - DOI (if available)
            - Full abstract text

        Example:
            search_pubmed(
                query="CAR-T cell therapy",
                max_results=5,
                date_from="2023",
                publication_type="Review"
            )
        """
        try:
            # Use valve default if not specified
            if max_results is None:
                max_results = self.valves.MAX_RESULTS

            # Clamp max_results
            max_results = max(1, min(100, max_results))

            # Build search query with filters
            search_query = self._build_search_query(
                query=query,
                author=author,
                journal=journal,
                date_from=date_from,
                date_to=date_to,
                publication_type=publication_type
            )

            # Search for PMIDs
            pmids = self._search_pubmed(
                query=search_query,
                max_results=max_results,
                date_from=date_from,
                date_to=date_to
            )

            if not pmids:
                return f"## PubMed Search Results\n\nNo articles found for query: **{query}**\n\nFilters applied:\n- Author: {author or 'None'}\n- Journal: {journal or 'None'}\n- Date range: {date_from or 'Any'} to {date_to or 'Any'}\n- Publication type: {publication_type or 'Any'}"

            # Fetch detailed article information
            articles = self._fetch_article_details(pmids)

            # Format results
            return self._format_results(articles, query)

        except Exception as e:
            return f"## PubMed Search Error\n\nAn error occurred while searching PubMed: {str(e)}\n\nPlease try again with different search terms or check your network connection."


# For testing outside OpenWebUI
if __name__ == "__main__":
    tool = Tools()

    # Test basic search
    print("Testing PubMed Search Tool...")
    print("=" * 60)

    result = tool.search_pubmed(
        query="CRISPR gene editing",
        max_results=3,
        date_from="2024",
        publication_type="Review"
    )

    print(result)
