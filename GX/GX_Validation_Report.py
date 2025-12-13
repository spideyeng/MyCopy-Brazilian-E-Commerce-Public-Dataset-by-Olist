# %%
import great_expectations as gx
from datetime import datetime,timedelta, timezone
import os
import sys
print(f"Great Expectations Version: {gx.__version__}")


# %%
# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ID = "durable-ripsaw-477914-g0"
DATASET =  "ecommerce"
CONNECTION_STRING = f"bigquery://{PROJECT_ID}/{DATASET}"
CREDENTIALS_PATH = "/path/to/credentials.json"

# %%
# ============================================================================
# SETUP GREAT EXPECTATIONS
# ============================================================================


"""Initialize GX context and datasource"""
context = context = gx.get_context(mode="file", project_root_dir=".")

datasource = context.data_sources.add_or_update_sql(
    name="bq_ds",
    connection_string=CONNECTION_STRING
    #kwargs={"credentials_path": CREDENTIALS_PATH}
)

# %%
#DATA COMPLETENESS PARAMETERS
MIN_TOTAL=100

#DATA FRESHNESS PARAMETERS
MAX_DATE =    datetime(2018, 9, 3)
MIN_DATE = MAX_DATE - timedelta(days=365*5)
FRESHNESS_DAY = 7
brazilian_states = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    
    

# %%
def fact_db_order_items_validation_asset():
    
    try:
        datasource.delete_asset("fact_db_order_items")
    except:
        pass
    fact_db_order_items_validation_asset = datasource.add_table_asset(
        name="fact_db_order_items",
        table_name="fact_db_order_items", 
        schema_name=DATASET
    )

    try:
        context.suites.delete("fact_db_order_items_validation")
    except:
        pass    
    suite_name = gx.ExpectationSuite(name="fact_db_order_items_validation")
        
    # Check Data Volume
    suite_name.add_expectation(
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=MIN_TOTAL)    
    )

    # Data freshness 
    suite_name.add_expectation(
        gx.expectations.ExpectColumnMaxToBeBetween(
            column="order_date_key", min_value=MAX_DATE - timedelta(days=FRESHNESS_DAY)  , max_value=MAX_DATE)
            
    )

    # Data freshness 
    suite_name.add_expectation(
        gx.expectations.ExpectColumnMaxToBeBetween(
            column="order_date_key", min_value=MIN_DATE  , max_value=MAX_DATE)
            
    )
    """
    suite_name.add_expectation(
        gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB( 
            column_A="order_delivered_customer_date",
            column_B="order_purchase_timestamp" 

        )
    )   

    # Valid Brazilian States
    suite_name.add_expectation(
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="customer_state", value_set=brazilian_states
        )    
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="seller_state", value_set=brazilian_states
        )    
    )
    """


    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="order_date_key",
            mostly=0.8  # At least 80% should have order date
            
        )
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="price", min_value=0.50,mostly=0.9
        )
    )
    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="freight_value", min_value=1.0,mostly=0.9
        )
    )
    
    suite_name.add_expectation(
        gx.expectations.ExpectColumnQuantileValuesToBeBetween(
            column="gross_order_item_value",
            quantile_ranges={
                "quantiles": [0.25, 0.5, 0.75, 0.95],
                "value_ranges": [
                    [10, 100],      # 25th percentile: $10-$100
                    [50, 200],      # 50th percentile: $50-$200
                    [100, 400],     # 75th percentile: $100-$400
                    [200, 1000]     # 95th percentile: $200-$1000
                ]
            }
        )
    )
    context.suites.add(suite_name)

