import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.request import Request


class RequestGetJobStatus(AbstractHandler):
    def __init__(self, request_id: str, job_id: str):
        self.request_id = request_id
        self.job_id = job_id

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- GET_JOB_STATUS -- JOB_ID: {self.job_id}")

            # Get job status from the database
            dao_request = Request(logger=current_app.logger)
            job = dao_request.read(self.request_id, "jobs", {"job_id": self.job_id})
            if "response" not in job:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- JOB_NOT_FOUND")
                raise Exception("Job not found", 404)
            
            return { "status": "SUCCESS", "data": job["response"]}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "message": str(e)}
