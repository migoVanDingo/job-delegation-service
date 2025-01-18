from flask import json
from pydantic import BaseModel

class IInsertJob(BaseModel):
    data: str
    job_name: str
    tasks: str
    status: str

class JobPayload:

    @staticmethod
    def form_insert_job_payload(data: dict) -> IInsertJob:
        payload = {
            "job_name": data.get("job_name"),
            "tasks": json.dumps(data.get("tasks")),
            "data": json.dumps(data.get("payload")),
            "status": "PENDING"
        }
        return payload