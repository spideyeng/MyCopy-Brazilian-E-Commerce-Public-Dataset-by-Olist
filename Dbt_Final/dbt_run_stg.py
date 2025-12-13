import subprocess
import sys

def run_dbt_stg():
    """
    Run all staging models (stg_db_*)
    """
    try:
        result = subprocess.run(
            ["dbt", "run", "--select", "stg_db_*"],
            check=True,
            text=True
        )
        print("✅ dbt run (staging) completed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ dbt run (staging) failed.")
        print(f"Exit code: {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    print("▶ Running dbt staging models: stg_db_* ...")
    run_dbt_stg()
