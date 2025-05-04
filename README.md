# team_proj


## how to run 
```sh
# Clone the repository
git clone https://github.com/Timur5050/shops_manager.git
# Change to the project directory
cd shops_manager
# Set up a virtual environment
python -m venv venv
# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
# Install required packages
pip install -r requirements.txt
# create directory in project with files encoders(private and public keys): private.pem and public.pem
# Add an .env file, following the structure provided in sample.env
# Set Up Alembic for Database Migrations
# alembic init alembic
# Import all models into alembic/env.py and set target_metadata = Base.metadata.
# set front end url in main
# build and start docker compose
docker-compose build
# then start containers
docker-compose up
# Go to http://127.0.0.1:8001/doc - swagger documentation
#  http://127.0.0.1:8001/ - API endpoint
```
