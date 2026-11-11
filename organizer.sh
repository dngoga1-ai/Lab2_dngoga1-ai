#!/usr/bin/env bash

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVE_DIR="archive"
ORIGINAL_FILE="grades.csv"
ARCHIVED_FILE="grades_${TIMESTAMP}.csv"
LOG_FILE="organizer.log"

# Create archive directory if it does not exist
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
fi

# Check that grades.csv exists
if [ ! -f "$ORIGINAL_FILE" ]; then
    echo "Error: $ORIGINAL_FILE was not found."
    exit 1
fi

# Move and rename the grades file
mv "$ORIGINAL_FILE" "$ARCHIVE_DIR/$ARCHIVED_FILE"

# Create a new empty grades.csv
touch "$ORIGINAL_FILE"

# Log the operation
echo "$TIMESTAMP | $ORIGINAL_FILE | $ARCHIVE_DIR/$ARCHIVED_FILE" >> "$LOG_FILE"

echo "Grades file archived successfully."
echo "Archived file: $ARCHIVE_DIR/$ARCHIVED_FILE"
echo "New grades.csv created."
