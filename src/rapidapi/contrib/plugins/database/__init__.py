from typing import TypeVar

from rapidapi.contrib.plugins import Plugin
from rapidapi.core.dependency_injection import ContainerBuilder

T = TypeVar("T")

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine, orm, sql
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool


class Database:
    def __init__(self, url: str) -> None:
        self._engine = create_engine(
            url,
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


class SQLitePlugin(Plugin):
    def __init__(self, url: str) -> None:
        super().__init__()

        self.url = url

    def register_dependencies(self, container: ContainerBuilder) -> ContainerBuilder:
        return container.bind(Database, Database(self.url))
