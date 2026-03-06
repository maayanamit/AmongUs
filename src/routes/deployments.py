import secrets
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.exceptions.deployment_exceptions import InvalidUsername, DatabaseExists, NotFound, UuidInvalid
from src.mongo_con import mongo_crud
from src.postgres_con import postgres_crud
from src.routes.models import DeploymentPost, DeploymentDbname

router = APIRouter()

security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"  # TODO change to list of users
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}


@router.post("/deployments", status_code=201)
def create_deployment(username: Annotated[str, Depends(get_current_username)],
                      db_details: DeploymentPost):
    if username != db_details.username:
        raise InvalidUsername()
    elif len(username) < 3:
        raise InvalidUsername("The username is too short. minimum length is 3 characters")
    elif not db_details.db_name.startswith(db_details.username):
        raise InvalidUsername("the db name prefix is not your username")
    else:
        result = postgres_crud.add_deployment(db_details)
        if not result:
            raise DatabaseExists()
        mongo_crud.create_database(db_details.db_name)
        return result


def uuid_is_valid(value_id: str):
    try:
        return str(UUID(str(value_id))) == str(value_id)
    except ValueError:
        return False


@router.get("/deployments/:{deployment_id}", status_code=200)
def get_by_id(username: Annotated[str, Depends(get_current_username)], deployment_id: str):
    if not uuid_is_valid(deployment_id):
        raise UuidInvalid()
    response = postgres_crud.get_deployment_by_id(deployment_id)
    if not response:
        raise NotFound()
    elif response.db_name.startswith(username):
        return response
    raise InvalidUsername("your username does not have access to this database")


@router.put("/deployments/:{deployment_id}", status_code=200)
def update_db(username: Annotated[str, Depends(get_current_username)], deployment_id: str, db_name: DeploymentDbname):
    if not uuid_is_valid(deployment_id):
        raise UuidInvalid()
    if not db_name.db_name.startswith(username):
        raise InvalidUsername("The database name's prefix has to be your username")
    else:
        response = postgres_crud.update_deployment_name(deployment_id, db_name.db_name)
        if not response:
            raise InvalidUsername("deployment id does not exist..")
        new_id = response.get("id")
        old_db_name = response.get("db_name")
        mongo_crud.update_database_name(old_db_name, db_name.db_name)
        return new_id


@router.delete("/deployments/:{deployment_id}:{dep_username}", status_code=204)
def delete_by_id(username: Annotated[str, Depends(get_current_username)], deployment_id: str, dep_username: str):
    if not uuid_is_valid(deployment_id):
        raise UuidInvalid()
    if username != dep_username:
        raise InvalidUsername("your username and the username entered do not match! you do not have access to this db")
    result = postgres_crud.delete_by_id(deployment_id, dep_username)
    if not result:
        raise InvalidUsername("The username entered and the ID do not match")
    else:
        mongo_crud.delete_database(result)


@router.get("/deployments/:{deployment_id}:{dep_username}", status_code=200)
def get_connection_string(username: Annotated[str, Depends(get_current_username)], deployment_id: str, dep_username: str):
    pass