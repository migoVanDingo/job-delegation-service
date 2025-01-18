class Constant:
    service = "datastore-management-service"

    datastore_root_dir = "/Users/bubz/Developer/master-project/tests/test-datastore-root"

    base_url = "http://localhost:"
    dao_port = "5010"

    check_mail_endpoint = "/api/check_mail"

    id_length = 25
    max_threads = 5
    max_queue = 10

    services = {
        "DAO_SERVICE": {
            "PORT": "5010",
            "ENDPOINT": {
                "CREATE": "/api/create",
                "READ": "/api/read",
                "LIST": "/api/read_list",
                "UPDATE": "/api/update",
                "DELETE": "/api/delete",
                "READ_ALL": "/api/read_all",
                "QUERY": "/api/query"
            }
        },
        "DATA_PROCESSING_SERVICE": {
            "PORT": "5011",
        },
        "DATASTORE_MANAGEMENT_SERVICE": {
            "PORT": "5012",
            "ENDPOINT":{
                "CHECK_RAW_DATA": "/api/datastore/check-raw-data",
                "GET_DATASET_ANNOTATION_PATH": "/api/datastore/dataset/path/annotation",
                "GET_DATASTORE_SET_DIRECTORY": "/api/datastore/path/set", 
                
            }
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
            "ENDPOINT": {
                "CREATE_LABEL_PROJECT": "/api/label-project/new",
                "CREATE_IMPORT_STORAGE": "/api/label-project/import-storage",
                "SYNC_IMPORT_STORAGE": "/api/label-project/import-storage/sync",
                "CREATE_WEBHOOK": "/api/label-project/webhook",
                "VALIDATE_CONFIG": "/api/label-project/validate-config"
            },

        },
    },

    

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
