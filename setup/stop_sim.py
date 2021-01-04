import json
import botocore
import boto3
import os
import sys

# To run locally on your machine based on CFN stack outputs.
if __name__ == "__main__":

  sim_job_path = ".simulation_jobs"

  # check if we have run jobs
  try:
    with open(sim_job_path) as json_file:
      robomaker = boto3.client('robomaker')
      json_str = json.load(json_file)
      jobs = json.loads(json_str)

      try:
        print("Cancel simulation job")
        print(jobs['simulation_job'])
        if jobs['simulation_job'] is not None:
          robomaker.cancel_simulation_job(job=jobs['simulation_job'])
      except Exception as e:
        print(e)    
      
      try:
        print("Cancel simulation batch job")
        print(jobs['simulation_batch'] )
        if jobs['simulation_batch'] is not None:
          robomaker.cancel_simulation_job_batch(batch=jobs['simulation_batch'])
      except Exception as e:
        print(e)    
  except Exception as e:
    print(e)