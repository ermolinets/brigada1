from abc import ABC, abstractmethod
from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError

class CustomerEligibilityRule(ABC):
    @abstractmethod
    def check(self, entity, context):
        raise NotImplementedError

class AllowedCategoryRule(CustomerEligibilityRule):
    def __init__(self, values):
        self._values = frozenset(values)
        for value in self._values:
            choice(value, ('STANDARD', 'PREMIUM', 'BUSINESS'), "INVALID_CONFIG")

    def check(self, entity, context):
        if entity.category not in self._values:
            return CheckResult(False, 'CUSTOMER_CATEGORY_DENIED')
        return CheckResult(True)

class AllowedOperationRule(CustomerEligibilityRule):
    def __init__(self, values):
        self._values = frozenset(values)
        for value in self._values:
            choice(value, ('PURCHASE', 'CASH_WITHDRAWAL'), "INVALID_CONFIG")

    def check(self, entity, context):
        if context.operation_type not in self._values:
            return CheckResult(False, 'OPERATION_DENIED')
        return CheckResult(True)
