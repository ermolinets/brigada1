import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError
from app.support.types import Repository, CheckResult, Money, money


def error(code, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == code


def invoke(service, method, *args, **kwargs):
    return api.call(service, method, *args, **kwargs)

from app.support.types import CustomerContext

def context():
    return CustomerContext()

def entity(key='C1'):
    return api.make(key, "Alice", "STANDARD")

def prepared(key='C1'):
    service = api.create()
    item = entity(key)
    invoke(service, "register", item)
    return service, item

def test_basic_lifecycle_and_isolation():
    service, item = prepared()
    other = entity("OTHER")
    invoke(service, "register", other)
    assert invoke(service, "check", 'C1', context()).allowed
    invoke(service, 'block', 'C1')
    assert invoke(service, "check", 'C1', context()).code == 'CUSTOMER_BLOCKED'
    assert api.view(other)["status"] == 'ACTIVE'
    invoke(service, 'activate', 'C1')
    assert invoke(service, "check", 'C1', context()).allowed
    assert invoke(service, "get", 'C1') is item

def test_repositories_are_independent():
    service, item = prepared()
    error("NOT_FOUND", lambda: invoke(api.create(), "get", 'C1'))

def test_checks_do_not_change_entity():
    service, item = prepared()
    before = api.view(item)
    invoke(service, "check", 'C1', context())
    invoke(service, "check", 'C1', context())
    assert api.view(item) == before

def test_closed_is_terminal():
    service, item = prepared()
    item.close()
    error("INVALID_STATE", item.activate)
    assert item.status == "CLOSED"
    assert invoke(service, "check", 'C1', context()).code == 'CUSTOMER_CLOSED'

def test_repeat_pause_does_not_change_status():
    service, item = prepared()
    item.block()
    error("INVALID_STATE", item.block)
    assert item.status == 'BLOCKED'

def test_status_is_read_only():
    service, item = prepared()
    with pytest.raises(AttributeError):
        item.status = "CLOSED"
def test_name_is_validated():
    error("INVALID_NAME", lambda: api.make("X", "   ", "STANDARD"))
    assert api.make("X", " Alice ", "STANDARD").name == "Alice"
