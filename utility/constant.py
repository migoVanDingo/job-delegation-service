class Constant:
    service = "datastore-management-service"

    datastore_root_dir = "/Users/bubz/Developer/master-project/tests/test-datastore-root"

    base_url = "http://localhost:"
    dao_port = "5010"

    check_mail_endpoint = "/api/check_mail"

    services = {
        "DAO_SERVICE": {
            "PORT": "5010",
        },
        "DATA_PROCESSING_SERVICE": {
            "PORT": "5011",
        },
        "DATASTORE_MANAGEMENT_SERVICE": {
            "PORT": "5012",
        },
        "PROJECT_MANAGEMENT_SERVICE": {
            "PORT": "5013",
        },
        "USER_MANAGEMENT_SERVICE": {
            "PORT": "5014",
        },
        "TEAM_MANAGEMENT_SERVICE": { 
            "PORT": "5015",
        },
        "LABEL_STUDIO_INTEGRATION_SERVICE": {
            "PORT": "5016",
        },
    }

    dao = {
        "create": "/api/create",
        "read": "/api/read",
        "list": "/api/read_list",
        "update": "/api/update",
        "delete": "/api/delete",
        "read_all": "/api/read_all",
        "query": "/api/query"
    }

    table = {
        "DATASTORE": "datastore",
        "DATASTORE_ROLES": "datastore_roles",
        "DATASET": "dataset",
        "DATASET_ROLES": "dataset_roles",
        "FILES": "files",
        "DATASTORE_CONFIG": "datastore_config",
        "DATASET_FILES": "dataset_files",
        "JOBS": "jobs",
        "JOB_TASKS": "job_tasks",
    }




    
