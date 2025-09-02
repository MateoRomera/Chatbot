"""
test_loader.py
--------------
Quick test script to validate multi-source data loading.
"""

from backend.data_loader import (
    DATA_DIR,
    load_csv,
    load_json,
    load_xlsx,
    load_sqlite,
    load_postgres,
    row_to_text,
    load_all_data,
)

def main():
    print("🔍 Testing data loading from /data ...\n")

    records = load_all_data()
    print(f"\n✅ Total registros cargados: {len(records)}\n")

    print("--- Formatted sample (row_to_text) ---")
    for i, rec in enumerate(records[:5]):
        print(f"{i+1}. {rec}")

if __name__ == "__main__":
    main()
