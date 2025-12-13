import subprocess
import sys

def test_dbt_fact():
    """
    Run dbt tests for all fact models under marts/fact
    """
    try:
        result = subprocess.run(
            ["dbt", "test", "--select", "path:marts/fact"],
            check=True,
            text=True
        )
        print("✅ dbt test (fact) completed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ dbt test (fact) failed.")
        print(f"Exit code: {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    print("▶ Testing dbt fact models: path:marts/fact ...")
    test_dbt_fact()
