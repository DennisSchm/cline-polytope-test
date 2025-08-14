@/.context/polytope/general/instructions.md @/.context/polytope/general @/.context/polytope/templates

generate a polytope template 'stack' that runs the following modules.
# Frontend (React App)
A React application, served on port 3000 by default. 
It needs form fields for
- username: string
- message: string
And an area to show new messages in real time. 

# API (FastAPI Python API)
A FastAPI Python API, served on port 4000 by default. It should expose `messages` as a REST API resource and a WebSocket endpoint for the frontend to receive new messages in real-time.

# Postgres DB
use a postgres db

Keep the README.md as concise as possible.
