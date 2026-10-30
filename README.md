                  GitHub (branches / pull requests)
                              |
                              v
                       Jenkins (CI)

   Sources de données (à intégrer)
                 |
                 v
        Kafka : raw_data
                 |
                 v
      Traitements (à développer) <---- Airflow (orchestration)
                 |
          +------+-------+
          |              |
          v              v
 Kafka : processed_data  Kafka : anomalies
          |
          v
 PostgreSQL (stockage à intégrer)
          |
          +----------> FastAPI (API à enrichir)
          |
          +----------> MLflow (suivi ML à intégrer)
