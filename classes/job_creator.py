from operator import attrgetter
import traceback
from flask import current_app
import requests
from utility.constant import Constant
from utility.error import ThrowError
from utility.payload.job_payload import JobPayload
from utility.request import Request


class JobCreator:
    def __init__(self, request_id, payload):
        self.request_id = request_id
        self.payload = payload
        self.dao_request = Request(logger=current_app.logger)

    def create_job(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- CREATE_JOB_PAYLOAD: {self.payload}")

            # Use job_name to get job tasks
            job_name = self.payload["job_name"]
            task_list = self.get_job_tasks(job_name)

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- JOB_TASKS: {task_list}")

            if not task_list:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- JOB_TASKS_NOT_FOUND")
                raise Exception("Job tasks not found", 404)

            # Form the payload
            # Insert the job into the database
            insert_job_response = self.dao_request.insert(self.request_id, "jobs", JobPayload.form_insert_job_payload({
                "payload": self.payload,
                "job_name": job_name,
                "tasks": sorted(task_list, key=lambda task: task["order_index"]),
                "user_id": self.payload["user_id"]
            }))

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- INSERT_JOB_RESPONSE: {insert_job_response}")
            
            # Respond with the job ID
            return {"status": "SUCCESS", "job_id":insert_job_response["response"]["job_id"]}


        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            raise ThrowError(str(e), 500)
        
    
    def get_job_tasks(self, job_name):
        # Get job tasks from the database
        job_tasks = self.dao_request.read_list(self.request_id, "job_tasks", {"job_name": job_name, "is_active": 1})
        return job_tasks["response"]
