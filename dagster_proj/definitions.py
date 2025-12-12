# definitions.py
from dagster import Definitions
from dagster_proj.jobs.dagster_elt_pipeline import elt_pipeline_job

defs = Definitions(
    jobs=[elt_pipeline_job]
)
