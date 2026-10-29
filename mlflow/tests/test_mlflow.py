import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

mlflow.set_experiment("DataOps-AirQuality")

with mlflow.start_run(run_name="test_infrastructure"):

    mlflow.log_param("model", "RandomForest")

    mlflow.log_param("dataset", "air_quality")

    mlflow.log_metric("accuracy", 0.95)

    mlflow.log_metric("rmse", 0.12)

    print("Expérience MLflow enregistrée avec succès !")
