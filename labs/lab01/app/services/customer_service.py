# ЛР1: заготовленный сервис. Допишите отмеченный метод и подключите объекты.
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
        raise NotImplementedError("ЛР1: завершите CustomerService.block")

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


from app.support.types import Repository



from app.support.types import CheckResult, checked, identifier, choice, boolean, date_only, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError

def make_entity(customer_id, name, category, online_consent=False):
    return {'customer_id': customer_id, 'name': name, 'category': category, 'online_consent': online_consent, "status": "ACTIVE"}

def _new_legacy_service(repository):
    return {"repository": repository}

def view(entity):
    return dict(entity)

def invoke(service, method, *args, **kwargs):
    repository = service["repository"]
    if method == "register":
        return repository.add(args[0])
    entity = repository.get(args[0])
    if method == "get":
        return entity
    if method == "block":
        entity["status"] = "BLOCKED"
        return None
    if method == "activate":
        entity["status"] = "ACTIVE"
        return None
    if method == "close":
        entity["status"] = "CLOSED"
        return None
    if method == "check":
        context = args[1]
        if entity["status"] != "ACTIVE":
            return CheckResult(False, "CUSTOMER_" + ("NOT_ACTIVE" if entity["status"] == "NEW" else entity["status"]))
        if entity["category"] not in {"STANDARD", "PREMIUM"}:
            return CheckResult(False, "CUSTOMER_CATEGORY_DENIED")
        if context.operation_type != "PURCHASE":
            return CheckResult(False, "OPERATION_DENIED")
        return CheckResult(True)
    raise ValueError(method)


from app.support.types import Repository

def new_service(repository=None):
    return _new_legacy_service(repository if repository is not None else Repository("customer_id"))