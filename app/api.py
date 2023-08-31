from sanic.views import HTTPMethodView
from sanic.response import json
from pycognito import Cognito
import jwt
import os
from datetime import datetime
from app.common import jwt_user, success_res, error_res, paginate, insert_data, update_data

class Project(HTTPMethodView):
  
  @jwt_user
  async def get(self, request, user):
    project_query = "SELECT * FROM project WHERE p_account_id={u_account_id}".format(u_account_id=user["u_account_id"])
    project_count_query = "SELECT count(*) FROM project WHERE p_account_id={u_account_id}".format(u_account_id=user["u_account_id"])
    
    if request.args.get("search"):
      search_query = " AND p_name LIKE '%{search}%' ".format(search=request.args.get("search"))
      project_query += search_query
      project_count_query += search_query

    projects = await paginate(project_query, project_count_query, request)

    return success_res({"data": projects})

  @jwt_user
  async def post(self, request, user):
    project_data = {
      "p_account_id": user["u_account_id"],
      "p_created_by": user["u_id"],
      "p_name": request.json.get("p_name"),
      "p_status": "active",
      "p_created": str(datetime.now()),
      "p_modified": str(datetime.now()),
    }

    await insert_data("project", project_data)

    return success_res()  

  @jwt_user
  async def put(self, request, user):
    project_data = {
      "p_name": request.json.get("p_name"),
      "p_modified": str(datetime.now()),
    }

    condition = "p_id={project_id}".format(project_id=request.json.get("p_id"))
    await update_data("project", condition, project_data)

    return success_res({"status": "success"})

  @jwt_user
  async def patch(self, request, user):
    project_data = {
      "p_status": request.json.get("p_status"),
    }

    condition = "p_id={project_id}".format(project_id=request.json.get("p_id"))
    await update_data("project", condition, project_data)

    return success_res()