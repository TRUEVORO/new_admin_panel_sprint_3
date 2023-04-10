#!/bin/sh

set -e

echo "Waiting for postgres..."
while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Waiting for Elasticsearch to start..."
until curl -s "${ELASTICSEARCH_DSN}/_cat/health?h=status" | grep -E -q "(yellow|green)"; do
  sleep 2
done

echo "Elasticsearch started."

INDEXES_PATH="/opt/postgres_to_es/elasticsearch_indexes"

# Function to create an index with the given name
create_index() {
  index_name="$1"

  # Check if the index already exists
  index_exists=$(curl -s -o /dev/null -w "%{http_code}" "${ELASTICSEARCH_DSN}/${index_name}")

  # Create the index with the mapping if it doesn't exist
  if [ "$index_exists" -ne 200 ]; then
    curl -XPUT "${ELASTICSEARCH_DSN}/${index_name}" -H "Content-Type: application/json" --data-binary "@${INDEXES_PATH}/${index_name}.json"
    echo "Index '${index_name}' created successfully."
  else
    echo "Index '${index_name}' already exists. Skipping index creation."
  fi
}

create_index "genres"
create_index "movies"
create_index "persons"

python src/main.py
