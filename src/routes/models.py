from datetime import datetime
from pydantic import BaseModel


class DeploymentPost(BaseModel):
    db_name: str
    username: str


class DeploymentGetById(BaseModel):
    id: str
    db_name: str
    status: str
    creation_time: datetime


class DeploymentId(BaseModel):
    id: str


class DeploymentDbname(BaseModel):
    db_name: str

