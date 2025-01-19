# FullStack Template Tutorial Part 2: API Endpoints and User Authentication

This repo corresponds to a [Tutorial](https://jezziecodes.com/blog-posts/fullstack-template-project-tutorial-p2-api) that goes through the process of creating a Fullstack template project step by step. To view the complete fullstack template (frontend and backend) see the full-stack-template-part-3 repo. 

### Steps to run this project:

1. Add/Create a new Python environment to your project. Select Virtualenv (venv) and your preferred Python version (3.8+). Install the dependencies in _requirements.txt_.
2. Add a _.env_ file to the backend folder with the following contents, make sure to add your own PostgreSQL database variables.

   ```txt
    # Postgres
    POSTGRES_SERVER=localhost
    POSTGRES_PORT=5432
    POSTGRES_DB=demo2
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres

    # First Admin User
    FIRST_ADMIN_EMAIL=admin@template.com
    FIRST_ADMIN_NAME=admin
    FIRST_ADMIN_PASSWORD=password

    # Backend
    SECRET_KEY=my-32-character-ultra-secure-and-ultra-long-secret
   ```
4. Run the following alembic command.
   ### `alembic upgrade head`
5. Run the main function in the _initial_data.py_ file to populate your admin user.
6. Create a Run Configuration for a fastAPI project or simply use the following command to run from the Terminal.
   ### `uvicorn main:app --reload`


# Part 3

Part 3 focuses on building the Frontend of the Appointment Manager App and integration with the Backend.
