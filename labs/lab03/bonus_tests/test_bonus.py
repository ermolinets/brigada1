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

from app.domain.eligibility import AllowedCategoryRule
from app.support.types import CustomerContext

def test_configured_code():
    item = api.make('C1', "Alice", "STANDARD")
    assert AllowedCategoryRule(set(), code="CUSTOM").check(item, CustomerContext()).code == "CUSTOM"
