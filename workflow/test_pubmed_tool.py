"""
Test script for PubMed Search Tool

This script tests all the filtering capabilities of the PubMed search tool.
"""

import sys
import time
sys.path.insert(0, '/app/sandbox/session_20260129_164406_e8f5692b459a/results')

from pubmed_search_tool import Tools

# Delay between tests to avoid rate limiting
TEST_DELAY = 1.5

def test_basic_search():
    """Test basic keyword search."""
    print("\n" + "=" * 60)
    print("TEST 1: Basic Keyword Search")
    print("=" * 60)

    tool = Tools()
    result = tool.search_pubmed(
        query="machine learning cancer diagnosis",
        max_results=3
    )
    print(result[:2000] + "..." if len(result) > 2000 else result)

    assert "PubMed Search Results" in result
    assert "PMID" in result or "No articles found" in result
    print("\n[PASS] Basic search completed successfully")
    return True


def test_date_filter():
    """Test date range filtering."""
    print("\n" + "=" * 60)
    print("TEST 2: Date Range Filter (2024 only)")
    print("=" * 60)

    tool = Tools()
    result = tool.search_pubmed(
        query="COVID-19 vaccine",
        max_results=3,
        date_from="2024",
        date_to="2024"
    )
    print(result[:2000] + "..." if len(result) > 2000 else result)

    assert "PubMed Search Results" in result
    print("\n[PASS] Date filter completed successfully")
    return True


def test_author_filter():
    """Test author filtering."""
    print("\n" + "=" * 60)
    print("TEST 3: Author Filter")
    print("=" * 60)

    tool = Tools()
    result = tool.search_pubmed(
        query="CRISPR",
        max_results=3,
        author="Doudna"
    )
    print(result[:2000] + "..." if len(result) > 2000 else result)

    assert "PubMed Search Results" in result
    print("\n[PASS] Author filter completed successfully")
    return True


def test_journal_filter():
    """Test journal filtering."""
    print("\n" + "=" * 60)
    print("TEST 4: Journal Filter (Nature)")
    print("=" * 60)

    tool = Tools()
    result = tool.search_pubmed(
        query="immunotherapy",
        max_results=3,
        journal="Nature"
    )
    print(result[:2000] + "..." if len(result) > 2000 else result)

    assert "PubMed Search Results" in result
    print("\n[PASS] Journal filter completed successfully")
    return True


def test_publication_type_filter():
    """Test publication type filtering."""
    print("\n" + "=" * 60)
    print("TEST 5: Publication Type Filter (Review)")
    print("=" * 60)

    tool = Tools()
    result = tool.search_pubmed(
        query="diabetes treatment",
        max_results=3,
        publication_type="Review"
    )
    print(result[:2000] + "..." if len(result) > 2000 else result)

    assert "PubMed Search Results" in result
    print("\n[PASS] Publication type filter completed successfully")
    return True


def test_combined_filters():
    """Test multiple filters combined."""
    print("\n" + "=" * 60)
    print("TEST 6: Combined Filters (Date + Type + Journal)")
    print("=" * 60)

    tool = Tools()
    result = tool.search_pubmed(
        query="Alzheimer",
        max_results=5,
        date_from="2023",
        publication_type="Review",
        journal="Lancet"
    )
    print(result[:3000] + "..." if len(result) > 3000 else result)

    assert "PubMed Search Results" in result
    print("\n[PASS] Combined filters completed successfully")
    return True


def test_abstract_retrieval():
    """Verify abstracts are included in results."""
    print("\n" + "=" * 60)
    print("TEST 7: Abstract Retrieval Verification")
    print("=" * 60)

    tool = Tools()
    result = tool.search_pubmed(
        query="heart failure treatment",
        max_results=2
    )
    print(result[:3000] + "..." if len(result) > 3000 else result)

    # Check that Abstract section exists
    if "No articles found" not in result:
        assert "**Abstract**" in result, "Abstract section not found in results"
        print("\n[PASS] Abstracts are included in results")
    else:
        print("\n[SKIP] No results to verify abstracts")
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("PubMed Search Tool - Test Suite")
    print("=" * 60)

    tests = [
        test_basic_search,
        test_date_filter,
        test_author_filter,
        test_journal_filter,
        test_publication_type_filter,
        test_combined_filters,
        test_abstract_retrieval,
    ]

    passed = 0
    failed = 0

    for i, test in enumerate(tests):
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n[FAIL] {test.__name__}: {str(e)}")
            failed += 1

        # Add delay between tests to avoid rate limiting
        if i < len(tests) - 1:
            print(f"\n[INFO] Waiting {TEST_DELAY}s to avoid rate limiting...")
            time.sleep(TEST_DELAY)

    print("\n" + "=" * 60)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
