# Implementation Plan: OpenWebUI PubMed Search Plugin

## Overview
Create an OpenWebUI Tool plugin that enables LLM-driven PubMed literature searches with advanced filtering capabilities.

## User Requirements
1. **Advanced Filtering**: Support filtering by publication date, author, journal, and publication type
2. **Abstract Retrieval**: Must include abstracts in search results
3. **Tool Format**: Implement as OpenWebUI "Tool" (function calling)
4. **Output Format**: Provide both raw list and formatted summary
5. **Documentation**: Technical report (handled by writing agent)

## Implementation Steps

### Step 1: Environment Setup
- Sync dependencies with `uv sync`
- Verify requests and lxml are available

### Step 2: PubMed API Client Implementation
- Use NCBI E-utilities API (esearch + efetch)
- esearch: Search and get PMIDs with filters
- efetch: Retrieve full records with abstracts
- Support parameters:
  - `term`: Search query
  - `mindate/maxdate`: Date range filter
  - `author`: Author filter (uses [AU] tag)
  - `journal`: Journal filter (uses [TA] tag)
  - `ptyp`: Publication type filter

### Step 3: OpenWebUI Tool Structure
- Follow OpenWebUI Tools specification
- Create class with `Tools` as base
- Define function with proper type hints and docstrings
- Include Valves for configuration (API key, email)

### Step 4: Data Formatting
- Parse XML response from efetch
- Extract: PMID, Title, Authors, Journal, Date, Abstract, DOI
- Format as Markdown for LLM consumption
- Provide summary statistics

### Step 5: Testing
- Test with sample queries
- Verify filters work correctly
- Check abstract retrieval

### Step 6: Documentation
- Update README.md with usage instructions
- Prepare data for technical report

## Success Criteria
- [ ] Plugin code follows OpenWebUI Tool specification
- [ ] Advanced filters (date, author, journal, type) work correctly
- [ ] Abstracts are retrieved and included in output
- [ ] Output is formatted in Markdown for LLM readability
- [ ] Test script validates functionality

## Technical Details

### PubMed E-utilities Endpoints
- esearch: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- efetch: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`

### Query Construction
```
term + [filter tags]
Example: "cancer[Title] AND 2024[PDAT] AND review[PT]"
```

### Filter Tags
- [AU] - Author
- [TA] - Journal Title Abbreviation
- [PDAT] - Publication Date
- [PT] - Publication Type
