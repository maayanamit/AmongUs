import datetime

from sqlalchemy import select

from src.postgres_con import engine, Deployment, StatusDeployment
from sqlalchemy.orm import Session
from src.routes.models import DeploymentPost, DeploymentGetById, DeploymentId


def add_deployment(deployment_post: DeploymentPost):
    session = Session(engine)
    with (session.begin()):
        if session.query(Deployment).filter(Deployment.db_name == deployment_post.db_name).first():
            return False
        deployment: Deployment = Deployment(db_name=deployment_post.db_name, status=StatusDeployment.CREATED,
                                            username=deployment_post.username,
                                            creation_time=datetime.datetime.now())
        session.add(deployment)
    dep = session.scalar(select(Deployment).where(Deployment.db_name == deployment_post.db_name))
    session.close()
    return DeploymentId(**{"id": str(dep.id)})  # TODO what to return?


def get_deployment_by_id(id_dep: str):
    session = Session(engine)
    query = select(Deployment).where(Deployment.id == id_dep)
    result = session.scalar(query)
    session.close()
    if result:
        result_dict = result.as_dict()
        result_dict.pop("username")
        return DeploymentGetById(**result_dict)
    return None


def update_deployment_name(id_dep: str, new_name: str):
    session = Session(engine)
    old_name: str
    with session.begin():
        query = select(Deployment).where(Deployment.id == id_dep)
        deployment: Deployment = session.scalar(query)
        if not deployment:
            return None
        old_name = deployment.db_name
        deployment.db_name = new_name
    dep = session.scalar(select(Deployment).where(Deployment.db_name == new_name))
    session.close()
    return {"id": str(dep.id), "db_name": old_name}


def delete_by_id(id_dep: str, username: str):  # TODO check that id exists in db
    session = Session(engine)
    with session.begin():
        query = select(Deployment).where(Deployment.id == id_dep)
        deployment: Deployment = session.scalar(query)
        if not deployment or deployment.username != username:
            return None
        deployment.status = StatusDeployment.DELETED
        return deployment.db_name


def get_connection_string(id_dep: str):
    pass
