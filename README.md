# multitenant-auth-service

## Tech Stack:
- Framework: FastAPI
- Database: Postgres
- ORM: SQLAlchemy
- Migration Tool: Alembic
- Email Integration: Brevo

## Steps to Run 
- Create a .env file in the root directory
- Fill in the values from .env.sample file to fill in the appropriate values
  - Fill in the approriate name for postgres user, password and db name
  - Change the Backend DB URL according to previous step
  - Generate a new JWT Key using "openssl rand -hex 32"
  - Write the appropriate Brevo API Key for email integration
  - Alternate, get the env file from the repository owner and paste it in the root directory
- Run "docker compose up --build -d"
  - Docker compose command may change according to windows, wsl or mac so check the appropriate command
- API Testing
  - Test the APIs by importing the Multitenant-Auth.postman_collection.json into Postman
    - Please set the right value of baseUrl in Collection Variables
    - The token is sent via query parameter in all the apis and is set through collection.variable token 
    - When the signin api responds with access_token, it is automatically sets the collection.variable token
  - Test the APIs on Fastapi docs "http://localhost:8020/docs"
 
## Working with APIs (Assumptions)
- On signup, an invitation link is sent to email and after clicking on the verification link, the user status becomes active to perform other tasks
- By default there are two roles added: owner and member
- On signup with new organization, signed up user becomes the owner of the organziation
- On creating a new organization, the user who is signed in automatically becomes the owner
- A new member is added with "member" role on invitation to organization
- As certain APIs require org_id, user_id, role_id so additional APIs were added under "info" tag to get these details about ids using APIs: Organization List, Org Member List and Roles List
  
