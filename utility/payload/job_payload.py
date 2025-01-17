from flask import json
from pydantic import BaseModel

class IInsertJob(BaseModel):
    data: str
    job_name: str
    service: str
    tasks: str

class JobPayload:

    @staticmethod
    def form_insert_job_payload(data: dict) -> IInsertJob:
        payload = {
            "job_name": data.get("job_name"),
            "service": data.get("service"),
            "tasks": json.dumps(data.get("tasks")),
            "data": json.dumps(data.get("payload")),
            "status": "PENDING"
        }
        return payload