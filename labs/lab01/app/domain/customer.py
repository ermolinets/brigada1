# ЛР1: поля, конструктор и служебные проверки даны преподавателем.
# Завершите отмеченные методы; API пока использует старые функции.
from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError


class Customer:
    def __init__(self, customer_id, name, category, online_consent=False):
        identifier(customer_id)
        name = valid_name(name)
        choice(category, ("STANDARD", "PREMIUM", "BUSINESS"), "INVALID_CATEGORY")
        boolean(online_consent)
        self._customer_id = customer_id
        self._name = name
        self._category = category
        self._online_consent = online_consent
        self._status = "ACTIVE"

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def online_consent(self):
        return self._online_consent

    @property
    def status(self):
        return self._status

    def block(self):
        if self.status != "ACTIVE":
            raise DomainError("INVALID_STATE")
        self._status = "BLOCKED"

    def activate(self):
        if self.status != "BLOCKED":
            raise DomainError("INVALID_STATE")
        self._status = "ACTIVE"

    def close(self):
        if self.status not in ('ACTIVE', 'BLOCKED'):
            raise DomainError("INVALID_STATE")
        self._status = "CLOSED"

    def availability(self):
        if self.status == "BLOCKED":
            return CheckResult(False, "CUSTOMER_BLOCKED")
        if self.status == "CLOSED":
            return CheckResult(False, "CUSTOMER_CLOSED")
        return CheckResult(True)
