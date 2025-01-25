import threading
import time
import uuid
from flask import Flask, g, jsonify, request, make_response
from flask_cors import CORS
import logging
from api.job_api import job_api
from classes.job_delegator import JobDelegator
from utility.error import ThrowError
from utility.utils import Utils



# logging.basicConfig(filename='record.log',
#                 level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(lineno)d | \n %(message)-20s')

def create_app():
    app = Flask(__name__)
    CORS(app)
    Utils.setup_logging()

    

    #Register blueprints
    app.register_blueprint(job_api, url_prefix='/api')


    return app

app = create_app()
# Start thread for job deletation
# with app.app_context():
#     job_delegator = JobDelegator(app)

#     # def run_job_delegator_periodically():
#     #     while True:
#     #         job_delegator.run()  # Call the function
#     #         time.sleep(5)  # Wait 5 seconds before the next iteration

#     # Start the thread
#     job_delegation_thread = threading.Thread(target=job_delegator.run, daemon=True)
#     job_delegation_thread.start()


@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response('success', 200)
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = '*'
        return response
    else:
        request_id = str(uuid.uuid4())
        g.request_id = request_id


@app.errorhandler(ThrowError)
def handle_throw_error(error):
    response = jsonify({
        "message": str(error),
        "error_code": error.status_code
    })
    response.status_code = error.status_code
    return response