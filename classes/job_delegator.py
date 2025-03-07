from concurrent.futures import ThreadPoolExecutor
import logging
from operator import attrgetter
import os
import sys
import time
import traceback
from flask import  json
import requests

# Add the root directory to the module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from utility.constant import Constant
from utility.error import ThrowError
from utility.jobs import Jobs
from utility.request import Request
from utility.utils import Utils


class JobDelegator:
    def __init__(self):
        self.logger = logging.getLogger("job_delegator")

    def run(self):
        try:
            # Explicitly push the app context
        
                # with ThreadPoolExecutor(max_workers=Constant.max_threads) as executor:

                    # Check if all threads are busy
                    # if executor._work_queue.qsize() > Constant.max_threads:
                    #     logging.info(
                    #         f"MAX THREADS REACHED, SKIPPING CYCLE: {executor._work_queue.qsize()}"
                    #     )
                    #     return
                while True:
                    jobs = self.fetch_pending_jobs()
                    if jobs and len(jobs) > 0:
                        self.logger.info(f"===============> PROCESSING NEW JOBS: {jobs}")
                        for job in jobs:
                            if not self.delegate_job(job):
                                self.logger.info(f"JOB_ID: {job['job_id']} --- JOB_FAILED: {job['job_name']} --- LAST_STAGE: {job['last_stage_completed']} --- RETRIES: {job['retries']}")

                                if job["retries"] >= Constant.max_retries:
                                    self.logger.info(f"JOB_ID: {job['job_id']} --- JOB_FAILED: {job['job_name']} --- MAX_RETRIES_REACHED")
                                    dao_request = Request(logger=self.logger)
                                    dao_request.update(job["job_id"], "jobs", "job_id", job["job_id"], {"status": "FAILED"})
                                    continue
                                break
                            # executor.submit(self.delegate_job, job)
                    time.sleep(5)

                 
        except Exception as e:
            logging.error(f"TRACE: {traceback.format_exc()} ---- JOB_DELEGATOR_ERROR: {str(e)}")
            raise ThrowError("Failed to delegate jobs", 500)

    def fetch_pending_jobs(self):
        try:
            dao_request = Request(logger=self.logger)
            pending_jobs = dao_request.query("FETCHING_JOBS",
                "SELECT * FROM jobs WHERE status = 'PENDING' ORDER BY priority DESC, created_at ASC"
            )
            
            if pending_jobs and "response" in pending_jobs:
                return pending_jobs["response"]
            else:
                return []
        except Exception as e:
            logging.error(f"TRACE: {traceback.format_exc()} ---- FETCH_PENDING_JOBS_ERROR: {str(e)}")
            raise ThrowError("Failed to fetch pending jobs", 500)
        
    def delegate_job(self, job):
        try:
            job_id = job["job_id"]

            dao_request = Request(logger=self.logger)
            dao_request.update(job_id, "jobs", "job_id", job_id, {"status": "IN_PROGRESS"})

            job_name = job["job_name"]
            job_payload = json.loads(job["data"])
            job_payload["request_id"] = job_id
            job_payload["job_id"] = job_id

            # task_list_response = dao_request.read_list(job_id, "job_tasks", {"job_name": job_name})
            task_list = json.loads(job["tasks"])
            task_list = sorted(task_list, key=lambda task: task["order_index"])

            logging.info(f"JOB_ID: {job_id} --- TASK_LIST_ORDERED: {task_list}")
            
            # Update Job status to IN_PROGRESS
            
        

            for task in task_list:
                logging.info(f"JOB_ID: {job_id} --- STARTING_TASK: {task}")
                port = Constant.services[task["service"]]["PORT"]
                endpoint = Constant.services[task["service"]]["ENDPOINT"][task["task_name"]]

                url = Constant.base_url + port + endpoint
                response = requests.post(url, headers={"Content-type": "application/json"}, json=job_payload)

                # if response.status_code == 500:
                #     raise Exception(f"JOB_ID: {job_id} --- TASK_FAILED: {task['task_name']} --- STATUS: {response.status_code} --- ERROR: {response.text}")
                response = response.json()
                logging.info(f"JOB_ID: {job_id} --- TASK: {task} --- TASK_RESPONSE: {response}")
                

                if "status" not in response or "data" not in response:
                    raise Exception(f"JOB_ID: {job_id} --- Task failed --- TASK_NAME: {task['task_name']} --- STATUS: FAILED --- ERROR: {response}")
                
                if response["status"] != "SUCCESS":
                    raise Exception(f"Task failed: {task['task_name']} --- {job_id} --- STATUS: {response['status']} --- ERROR: {response['message']}")
                
                job_payload = response["data"]
                
                # Remove current task from task list
                task_list = [t for t in task_list if t["task_name"] != task["task_name"]]
                task_list = sorted(task_list, key=lambda task: task["order_index"])
                
                # Update the job payload
                dao_request.update(job_id, "jobs", "job_id", job_id, {"data": json.dumps(job_payload), "last_stage_completed": task["task_name"], "tasks": json.dumps(task_list)})

                logging.info(f"JOB_ID: {job_id} --- COMPLETED_TASK: {task['task_name']}")



            # Update Job status to COMPLETED
            dao_request.update(job_id, "jobs", "job_id", job_id, {"status": "COMPLETED"})
            logging.info(f"JOB_ID: {job_id} --- COMPLETED_JOB: {job_name}")
            return True
        except Exception as e:
            # If job fails, update the status as FAILED and error_message as the exception message
            logging.error(f"JOB_ID: {job_id} --- {traceback.format_exc()} --- DELEGATE_JOB_ERROR: {str(e)}")
            dao_request.update(job_id, "jobs", "job_id", job_id, {"status": "PENDING", "error_message": str(e), "retries": job["retries"] + 1, "priority": job["priority"] + 1})
            return False

if __name__ == "__main__":
    Utils.setup_logging()
    logging.info("================  Starting Job Delegator  ================")
    job_delegator = JobDelegator()
    job_delegator.run()