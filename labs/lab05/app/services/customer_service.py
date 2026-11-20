from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError
from app.domain.customer import Customer

class CustomerService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        self._rules = tuple(rules)

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
        customer = self.get(key)
        result = checked(customer.availability())
        if not result.allowed:
            return result
        for rule in self._rules:
            result = checked(rule.check(customer, context))
            if not result.allowed:
                return result
        return CheckResult(True)

    def check_many(self, customer_ids, context):
        return tuple((customer_id, self.check(customer_id, context)) for customer_id in customer_ids)

    def denial_codes(self, customer_ids, context):
        return tuple(dict.fromkeys(
            result.code
            for _, result in self.check_many(customer_ids, context)
            if not result.allowed
        ))

def make_entity(*args, **kwargs):
    return Customer(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'customer_id': entity.customer_id, 'name': entity.name, 'category': entity.category, 'online_consent': entity.online_consent, 'status': entity.status}
