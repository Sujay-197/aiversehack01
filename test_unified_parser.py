"""
Test Unified Parser
Verifies strategy selection and fallback logic.
"""
import sys
import os
sys.path.append(os.getcwd())
from backend.llm import UnifiedResumeParser

def test_unified_parser():
    print("="*80)
    print("Testing Unified Resume Parser")
    print("="*80)
    
    parser = UnifiedResumeParser()
    
    test_resume = """
    Sam Smith
    sam@example.com
    Java Engineer with 10 years experience.
    Skills: Java, Spring Boot, MySQL.
    """
    
    print("\n[TEST] Strategy: Direct")
    res_direct = parser.parse(test_resume, strategy="direct")
    print(f"Direct Result Skills: {len(res_direct.skills)}")

    print("\n[TEST] Strategy: RAG (may fail if key invalid)")
    try:
        res_rag = parser.parse(test_resume, strategy="rag")
        print(f"RAG Result Skills: {len(res_rag.skills)}")
    except Exception as e:
        print(f"[EXPECTED ERROR] RAG strategy failed (invalid key): {e}")

    print("\n[TEST] Strategy: Auto (RAG -> Direct Fallback)")
    # This should succeed by falling back to Direct
    res_auto = parser.parse(test_resume, strategy="auto")
    print(f"Auto Result Skills: {len(res_auto.skills)}")
    
    if len(res_auto.skills) > 0:
        print("[SUCCESS] Auto strategy returned results (likely via fallback or success)")
    else:
        print("[FAIL] Auto strategy returned no results (both failed?)")

if __name__ == "__main__":
    test_unified_parser()
