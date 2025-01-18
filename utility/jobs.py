class Jobs:
    jobs = {


        "LABEL_PROJECT_INITIALIZATION": [
            # Check if raw data is available or if it needs to be fetched
            {
                "SERVICE": "DATASTORE_MANAGEMENT_SERVICE",
                "TASK": "CHECK_RAW_DATA", 
                "ORDER_INDEX": 1

            },

            # Gather dataset path for webhook output
            {
                "SERVICE": "DATASTORE_MANAGEMENT_SERVICE",
                "TASK": "GET_DATASET_ANNOTATION_PATH", 
                "ORDER_INDEX": 2},

            # Get datastore set directory for import storage
            {
                "SERVICE": "DATASTORE_MANAGEMENT_SERVICE",
                "TASK": "GET_DATASTORE_SET_DIRECTORY", 
                "ORDER_INDEX": 3},

            # Validate the label configs
            {
                "SERVICE": "LABEL_STUDIO_INTEGRATION_SERVICE",
                "TASK": "VALIDATE_CONFIG", 
                "ORDER_INDEX": 4},

            # Create label project
            {
                "SERVICE": "LABEL_STUDIO_INTEGRATION_SERVICE",
                "TASK": "CREATE_LABEL_PROJECT", 
                "ORDER_INDEX": 5},

            # Initialize webhook for output
            {
                "SERVICE": "LABEL_STUDIO_INTEGRATION_SERVICE",
                "TASK": "CREATE_WEBHOOK", 
                "ORDER_INDEX": 6},

            # Initialize import storage for videos/audio/images
            {
                "SERVICE": "LABEL_STUDIO_INTEGRATION_SERVICE",
                "TASK": "CREATE_IMPORT_STORAGE", 
                "ORDER_INDEX": 7},

            # Sync import storage
            {
                "SERVICE": "LABEL_STUDIO_INTEGRATION_SERVICE",
                "TASK": "SYNC_IMPORT_STORAGE", 
                "ORDER_INDEX": 8}
        ]



    }
