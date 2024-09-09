# multitenant-auth-service
- Create a .env file in the root directory
- Fill in the values from .env.sample file to fill in the appropriate values
  - Write the approriate name for postgres user, password and db name
  - Change the Backend DB URL according to previous step
  - Generate a new JWT Key using openssl rand -hex 32
  - Write the appropriate Brevo API Key for email integration
  - Alternate, get the env file from the repository owner and paste it in the root directory

- Run "docker compose up --build -d"
- Docker compose command may change according to windows, wsl or mac so check the appropriate command
- Test the APIs by importing the Multitenant-Auth.postman_collection.json into Postman
- Or Test the APIs on Fastapi docs "http://localhost:8020/docs" 