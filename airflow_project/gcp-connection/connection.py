from airflow import models, settings

# Create the gcp connection
cloud_conn = models.Connection(
    conn_id="gcp_connection_key",
    conn_type="google_cloud_platform",
    extra={"extra__google_cloud_platform__project": "zinc-forge-399014",
          "extra__google_cloud_platform__key_path": "/home/SEHC/airflow_project/gcp-connection/key_service.json"}
)

# Add the connection to Airflow
session = settings.Session()
session.add(cloud_conn)
session.commit()
session.close()
