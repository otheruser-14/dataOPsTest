from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extraction():
    print("1. Extraction des données réussie")

def transformation():
    print("2. Transformation des données réussie")

def chargement():
    print("3. Chargement des données réussi")

with DAG(
    dag_id="test_dataops_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dataops", "test"],
) as dag:

    extract = PythonOperator(
        task_id="extraction",
        python_callable=extraction
    )

    transform = PythonOperator(
        task_id="transformation",
        python_callable=transformation
    )

    load = PythonOperator(
        task_id="chargement",
        python_callable=chargement
    )

    extract >> transform >> load
