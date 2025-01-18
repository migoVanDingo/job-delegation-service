from flask import Blueprint, g, json, request

from classes.job_creator import JobCreator


job_api = Blueprint('job_api', __name__)

@job_api.route('/job/new', methods=['POST'])
def create_job():
    data = json.loads(request.data)
    request_id = g.request_id
    job_manager = JobCreator(request_id, data)
    response = job_manager.create_job()

    return response


