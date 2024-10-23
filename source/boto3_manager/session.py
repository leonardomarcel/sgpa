from app.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME
from typing import Union
from django.db import connection
import boto3


class Boto3SessionManager:
    _session = None

    @classmethod
    def get_session(cls):
        if cls._session is None:
            # Create session
            cls._session = boto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION_NAME
            )

        return cls._session


class AsAwsUtil:
    # App.View -> Schema (Tenant) - General Identifiers
    app: str
    view: str
    schema_name: str

    # Boto3 Session
    session: Union[boto3.session.Session, None] = None

    def __init__(self, util_name: str, app_: str, view_: str):
        self.session = Boto3SessionManager.get_session()
        self.app = app_
        self.view = view_
        self.schema_name = connection.schema_name
        self.client = self.session.client(util_name)