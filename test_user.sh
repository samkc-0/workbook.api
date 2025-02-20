#!/bin/bash

# API Base URL
BASE_URL="http://127.0.0.1:8000/workbook/api"


# Test User Credentials
USERNAME="testuser_$(openssl rand -hex 4)"
PASSWORD="testpassword_$(openssl rand -hex 4)"

echo "🚀 Creating user..."
CREATE_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/create-user/" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")

if [ "$CREATE_RESPONSE" -ne 201 ]; then
    echo "❌ User creation failed (Expected 201, got $CREATE_RESPONSE)"
    exit 1
fi
echo "✅ User created successfully."

echo "🔑 Requesting JWT token..."
TOKEN=$(curl -s -X POST "$BASE_URL/token/" -H "Content-Type: application/json" \
    -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" | jq -r .access)

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
    echo "❌ Authentication failed. Exiting..."
    exit 1
fi
echo "✅ Token acquired: $TOKEN"

# Topic ID for progress tracking
TOPIC_ID=1

echo "📈 Incrementing progress..."
for i in {1..3}; do
    PROGRESS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$BASE_URL/progress/" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"topic\": $TOPIC_ID, \"exercise_number\": $i}")

    if [ "$PROGRESS_RESPONSE" -ne 200 ]; then
        echo "❌ Progress update failed at step $i (Expected 200, got $PROGRESS_RESPONSE)"
        exit 1
    fi
    echo "✅ Progress updated to $i."
done

# Get the progress response
PROGRESS_CHECK=$(curl -s -X GET "$BASE_URL/progress/?topic=$TOPIC_ID" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json")

# Extract "exercise_number" from JSON response
EXERCISE_NUMBER=$(echo "$PROGRESS_CHECK" | jq -r '.exercise_number')

# Validate that exercise_number is 3
if [[ "$EXERCISE_NUMBER" -ne 3 ]]; then
    echo "❌ Progress verification failed (Expected exercise_number: 3, got $EXERCISE_NUMBER)"
    exit 1
fi
echo "✅ Progress retrieval successful."



echo "🎉 All tests passed successfully!"
exit 0