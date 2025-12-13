import subprocess
import sys

def test_dbt_stg():
    """
    Run dbt tests for all staging models (stg_db_*)
    """
    try:
        result = subprocess.run(
            ["dbt", "test", "--select", "stg_db_*"],
            check=True,
            text=True
        )
        print("✅ dbt test (staging) completed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ dbt test (staging) failed.")
        print(f"Exit code: {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    print("▶ Testing dbt staging models: stg_db_* ...")
    test_dbt_stg()
