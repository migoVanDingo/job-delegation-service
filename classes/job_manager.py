import traceback
from flask import current_app
import requests
from utility.constant import Constant
from utility.error import ThrowError
from utility.payload.job_payload import JobPayload
from utility.request import Request


class JobManager:
    def __init__(self, request_id, payload):
        self.request_id = request_id
        self.payload = payload
        self.dao_request = Request()

    def create_job(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- CREATE_JOB_PAYLOAD: {self.payload}")

            # Use job_name to get job tasks
            job_name = self.payload.get("job_name")
            job_tasks = self.get_job_tasks(job_name)

            if not job_tasks or not job_tasks["response"]:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- JOB_TASKS_NOT_FOUND")
                raise Exception("Job tasks not found", 404)

            # Form the payload
            # Insert the job into the database
            insert_job_response = self.dao_request.insert(self.request_id, "jobs", JobPayload.form_insert_job_payload({
                "payload": self.payload.get("payload"),
                "job_name": job_name,
                "service": [task["service"] for task in job_tasks["response"]],
                "tasks": [task["task_name"] for task in job_tasks["response"]]
            }))
            

            # Send request to service to check mail
            if not self.webhook(insert_job_response["response"][0]["service"]):
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- FAILED_TO_SEND_WEBHOOK")
                raise Exception(f"Failed to send webhook --- REQUEST_ID: {self.request_id}", 500)
            

            # Respond with the job ID
            return insert_job_response["response"]["job_id"]


        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            raise ThrowError(str(e), 500)
        
    
    def get_job_tasks(self, job_name):
        # Get job tasks from the database
        job_tasks = self.dao_request.read_list(self.request_id, "job_tasks", {"job_name": job_name})
        return job_tasks["response"]

    def webhook(self, service):
        # Send request to service to check mail
        port = Constant.services[service]["PORT"]
        response = requests.get(Constant.base_url + port + Constant.check_mail_endpoint)

        if response["response"] == "success":
            return True