# %%
def fact_customer_validation_asset():
    
    try:
        datasource.delete_asset("fact_customer")
    except:
        pass    
    fact_customer_validation_asset = datasource.add_table_asset(
        name="fact_customer",
        table_name="fact_customer", 
        schema_name=DATASET
    )

    try:
        context.suites.delete("fact_customer_validation")
    except:
        pass
    
    suite_name = gx.ExpectationSuite(name="fact_customer_validation")
    


    # Check Data Volume
    suite_name.add_expectation(
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=MIN_TOTAL)    
    )

    """
    # Data freshness 
    suite_name.add_expectation(
        gx.expectations.ExpectColumnMaxToBeBetween(
            column="order_purchase_timestamp", min_value=MAX_DATE - timedelta(days=FRESHNESS_DAY)  , max_value=MAX_DATE)
            
    )
    """
    suite_name.add_expectation(
        gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB( 
            column_A="last_purchase_timestamp",
            column_B="first_purchase_timestamp" ,
            or_equal=True

        )
    )   

    # Valid Brazilian States
    suite_name.add_expectation(
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="customer_state", value_set=brazilian_states
        )    
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="total_orders", min_value=1,mostly=0.9
        )
    )
    
    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="pct_multiple_sellers", min_value=0.0,max_value=1.0
        )
    )
    
    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="pct_credit_card", min_value=0.0,max_value=1.0
        )
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="pct_debit_card", min_value=0.0,max_value=1.0
        )
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="pct_voucher", min_value=0.0,max_value=1.0
        )
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="pct_boleto", min_value=0.0,max_value=1.0
        )
    )
    
    

        
    


    context.suites.add(suite_name)

# %%
def dim_db_customers_validation_asset():
    
    try:
        datasource.delete_asset("dim_db_customers")
    except:
        pass
    
    dim_db_customers_validation_asset = datasource.add_table_asset(
        name="dim_db_customers",
        table_name="dim_db_customers", 
        schema_name=DATASET
    )

    try:
        context.suites.delete("dim_db_customers_validation")
    except:
        pass
    suite_name = gx.ExpectationSuite(name="dim_db_customers_validation")


    # Check Data Volume
    suite_name.add_expectation(
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=MIN_TOTAL)    
    )

    """
    # Data freshness 
    suite_name.add_expectation(
        gx.expectations.ExpectColumnMaxToBeBetween(
            column="order_purchase_timestamp", min_value=MAX_DATE - timedelta(days=FRESHNESS_DAY)  , max_value=MAX_DATE)
            
    )
   
    suite_name.add_expectation(
        gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB( 
            column_A="last_purchase_timestamp",
            column_B="first_purchase_timestamp" ,
            or_equal=True

        )
    )   
    """
    # Valid Brazilian States
    suite_name.add_expectation(
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="customer_state", value_set=brazilian_states
        )    
    )
    """
    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="total_orders", min_value=1,mostly=0.9
        )
    )
    
    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="total_revenue", min_value=1,mostly=0.9
        )
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="avg_order_value", min_value=1,mostly=0.9
        )
    )
    """
    context.suites.add(suite_name)

# %%
def dim_db_products_validation_asset():
    
    try:
        datasource.delete_asset("dim_db_products")
    except:
        pass
    dim_db_products_vvalidation_asset = datasource.add_table_asset(
        name="dim_db_products",
        table_name="dim_db_products", 
        schema_name=DATASET
    )

    try:
        context.suites.delete("dim_db_products_validation")
    except:
        pass    
    suite_name = gx.ExpectationSuite(name="dim_db_products_validation")
        
    # Check Data Volume
    suite_name.add_expectation(
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=MIN_TOTAL)    
    )
    """
    # Data freshness 
    suite_name.add_expectation(
        gx.expectations.ExpectColumnMaxToBeBetween(
            column="order_purchase_timestamp", min_value=MAX_DATE - timedelta(days=FRESHNESS_DAY)  , max_value=MAX_DATE)
            
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB( 
            column_A="order_delivered_customer_date",
            column_B="order_purchase_timestamp" ,
            or_equal=True
        )
    )   
    


    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="total_order_value",
            mostly=0.8  # At least 80% should have delivery date
            
        )
    )
    
    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="product_category_name_english",
            mostly=0.9  # At least 80% should have delivery date
            
        )
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="product_weight_g", min_value=1, max_value=100000
        )
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="product_length_cm", min_value=0.1, max_value=100000,mostly=0.9
        )
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="product_height_cm", min_value=0.1, max_value=100000,mostly=0.9
        )
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="product_width_cm", min_value=0.1, max_value=100000,mostly=0.9
        )
    )
    """
    context.suites.add(suite_name)

