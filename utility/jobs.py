class Jobs:
    #These are just template tasks. The real tasks will be fetched from the database
    jobs = {
        "LABEL_PROJECT_INITIALIZATION": {
            "TASKS": [
                {
                    "task_name": "GET_DATASTORE_SET_DIRECTORY",
                    "service": "DATASTORE_MANAGEMENT_SERVICE",
                    "order_index": 1
                },
                {
                    "task_name": "GET_DATASET_ANNOTATION_PATH",
                    "service": "DATASTORE_MANAGEMENT_SERVICE",
                    "order_index": 2,
                },
                {
                    "task_name": "VALIDATE_CONFIG", 
                    "service": "LABEL_STUDIO_INTEGRATION_SERVICE",
                    "order_index": 3
                },
                {
                    "task_name": "CREATE_LABEL_PROJECT",
                    "service": "LABEL_STUDIO_INTEGRATION_SERVICE",
                    "order_index": 4
                },
                {
                    "task_name": "CREATE_WEBHOOK",
                    "service": "LABEL_STUDIO_INTEGRATION_SERVICE",
                    "order_index": 5
                },
                {
                    "task_name": "CREATE_IMPORT_STORAGE",
                    "service": "LABEL_STUDIO_INTEGRATION_SERVICE",
                    "order_index": 6
                },
                {
                    "task_name": "CHECK_RAW_DATA",
                    "service": "DATASTORE_MANAGEMENT_SERVICE",
                    "order_index": 7
                },
                {
                    "task_name": "SYNC_IMPORT_STORAGE",
                    "service": "LABEL_STUDIO_INTEGRATION_SERVICE",
                    "order_index": 8
                }
            ]
        },
        "HANDLE_LABEL_PROJECT_UPDATE": {
            "TASKS": [
               
                {
                    "task_name": "VERIFY_DATASET_OUTPUT_PATH",
                    "service": "DATASTORE_MANAGEMENT_SERVICE",
                    "order_index": 1
                },
                {
                    "task_name": "VERIFY_TEMP_OUTPUT_PATH",
                    "service": "LABEL_STUDIO_INTEGRATION_SERVICE",
                    "order_index": 2
                },
                {
                    "task_name": "REQUEST_EXPORT_ALL_FRAMES",
                    "service": "LABEL_STUDIO_INTEGRATION_SERVICE",
                    "order_index": 3
                },
                {
                    "task_name": "REFORMAT_EXPORTED_FRAMES",
                    "service": "DATA_PROCESSING_SERVICE",
                    "order_index": 4
                },
                """ {
                    "task_name": "MERGE_ANNOTATION_TO_DATASET",
                    "service": "DATASTORE_MANAGEMENT_SERVICE",
                    "order_index": 4
                } """

            ]
        },
        "REGISTER_USER": {
            "TASKS": [
                {
                    "task_name": "INSERT_USER",
                    "service": "USER_MANAGEMENT_SERVICE",
                    "order_index": 1
                },
                {
                    "task_name": "INSERT_USER_REGISTRATION",
                    "service": "USER_MANAGEMENT_SERVICE",
                    "order_index": 2
                },
                {
                    "task_name": "EMAIL_USER_VERIFICATION",
                    "service": "EMAIL_NOTIFICATION_SERVICE",
                    "order_index": 3
                }
            ]
        }
    }