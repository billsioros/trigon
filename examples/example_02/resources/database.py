from collections.abc import Iterator
from contextlib import contextmanager

from models._model import Model
from settings import DatabaseSettings
from sqlalchemy import create_engine, orm, sql
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool


class Database:
    def __init__(self, settings: DatabaseSettings) -> None:
        self._engine = create_engine(
            str(settings.url),
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

        self.create_database()

    # TODO: startup / shutdown hooks
    def create_database(self) -> None:
        Model.metadata.create_all(self._engine)

    @contextmanager
    def session_factory(self) -> Iterator[Session]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def health_check(self) -> str | None:
        try:
            with self.session_factory() as session:
                session.execute(sql.text("SELECT 1"))
        except Exception as e:
            return str(e)
