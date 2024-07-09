# This script contains an example of each CRUD operation for the Note API.
# It is intended to be used as a reference for the implementation of the API.

# Create a note
curl -X POST http://127.0.0.1:8000/note/notes/ -d '{"title": "Test Note", "content": "This is a test note."}' -H "Content-Type: application/json"

# Get all notes
curl -X GET http://127.0.0.1:8000/note/notes/ -H "Content-Type: application/json"

# Get a note
curl -X GET http://127.0.0.1:8000/note/notes/1/ -H "Content-Type: application/json"

# Update a note
curl -X PUT  http://127.0.0.1:8000/note/notes/1/  -d '{"title": "Test Note", "content": "This is the updated test note."}' -H "Content-Type: application/json"

# Delete a note
curl -X DELETE http://127.0.0.1:8000/note/notes/1/