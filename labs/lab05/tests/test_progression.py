import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from app import api
from app.support.errors import DomainError


def code(expected, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == expected

from app.domain.customer import Customer
from app.support.types import CustomerContext

def test_progression_availability_does_not_cache_state():
    service = api.create()
    item = Customer("C", "Alice", "STANDARD")

    service.register(item)
    first = service.check("C", CustomerContext())
    assert first.allowed
    item.block()
    assert service.check("C", CustomerContext()).code == "CUSTOMER_BLOCKED"
    item.activate()
    assert service.check("C", CustomerContext()).allowed
    assert first.allowed and item.status == "ACTIVE"

from app.domain.eligibility import CustomerEligibilityRule
from app.support.types import Repository, CheckResult
from app.services.customer_service import CustomerService

def test_progression_dependency_called_once_and_retained():
    calls = []
    class Once(CustomerEligibilityRule):
        def check(self, item, ctx):
            calls.append(item)
            if len(calls) == 1: raise DomainError("TEMPORARY")
            return CheckResult(True)
    rules = [Once()]
    repo = Repository("customer_id")
    item = Customer("C", "Alice", "STANDARD")

    repo.add(item)
    service = CustomerService(repo, rules)
    rules.clear()
    code("TEMPORARY", lambda: service.check("C", CustomerContext()))
    assert len(calls) == 1 and item.status == "ACTIVE"
    assert service.check("C", CustomerContext()).allowed and calls == [item, item]

from app.services.customer_service import CustomerService
from app.support.types import CheckResult

def test_progression_extra_lab05(monkeypatch):
    calls = []
    def check(self, customer_id, context):
        calls.append(customer_id)
        return CheckResult(False, "BLOCKED") if customer_id == "B" else CheckResult(True)
    monkeypatch.setattr(CustomerService, "check", check)
    service = object.__new__(CustomerService)
    values = service.check_many(["A", "B", "C"], object())
    assert tuple(key for key, _ in values) == ("A", "B", "C")
    assert tuple(result.allowed for _, result in values) == (True, False, True)
    assert service.denial_codes(["B", "B", "A"], object()) == ("BLOCKED",)
    assert calls == ["A", "B", "C", "B", "B", "A"]
