import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
from app.main import app
from app.api.database import get_session

# 인메모리 테스트용 SQLite DB 설정
sqlite_url = "sqlite:///:memory:"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

@pytest.fixture(name="session")
def session_fixture():
    """테스트마다 독립적인 세션을 생성하고 종료 후 롤백/클린업"""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """get_session 종속성을 테스트용 세션으로 오버라이딩하여 TestClient 반환"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
