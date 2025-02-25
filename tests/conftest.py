from contextlib import contextmanager
import os
from unittest.mock import patch
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from naomi_core.db import (
    Base,
    Message,
    MessageModel,
)
from tests.data import message_data_1, message_data_2, message_model_1, message_model_2

os.environ["OPENAI_BASE_URL"] = ""
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_BASE_MODEL"] = ""


TEST_DATABASE_URL = "sqlite:///:memory:"


@contextmanager
def patch_session_scope(module: str):
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    InMemorySession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @contextmanager
    def mock_session_scope():
        session = InMemorySession()
        yield session
        session.rollback()
        session.close()

    with patch(module, side_effect=mock_session_scope) as session_scope_fn:
        yield session_scope_fn

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def message_data() -> Message:
    return message_data_1()


@pytest.fixture(scope="function")
def message_data2() -> Message:
    return message_data_2()


@pytest.fixture(scope="function")
def message1() -> MessageModel:
    return message_model_1()


@pytest.fixture(scope="function")
def message2() -> MessageModel:
    return message_model_2()


@pytest.fixture(scope="function")
def persist_messages(db_session, message1: MessageModel, message2: MessageModel):
    db_session.add(message1)
    db_session.add(message2)
    db_session.commit()
    return message1, message2
