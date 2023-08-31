from sanic import Sanic
from sanic_cors import CORS
from mangum import Mangum
import os
from dotenv import load_dotenv
load_dotenv()

app = Sanic("UserProjectService")
CORS(app, resources={r"*": {"origins": "*"}})

# Add Controller
from app.api import Project
app.add_route(Project.as_view(), "/user-project")
# /Add Controller

handler = Mangum(app)