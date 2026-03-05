import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.exceptions.deployment_exceptions import InvalidUsername
from src.mongo_con import mongo_crud
from src.postgres_con import postgres_crud
from src.routes.models import DeploymentPost, DeploymentId

app = FastAPI()

security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
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


@app.get("/")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}


@app.post("/deployments", status_code=201)
def create_deployment(username: Annotated[str, Depends(get_current_username)],
                      db_details: DeploymentPost) -> DeploymentId:
    if username != db_details.username:
        raise InvalidUsername()
    elif len(username) < 3:
        raise InvalidUsername("The username is too short. minimum length is 3 characters")
    elif not db_details.db_name.startswith(db_details.username):
        raise InvalidUsername("the db name prefix is not your username")
    else:
        mongo_crud.create_database(db_details.db_name)
        return postgres_crud.add_deployment(db_details)

