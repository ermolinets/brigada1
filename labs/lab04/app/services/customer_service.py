from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError
from app.domain.customer import Customer
from app.domain.eligibility import AllowedCategoryRule, AllowedOperationRule

class CustomerService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = [AllowedCategoryRule({"STANDARD", "PREMIUM"}), AllowedOperationRule({"PURCHASE"})]  # конкретные объекты пока создаются здесь

    def register(self, entity):
        return self._repository.add(entity)

    def get(self, key):
        return self._repository.get(key)

    def block(self, key):
        entity = self.get(key)
        if entity.status not in ('ACTIVE',):
            raise DomainError("INVALID_STATE")
        entity._status = "BLOCKED"

    def activate(self, key):
        entity = self.get(key)
        if entity.status not in ('BLOCKED',):
            raise DomainError("INVALID_STATE")
        entity._status = "ACTIVE"

    def close(self, key):
        entity = self.get(key)
        if entity.status not in ('ACTIVE', 'BLOCKED'):
            raise DomainError("INVALID_STATE")
        entity._status = "CLOSED"

    def check(self, key, context):
        entity = self.get(key)
        if entity.status != "ACTIVE":
            return CheckResult(False, "CUSTOMER_" + ("NOT_ACTIVE" if entity.status == "NEW" else entity.status))
        for rule in self._rules:
            result = checked(rule.check(entity, context))
            if not result.allowed:
                return result
        return CheckResult(True)

    def diagnostic(self, key):
        self._repository.get(key)
        return self._repository.get(key).name

def make_entity(*args, **kwargs):
    return Customer(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'customer_id': entity.customer_id, 'name': entity.name, 'category': entity.category, 'online_consent': entity.online_consent, 'status': entity.status}


from app.support.types import Repository

def new_service(repository=None):
    return CustomerService(repository if repository is not None else Repository("customer_id"))
