import subprocess
import sys

def run_dbt_dim():
    """
    Run all dimension models under marts/dim
    """
    try:
        result = subprocess.run(
            ["dbt", "run", "--select", "path:marts/dim"],
            check=True,
            text=True
        )
        print("✅ dbt run (dim) completed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ dbt run (dim) failed.")
        print(f"Exit code: {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    print("▶ Running dbt dimension models: path:marts/dim ...")
    run_dbt_dim()
