from app.support.types import CheckResult, checked, Repository
from app.domain.customer import Customer
from app.domain.eligibility import AllowedCategoryRule, AllowedOperationRule

class CustomerService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = tuple(rules) or (
            AllowedCategoryRule({"STANDARD", "PREMIUM"}),
            AllowedOperationRule({"PURCHASE"}),
        )

    def register(self, entity):
        return self._repository.add(entity)

    def get(self, key):
        return self._repository.get(key)

    def block(self, key):
        self.get(key).block()

    def activate(self, key):
        self.get(key).activate()

    def close(self, key):
        self.get(key).close()

    def check(self, key, context):
        entity = self.get(key)
        result = checked(entity.availability())
        if not result.allowed:
            return result
        for rule in self._rules:
            result = checked(rule.check(entity, context))
            if not result.allowed:
                return result
        return CheckResult(True)

def make_entity(*args, **kwargs):
    return Customer(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'customer_id': entity.customer_id, 'name': entity.name, 'category': entity.category, 'online_consent': entity.online_consent, 'status': entity.status}


def new_service(repository=None):
    return CustomerService(repository if repository is not None else Repository("customer_id"))
