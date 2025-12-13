import subprocess
import sys

def test_dbt_dim():
    """
    Run dbt tests for all dimension models under marts/dim
    """
    try:
        result = subprocess.run(
            ["dbt", "test", "--select", "path:marts/dim"],
            check=True,
            text=True
        )
        print("✅ dbt test (dim) completed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ dbt test (dim) failed.")
        print(f"Exit code: {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    print("▶ Testing dbt dimension models: path:marts/dim ...")
    test_dbt_dim()

