from app.domain.eligibility import CustomerEligibilityRule
from app.support.types import CheckResult

class LegacyAdapter(CustomerEligibilityRule):
    def __init__(self, legacy):
        self._legacy = legacy

    def check(self, entity, context):
        raise NotImplementedError("Бонус: локальный адаптер")
