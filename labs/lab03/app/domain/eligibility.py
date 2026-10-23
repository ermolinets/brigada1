from abc import ABC, abstractmethod
from app.support.types import CheckResult, choice, result_code

class CustomerEligibilityRule(ABC):
    @abstractmethod
    def check(self, entity, context):
        raise NotImplementedError

class AllowedCategoryRule(CustomerEligibilityRule):
    def __init__(self, values, code="CUSTOMER_CATEGORY_DENIED"):
        self._code = result_code(code)
        self._values = frozenset(values)
        for value in self._values:
            choice(value, ('STANDARD', 'PREMIUM', 'BUSINESS'), "INVALID_CONFIG")

    def check(self, entity, context):
        if entity.category not in self._values:
            return CheckResult(False, self._code)
        return CheckResult(True)

class AllowedOperationRule(CustomerEligibilityRule):
    def __init__(self, values):
        self._values = frozenset(values)
        for value in self._values:
            choice(value, ('PURCHASE', 'CASH_WITHDRAWAL'), "INVALID_CONFIG")

    def check(self, entity, context):
        return CheckResult(True)
