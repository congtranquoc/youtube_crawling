#!/bin/bash

# MongoDB Database Information
DATABASE="youtube_db"
COLLECTIONS=("playlists" "videoids" "commentvideo" "statics")

# Function to export data from MongoDB and ensure valid JSON formatting
export_data() {
    COLLECTION=$1
    FILE="/home/quoccong-workspace/airflow_project/data/${COLLECTION}_export.json"
    TEMP_FILE="/home/quoccong-workspace/airflow_project/data/${COLLECTION}_export_temp.json"

    echo "Exporting data from collection '$COLLECTION' to file '$FILE'..."
    mongoexport --db "$DATABASE" --collection "$COLLECTION" > "$TEMP_FILE"

    echo "Ensuring valid JSON formatting using jq..."
    jq -c '.' "$TEMP_FILE" > "$FILE"

    echo "Cleaning up temporary file..."
    rm "$TEMP_FILE"
}

# Check if MongoDB service is running
if sudo systemctl is-active --quiet mongod; then
    echo "MongoDB service is running."
else
    echo "MongoDB service is not running. Starting MongoDB..."
    sudo systemctl start mongod
fi

# Check if MONGO_HOST and MONGO_PORT environment variables are set
if [ -z "$MONGO_HOST" ] || [ -z "$MONGO_PORT" ]; then
    echo "MONGO_HOST and MONGO_PORT environment variables are not set. Please set them."
    exit 1
fi

# Check connection to MongoDB
echo "Checking connection to MongoDB..."
if mongosh --host $MONGO_HOST --port $MONGO_PORT --eval "quit()" 2>/dev/null; then
    echo "Successfully connected to MongoDB"
else
    echo "Unable to connect to MongoDB. Make sure MongoDB is running and check the host and port settings."
    exit 1
fi

# Check if the database exists
echo "Checking if database '$DATABASE' exists..."
if ! mongosh --host $MONGO_HOST --port $MONGO_PORT --eval "db.getSiblingDB('$DATABASE')" | grep -q "not found"; then
    echo "Database '$DATABASE' exists"
else
    echo "Database '$DATABASE' does not exist"
    exit 1
fi

# Export data from MongoDB and process it for each collection
for COLLECTION in "${COLLECTIONS[@]}"; do
    export_data "$COLLECTION"
done
