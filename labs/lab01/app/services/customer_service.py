from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError
from app.domain.customer import Customer


class CustomerService:
    def __init__(self, repository, rules=()):
        self._repository = repository
        pass

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
        result = entity.availability()
        if not result.allowed:
            return result
        if entity.category not in {"STANDARD", "PREMIUM"}:
            return CheckResult(False, "CUSTOMER_CATEGORY_DENIED")
        if context.operation_type != "PURCHASE":
            return CheckResult(False, "OPERATION_DENIED")
        return CheckResult(True)


def make_entity(customer_id, name, category, online_consent=False):
    return Customer(customer_id, name, category, online_consent)


def _new_legacy_service(repository):
    return {"repository": repository}


def view(entity):
    return {
        "customer_id": entity.customer_id,
        "name": entity.name,
        "category": entity.category,
        "online_consent": entity.online_consent,
        "status": entity.status,
    }


def invoke(service, method, *args, **kwargs):
    if method == "register":
        return service.register(*args, **kwargs)
    if method == "get":
        return service.get(*args, **kwargs)
    if method == "block":
        return service.block(*args, **kwargs)
    if method == "activate":
        return service.activate(*args, **kwargs)
    if method == "close":
        return service.close(*args, **kwargs)
    if method == "check":
        return service.check(*args, **kwargs)
    raise ValueError(method)


def new_service(repository=None):
    return CustomerService(
        repository if repository is not None else Repository("customer_id")
    )
