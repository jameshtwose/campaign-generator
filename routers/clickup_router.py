from fastapi import APIRouter
import requests

from settings import ClickUpSettings

router = APIRouter(prefix="/clickup", tags=["clickup"])

@router.get("/tasks")
async def clickup_tasks():
    # get space id
    response = requests.get(
        "https://api.clickup.com/api/v2/team/{team_id}/space".format(team_id=ClickUpSettings().clickup_team_id),
        headers={
            "Authorization": ClickUpSettings().clickup_api_key
        }
    )
    if response.status_code == 200:
        spaces = response.json().get("spaces", [])
        if not spaces:
            return {"error": "No spaces found"}
        space_id = spaces[0].get("id")
        # print("Spaces:", spaces)
        # print("Space ID:", space_id)
    else:
        return {"error": "Failed to retrieve space ID"}
    
    # get folders
    response = requests.get(
        "https://api.clickup.com/api/v2/space/{space_id}/folder".format(space_id=space_id),
        headers={
            "Authorization": ClickUpSettings().clickup_api_key
        }
    )
    if response.status_code == 200:
        folders = response.json().get("folders", [])
        if not folders:
            return {"error": "No folders found"}
        folder_id = folders[0].get("id")
        # print("Folders:", folders)
        # print("Folder ID:", folder_id)
    else:
        return {"error": "Failed to retrieve folder ID"}
    
    # get lists
    response = requests.get(
        "https://api.clickup.com/api/v2/folder/{folder_id}/list".format(folder_id=folder_id),
        headers={
            "Authorization": ClickUpSettings().clickup_api_key
        }
    )
    if response.status_code == 200:
        lists = response.json().get("lists", [])
        if not lists:
            return {"error": "No lists found"}
        list_id = lists[0].get("id")
        # print("Lists:", lists)
        # print("List ID:", list_id)
    else:
        return {"error": "Failed to retrieve list ID"}

    response = requests.get(
        "https://api.clickup.com/api/v2/list/{list_id}/task".format(list_id=list_id),
        headers={
            "Authorization": ClickUpSettings().clickup_api_key
        }
    )
    # print(response.status_code, response.json())
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to retrieve tasks"}