# %%
def dim_db_sellers_validation_asset():
    
    try:
        datasource.delete_asset("dim_db_sellers")
    except:
        pass
    
    dim_db_sellers_validation_asset = datasource.add_table_asset(
        name="dim_db_sellers",
        table_name="dim_db_sellers", 
        schema_name=DATASET
    )

    try:
        context.suites.delete("dim_db_sellers_validation")
    except:
        pass
    suite_name = gx.ExpectationSuite(name="dim_db_sellers_validation")


    # Check Data Volume
    suite_name.add_expectation(
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=MIN_TOTAL)    
    )

    """
    # Data freshness 
    suite_name.add_expectation(
        gx.expectations.ExpectColumnMaxToBeBetween(
            column="order_purchase_timestamp", min_value=MAX_DATE - timedelta(days=FRESHNESS_DAY)  , max_value=MAX_DATE)
            
    )
    """

    # Valid Brazilian States
    suite_name.add_expectation(
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="seller_state", value_set=brazilian_states
        )    
    )
    """
    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="num_orders", min_value=0,mostly=0.9
        )
    )
    """
    context.suites.add(suite_name)

# %%
"""
def dim_order_payments_validation_asset():
    
    try:
        datasource.delete_asset("dim_order_payments")
    except:
        pass
    dim_order_payments_validation_asset = datasource.add_table_asset(
        name="dim_order_payments",
        table_name="dim_order_payments", 
        schema_name=DATASET
    )

    try:
        context.suites.delete("dim_order_payments_validation")
    except:
        pass    
    suite_name = gx.ExpectationSuite(name="dim_order_payments_validation")
        
    # Check Data Volume
    suite_name.add_expectation(
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=MIN_TOTAL)    
    )



    suite_name.add_expectation(
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="payment_type_credit_card", value_set=[0,1]
        )    
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="payment_type_debit_card", value_set=[0,1]
        )    
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="payment_type_voucher", value_set=[0,1]
        )    
    )

    suite_name.add_expectation(
        gx.expectations.ExpectColumnDistinctValuesToBeInSet(
            column="payment_type_boleto", value_set=[0,1]
        )    
    )




    suite_name.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="installment_count",
            mostly=0.8  
            
        )
    )

    context.suites.add(suite_name)
"""

# %%
# ============================================
# SCRIPT MODE 1: Setup Mode (Run Once)
# Define expectations and save them
# ============================================
def setup_expectations():
    """
    python validate_data.py --mode setup
    
    Run this ONCE to define and save expectations.
    """
    print("🔧 SETUP MODE: Defining expectations...")

    fact_db_order_items_validation_asset()
    #fact_customer_validation_asset()
    dim_db_customers_validation_asset()
    dim_db_sellers_validation_asset()
    dim_db_products_validation_asset()    
    #dim_order_payments_validation_asset()
    print("✅ Expectations defined and saved!")

# %%
from typing import Dict
import subprocess

def get_windows_unc_path(linux_path: str, distro_name: str) -> str:
    """Converts a WSL (Linux) path into the explicit Windows UNC path format."""
    cleaned_distro = distro_name.strip('/')
    cleaned_path = linux_path.strip('/')
    unc_path = f"\\\\wsl.localhost\\{cleaned_distro}\\{cleaned_path}"
    return unc_path.replace('/', '\\') # Use backslashes for the Windows command

import webbrowser
import os
from pathlib import Path
import platform


