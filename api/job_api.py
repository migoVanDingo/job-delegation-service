from flask import Blueprint, g, json, request

from api.handler.request_get_job_status import RequestGetJobStatus
from classes.job_creator import JobCreator


job_api = Blueprint('job_api', __name__)

@job_api.route('/job/new', methods=['POST'])
def create_job():
    data = json.loads(request.data)
    request_id = g.request_id
    job_manager = JobCreator(request_id, data)
    response = job_manager.create_job()

    return response

@job_api.route('/job/status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    request_id = g.request_id
    api_request = RequestGetJobStatus(request_id, job_id)
    response = api_request.do_process()
    return response


