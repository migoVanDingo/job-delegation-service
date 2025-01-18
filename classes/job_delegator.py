from concurrent.futures import ThreadPoolExecutor
from operator import attrgetter
import traceback
from flask import  json
import requests
from utility.constant import Constant
from utility.error import ThrowError
from utility.jobs import Jobs
from utility.request import Request


class JobDelegator:
    def __init__(self, app):
        self.app = app


    def run(self):
        try:
            # Explicitly push the app context
            with self.app.app_context():
                with ThreadPoolExecutor(max_workers=Constant.max_threads) as executor:
                    if executor._work_queue.qsize() > Constant.max_threads:
                        self.app.logger.info(
                            f"MAX THREADS REACHED, SKIPPING CYCLE: {executor._work_queue.qsize()}"
                        )
                        return

                    jobs = self.fetch_pending_jobs()
                    if jobs and len(jobs) > 0:
                        for job in jobs:
                            executor.submit(self.delegate_job, job)


        except Exception as e:
            self.app.logger.error(f"TRACE: {traceback.format_exc()} ---- JOB_DELEGATOR_ERROR: {str(e)}")
            raise ThrowError("Failed to delegate jobs", 500)

    def fetch_pending_jobs(self):
        try:
            dao_request = Request()
            pending_jobs = dao_request.query("FETCHING_JOBS",
                "SELECT * FROM jobs WHERE status = 'PENDING' ORDER BY priority DESC, created_at ASC"
            )
            self.app.logger.info(f"FETCH_PENDING_JOBS: {pending_jobs}")
            if pending_jobs and "response" in pending_jobs:
                return pending_jobs["response"]
            else:
                return []
        except Exception as e:
            self.app.logger.error(f"TRACE: {traceback.format_exc()} ---- FETCH_PENDING_JOBS_ERROR: {str(e)}")
            raise ThrowError("Failed to fetch pending jobs", 500)
        
    def delegate_job(self, job):
        try:
            job_id = job["job_id"]
            job_name = job["job_name"]
            job_payload = json.loads(job["data"])
            job_payload["request_id"] = job_id
            job_payload["job_id"] = job_id

            self.app.logger.info(f"JOB_ID: {job_id} --- STARTING_JOB: {job_name}")
            
            dao_request = Request()
            task_list = sorted(dao_request.read_list(job_id, "job_tasks", {"job_name": job_name}), key=attrgetter("order_index"))

            # Update Job status to IN_PROGRESS
            dao_request.update(job_id, "jobs", "job_id", job_id, {"status": "IN_PROGRESS"})
        

            for task in task_list:
                self.app.logger.info(f"JOB_ID: {job_id} --- STARTING_TASK: {task['task_name']}")
                port = Constant.services[task["service"]]["PORT"]
                endpoint = Constant.services[task["service"]]["ENDPOINT"][task["task_name"]]

                url = Constant.base_url + port + endpoint
                response = requests.post(url, headers={"Content-type": "application/json"}, json=job_payload)

                response = response.json()

                if "status" not in response:
                    raise Exception(f"JOB_ID: {job_id} --- Task failed --- TASK_NAME: {task['task_name']} --- STATUS: FAILED --- ERROR: {response.text}")
                
                elif response["status"] == "FAILED":
                    raise Exception(f"Task failed: {task['task_name']} --- {job_id} --- STATUS: {response['status']} --- ERROR: {response['message']}")
                
                

                # Update the job payload
                dao_request.update(job_id, "jobs", "job_id", job_id, {"data": response['data']})

                self.app.logger.info(f"JOB_ID: {job_id} --- COMPLETED_TASK: {task['task_name']}")



            # Update Job status to COMPLETED
            dao_request.update(job_id, "jobs", "job_id", job_id, {"status": "COMPLETED"})
            self.app.logger.info(f"JOB_ID: {job_id} --- COMPLETED_JOB: {job_name}")

        except Exception as e:
            # If job fails, update the status as FAILED and error_message as the exception message
            self.app.logger.error(f"JOB_ID: {job_id} --- {traceback.format_exc()} --- DELEGATE_JOB_ERROR: {str(e)}")
            dao_request.update(job_id, "jobs", "job_id", job_id, {"status": "PENDING", "error_message": str(e), "retries": job["retries"] + 1, "priority": job["priority"] + 1})

