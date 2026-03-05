import datetime
import enum
from uuid import UUID, uuid4

from sqlalchemy import create_engine, Enum
from sqlalchemy import MetaData, DateTime
import logging


from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)


def get_db_engine():
    return create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format('postgres', 'postgres', 'localhost:5432', 'amongodb'))


engine = get_db_engine()
metadata = MetaData()


class StatusDeployment(enum.Enum):
    CREATED = 'CREATED'
    DELETED = "DELETED"


class Base(DeclarativeBase):
    pass


class Deployment(Base):
    __tablename__ = "deployments_db"
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    db_name: Mapped[str] = mapped_column()
    status: Mapped[StatusDeployment] = mapped_column(Enum(StatusDeployment, name="status"))
    username: Mapped[str] = mapped_column()
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return (f"Deployment(id={self.id!r}, db_name={self.db_name!r}, status={self.status!r}, username={self.username!r}, "
                f"creation_time={self.creation_time!r})")

    def as_dict(self) -> dict:
        return {"id": str(self.id), "db_name": self.db_name, "status": str(self.status), "username": self.username,
                "creation_time": self.creation_time}


Base.metadata.create_all(engine)
