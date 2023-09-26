BUCKET="bigdata-python"
FILE_NAMES=("playlists_export.json" "videoids_export.json" "commentvideo_export.json" "statics_export.json")

migrate_data(){
  FILE_NAME=$1
  URI_PATH="/home/SEHC/airflow_project/data/${FILE_NAME}"
  echo "Migrate data from uri '$URI_PATH' to gcs '$BUCKET'..."
  gsutil -o "GSUtil:parallel_composite_upload_threshold=150M" -m cp "$URI_PATH" gs://"$BUCKET"
}

# Export data from MongoDB and process it for each collection
for FILE_NAME in "${FILE_NAMES[@]}"; do
    migrate_data "$FILE_NAME"
done
