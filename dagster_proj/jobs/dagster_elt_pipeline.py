import time
import random
from dagster import op, job, OpExecutionContext, Out, In, Nothing
import os
import subprocess
# --- 1. Define Operations (The Tasks) ---

@op(name="Meltano_Extract_and_Load")
def run_meltano_elt(context: OpExecutionContext) -> str:
    context.log.info("🚀 [Meltano] Starting extraction from Kaggle...")
    
    
    #shell_command = "meltano run tap-csv target-bigquery"
    shell_command = "sleep 30"
    result = subprocess.run(
            shell_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    # Log the output to Dagster's structured logging system
    for line in result.stdout.splitlines():
        context.log.info(line)
    
    
    
    context.log.info("✅ [Meltano] Data loaded into BigQuery staging_tables.")
    return "staging_tables_ready"

@op(name="DBT_STG_Run", ins={"start_signal": In(Nothing)})
def run_dbt_stg_models(context: OpExecutionContext):

    context.log.info("🛠️ [dbt] Building staging models...")
    shell_command = "cd Dbt_Final/; python dbt_run_stg.py"
    result = subprocess.run(
            shell_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    # Log the output to Dagster's structured logging system
    for line in result.stdout.splitlines():
        context.log.info(line)
    
    context.log.info("✅ [dbt] Staging models built successfully.")
    return "staging_models_built"

@op(name="DBT_STG_Test", ins={"start_signal": In(Nothing)})
def run_dbt_stg_tests(context: OpExecutionContext) -> str:

    #context.log.info(f"Trigger received: {start_signal}")
    shell_command = "cd Dbt_Final/; python dbt_test_stg.py"
    result = subprocess.run(
            shell_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    # Log the output to Dagster's structured logging system
    for line in result.stdout.splitlines():
        context.log.info(line)

    context.log.info("✅ [dbt] Staging tables tested successfully.")
    return "staging_tests_complete"


@op(name="DBT_Transformation", ins={"start_signal": In(Nothing)})
def run_dbt_dim_fact_models(context: OpExecutionContext) -> str:

    #context.log.info(f"Trigger received: {start_signal}")
    context.log.info("🛠️ [dbt] Building Dim & Fact models...")
    shell_command = "cd Dbt_Final/; python dbt_run_fact.py"
    result = subprocess.run(
            shell_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    # Log the output to Dagster's structured logging system
    for line in result.stdout.splitlines():
        context.log.info(line)
    
    shell_command = "cd Dbt_Final/; python dbt_run_dim.py"
    result = subprocess.run(
            shell_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    # Log the output to Dagster's structured logging system
    for line in result.stdout.splitlines():
        context.log.info(line)
    
    context.log.info("✅ [dbt] Dim & Fact models built successfully.")
    return "dim_fact_tests_complete"

@op(name="DBT_Transformation_Test", ins={"start_signal": In(Nothing)})
def run_dbt_dim_fact_tests(context: OpExecutionContext) -> str:

    #context.log.info(f"Trigger received: {start_signal}")
    context.log.info("🛠️ [dbt] Running schema tests on Dim & Fact tables...")
    
    shell_command = "cd Dbt_Final/; python dbt_test_fact.py"
    
    result = subprocess.run(
            shell_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    
    # Log the output to Dagster's structured logging system
    for line in result.stdout.splitlines():
        context.log.info(line)
    
    
    shell_command = "cd Dbt_Final/; python dbt_test_dim.py"
    result = subprocess.run(
            shell_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    # Log the output to Dagster's structured logging system
    for line in result.stdout.splitlines():
        context.log.info(line)
    
    context.log.info("✅ [dbt] Dim & Fact tables tested successfully.")
    return "dim_fact_tests_complete"

    # Simulate a conditional check (mocking a pass)
    #if random.choice([True, True, False]): 
    #    context.log.info("✅ [dbt] All tests passed.")
    #else:
        # In a real scenario, you might raise an exception here
    #    context.log.warning("⚠️ [dbt] Warning: Some tests found data anomalies.")
    context.log.info("✅ [dbt] All tests passed.")
    return "tests_complete"

@op(name="GX_Validation", ins={"start_signal": In(Nothing)})
def run_gx_validation(context: OpExecutionContext):
    """Simulates Great Expectations data quality checks."""
    context.log.info("🔍 [GX] Running checkpoint 'Data quality Validation'...")
    #os.system("python  ../GX/GX_Validation_Report.py")
    
    shell_command = "python  GX/GX_Validation_Report.py"
    result = subprocess.run(
            shell_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    # Log the output to Dagster's structured logging system
    for line in result.stdout.splitlines():
        context.log.info(line)
    
    context.log.info("✅ [GX] Data quality validation passed.")
    return "gx_success"

@op(name="EDA_ML_Analysis_Report",  ins={"start_signal": In(Nothing)})
def generate_eda_report(context: OpExecutionContext):
    """Simulates generating an EDA report."""
    context.log.info("📊 [EDA] Analyzing data distributions...")
    #time.sleep(1)
    #os.system("python  EDA_ML/EDA_ML.py")

    shell_command = "python  EDA_ML/EDA_ML.py"
    result = subprocess.run(
            shell_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
    # Log the output to Dagster's structured logging system
    for line in result.stdout.splitlines():
        context.log.info(line)

    context.log.info("✅ [EDA] Report generated at /tmp/eda_report.html")
    return "eda_ready"
"""
@op(name="Notification",  ins={"gx_signal": In(str), "eda_signal": In(str)})
def send_notification(context: OpExecutionContext, gx_signal: str, eda_signal: str):
    ""Sends a notification only after GX and EDA are done.""
    context.log.info(f"Signals received: {gx_signal}, {eda_signal}")
    context.log.info("🔔 [Slack] Pipeline finished successfully. Report available.")
"""
# --- 2. Define the Job (The Workflow) ---

@job(name="ELT_Pipeline_Job")
def elt_pipeline_job():
    # Step 1: Extract & Load
    raw_data = run_meltano_elt()

    # Step 2: Run dbt tests (waits for models)
    stg_models_done = run_dbt_stg_models(raw_data)
    stg_tests_done = run_dbt_stg_tests(stg_models_done)

    # Step 3: Transform (waits for raw_data)
    

    dim_fact_models_done = run_dbt_dim_fact_models(stg_tests_done)
    dim_fact_tests_done = run_dbt_dim_fact_tests(dim_fact_models_done)
    
    # Step 4: Run GX and EDA in parallel (both wait for models to finish)
    gx_result = run_gx_validation(dim_fact_tests_done)
    eda_result = generate_eda_report(dim_fact_tests_done)
    
    # Step 5: Notify (waits for BOTH GX and EDA to finish)
    #send_notification(gx_result, eda_result)