def open_file_in_external_browser(linux_path: str):
    """
    Explicitly tells Windows to open the file in the default browser 
    using the 'start' command via cmd.exe.
    """
    # 1. Path existence check (applies to all OSes)
    if not os.path.exists(linux_path):
        print(f"File Not Found: The report file does not exist at '{linux_path}'. Skipping browser launch.")
        return

    # 2. Determine OS and set the appropriate command
    os_name = platform.system()
    command = None
    
    if os_name == "Darwin":  # macOS
        # On macOS, the 'open' command launches the file with its default application.
        # Since it's a local file, the browser will open it directly.
        command = ["open", linux_path]
        print(f"Detected macOS. Using 'open' command.")
        success_message = f"\n✅ Successfully launched report in external browser via 'open': {linux_path}"

    elif os_name == "Windows" or os_name == "Linux":  # Windows (assuming original logic is for WSL on Windows)
        # Re-use your existing logic for Windows/WSL
        # Note: You must ensure 'get_windows_unc_path' is available in your full script.
        try:
            unc_path = get_windows_unc_path(linux_path, 'Ubuntu')  # Adjust distro name as needed
            command = ["cmd.exe", "/c", "start", "", unc_path]
            print(f"Detected Windows/WSL. Using 'cmd.exe start' with UNC path.")
            success_message = f"\n✅ Successfully launched report in external browser via UNC path: {unc_path}"
        except NameError:
             
             
             print("\n❌ Error: get_windows_unc_path is not defined. Cannot launch on Windows.")
             return # Exit if UNC path logic is missing
    else:
        print(f"\n⚠️ Unsupported Operating System: {os_name}. Skipping browser launch.")
        return


    
    # 3. Execute the command
    try:
        # Execute the command determined above
        subprocess.run(command, check=True, text=True, capture_output=True)
        print(success_message)
        
    except FileNotFoundError:
        # This catches errors if the command itself (e.g., 'open', 'xdg-open', 'cmd.exe') isn't found
        print(f"\n❌ Error: The required command '{command[0]}' was not found on your system.")
    except subprocess.CalledProcessError as e:
        # This catches non-zero exit codes from the command
        try:
            command = ["xdg-open", linux_path]
            print(f"Detected Linux. Using 'xdg-open' command.")
            success_message = f"\n✅ Successfully launched report in external browser via 'xdg-open': {linux_path}"

            subprocess.run(command, check=True, text=True, capture_output=True)
            print(success_message)
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error launching browser (Command Failed): {e}")
            print(f"Stdout: {e.stdout.strip()}")
            print(f"Stderr: {e.stderr.strip()}")
    except Exception as e:
        # Catch all other exceptions
        print(f"\n❌ Generic Error launching browser: {e}")

def generate_gx_html_report(run_name):
    # ============================================
    # 9. Open HTML Report
    # ============================================


    # Build data docs
    context.build_data_docs()

    print(f"\n{'='*60}")
    print("GX HTML REPORT LOCATION")
    print(f"{'='*60}")

    data_docs_path = os.path.join(context.root_directory, "uncommitted", "data_docs", "local_site")
    index_path = os.path.join(data_docs_path, "index.html")

    print(f"Main Index: {index_path}")
    print(f"\n💡 The HTML report includes validation results for ALL 3 assets!")
    print(f"   Navigate to 'Validation Results' > '{run_name}' to see all results.")
    print(f"{'='*60}\n")

    print("\nOpen the index.html file in your browser to view the interactive report!")
    open_file_in_external_browser( os.path.abspath(index_path)  )

