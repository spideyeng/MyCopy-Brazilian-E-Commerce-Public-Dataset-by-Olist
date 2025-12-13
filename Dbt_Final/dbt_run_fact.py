import subprocess
import sys

def run_dbt_fact():
    """
    Run all fact models under marts/fact
    """
    try:
        result = subprocess.run(
            ["dbt", "run", "--select", "path:marts/fact"],
            check=True,
            text=True
        )
        print("✅ dbt run (fact) completed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ dbt run (fact) failed.")
        print(f"Exit code: {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    print("▶ Running dbt fact models: path:marts/fact ...")
    run_dbt_fact()
