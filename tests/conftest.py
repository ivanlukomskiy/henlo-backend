import json
import weakref

import pytest
from twisted.internet.tcp import BaseClient

from tests.factories import UserFactory


@pytest.fixture()
def client(_, settings):
    client_ = Client(settings=settings)
    return client_


@pytest.fixture()
def logged_in_client(client):
    user = UserFactory()
    client.login(username=user.username, password='')
    return client


class JsonClient:
    def __init__(self, client):
        self.client = client

    def get(self, path, data=None, **extra):
        return self.jsonify(self.client.get(
            path,
            data={} if data is None else data,
            **extra,
        ))

    def post(self, path, data=None, content_type='application/json', **extra):
        return self.jsonify(self.client.post(
            path,
            data=json.dumps({} if data is None else data),
            content_type=content_type,
            **extra,
        ))

    def head(self, path, data=None, **extra):
        return self.jsonify(self.client.head(
            path,
            data={} if data is None else data,
            **extra,
        ))

    def options(self, path, data=None, content_type='application/json', **extra):
        return self.jsonify(self.client.options(
            path,
            data=json.dumps({} if data is None else data),
            content_type=content_type,
            **extra,
        ))

    def put(self, path, data=None, content_type='application/json', **extra):
        return self.jsonify(self.client.put(
            path,
            data=json.dumps({} if data is None else data),
            content_type=content_type,
            **extra,
        ))

    def patch(self, path, data=None, content_type='application/json', **extra):
        return self.jsonify(self.client.patch(
            path,
            data=json.dumps({} if data is None else data),
            content_type=content_type,
            **extra,
        ))

    def delete(self, path, data=None, content_type='application/json', **extra):
        return self.jsonify(self.client.delete(
            path,
            data=json.dumps({} if data is None else data),
            content_type=content_type,
            **extra,
        ))

    def jsonify(self, response):
        response.json = lambda: json.loads(response.content) if hasattr(response, 'content') else None
        return response


class Client(BaseClient):
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self.json = JsonClient(weakref.proxy(self))
        self.settings = kwargs['settings']