# %%
# ============================================
# SCRIPT MODE 2: Regular Runs (Run All Checkpoints)
# ============================================
def run_all_validations():
    """
    This uses the ALREADY SAVED expectations - no need to redefine them!
    """
    
    #fact_db_order_items
    batch_def_fact_db_order_items = datasource.get_asset("fact_db_order_items").add_batch_definition_whole_table(
        name=f"b_fact_db_order_items_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ) 

    validation_def_fact_db_order_items = gx.ValidationDefinition(
        name=f"v_fact_db_order_items_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        data=batch_def_fact_db_order_items,
        suite=context.suites.get("fact_db_order_items_validation")
    )
    context.validation_definitions.add(validation_def_fact_db_order_items)  
    
    """
    #fact_customer
    batch_def_fact_customer = datasource.get_asset("fact_customer").add_batch_definition_whole_table(
        name=f"b_fact_customer_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ) 

    validation_def_fact_customer= gx.ValidationDefinition(
        name=f"v_fact_customer_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        data=batch_def_fact_customer,
        suite=context.suites.get("fact_customer_validation")
    )
    context.validation_definitions.add(validation_def_fact_customer) 
    """

    #dim_db_customers
    batch_def_dim_db_customers = datasource.get_asset("dim_db_customers").add_batch_definition_whole_table(
        name=f"b_dim_db_customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ) 

    validation_def_dim_db_customers = gx.ValidationDefinition(
        name=f"v_dim_db_customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        data=batch_def_dim_db_customers,
        suite=context.suites.get("dim_db_customers_validation")
    )
    context.validation_definitions.add(validation_def_dim_db_customers) 

    #dim_db_sellers
    batch_def_dim_db_sellers = datasource.get_asset("dim_db_sellers").add_batch_definition_whole_table(
        name=f"b_dim_db_sellers_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ) 

    validation_def_dim_db_sellers = gx.ValidationDefinition(
        name=f"v_dim_db_sellers_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        data=batch_def_dim_db_sellers,
        suite=context.suites.get("dim_db_sellers_validation")
    )
    context.validation_definitions.add(validation_def_dim_db_sellers) 

    #dim_db_products
    batch_def_dim_db_products = datasource.get_asset("dim_db_products").add_batch_definition_whole_table(
        name=f"b_dim_db_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ) 

    validation_def_dim_db_products = gx.ValidationDefinition(
        name=f"v_dim_db_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        data=batch_def_dim_db_products,
        suite=context.suites.get("dim_db_products_validation")
    )
    context.validation_definitions.add(validation_def_dim_db_products) 
    """
    #dim_order_payments
    batch_def_dim_order_payments = datasource.get_asset("dim_order_payments").add_batch_definition_whole_table(
        name=f"b_dim_order_payments_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ) 

    validation_def_dim_order_payments = gx.ValidationDefinition(
        name=f"v_dim_order_payments_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        data=batch_def_dim_order_payments,
        suite=context.suites.get("dim_order_payments_validation")
    )
    context.validation_definitions.add(validation_def_dim_order_payments) 
    """
    # Create checkpoint
    checkpoint = gx.Checkpoint(
        name=f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        validation_definitions=[validation_def_fact_db_order_items,
                               # validation_def_fact_customer,
                                validation_def_dim_db_customers,
                                validation_def_dim_db_sellers,
                                #validation_def_dim_order_payments
                                validation_def_dim_db_products
                                
                                ],
        result_format={"result_format": "COMPLETE"}
    )
    context.checkpoints.add(checkpoint)
    
    print("\n🔍 Running multi-asset validation via Checkpoint...")
    # Run validation - uses the saved expectations
    run_name = f"validation_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_id = gx.RunIdentifier(run_name=run_name)
    
    checkpoint_result = checkpoint.run(run_id=run_id)
    
    print(f"\n{'='*60}")
    print("MULTI-ASSET VALIDATION RESULTS")
    print(f"{'='*60}")
    print(f"Overall Success: {checkpoint_result.success}")
    print(f"Number of assets validated: {len(checkpoint_result.run_results)}")

    # Show results for each asset
    for idx, (result_id, validation_result) in enumerate(checkpoint_result.run_results.items(), 1):
        # Extract asset name from result_id (after the last '/')
        asset_name = str(result_id).split('/')[-1] if '/' in str(result_id) else "Unknown"
        
        suite_name = validation_result.suite_name
        total = len(validation_result.results)
        passed = sum(1 for r in validation_result.results if r.success)
        failed = total - passed
        
        print(f"\n📊 Asset {idx}: {asset_name}")
        print(f"   Suite: {suite_name}")
        print(f"   Total Expectations: {total}")
        print(f"   ✅ Passed: {passed}")
        print(f"   ❌ Failed: {failed}")
        
        # Show failed expectations if any
        if failed > 0:
            print(f"   \n   Failed Expectations:")
            for result in validation_result.results:
                if not result.success:
                    
                    #expectation_context = result.expectation_config.expectation_context
                    column = result.expectation_config.kwargs.get('column', 'N/A')
                    #print(f"      ❌ {expectation_context.e} on column '{column}'")


    print(f"✅ Checkpoint completed with run_name: {run_name}")
    print(f"   Overall Success: {checkpoint_result.success}")

    generate_gx_html_report(run_name)

    return checkpoint_result

# %%
# ============================================
# SCRIPT MODE 3: Full Mode (Setup + Validate)
# For CI/CD or when you want to ensure fresh setup
# ============================================
def full_run():
    """
    python validate_data.py --mode full
    
    Run this when you want to redefine expectations AND validate.
    Useful for CI/CD pipelines or testing.
    """
    print("🔄 FULL MODE: Setting up expectations and running validation...\n")
    
    setup_expectations()
    print()
    success = run_all_validations()
    
    return success

# %%
# ============================================
# Main Script Entry Point
# ============================================
if __name__ == "__main__":
    
    try:
        success = full_run()
        sys.exit(0 if success else 1)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)



