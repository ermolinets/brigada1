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
        self.get(key).block()

    def activate(self, key):
        self.get(key).activate()

    def close(self, key):
        self.get(key).close()

    def check(self, key, context):
        raise NotImplementedError("ЛР5: реализуйте CustomerService.check по TASK.md")

    def check_many(self, customer_ids, context):
        raise NotImplementedError("ЛР5: реализуйте CustomerService.check_many по TASK.md")

    def denial_codes(self, customer_ids, context):
        raise NotImplementedError("ЛР5: реализуйте CustomerService.denial_codes по TASK.md")

def make_entity(*args, **kwargs):
    return Customer(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'customer_id': entity.customer_id, 'name': entity.name, 'category': entity.category, 'online_consent': entity.online_consent, 'status': entity.status}
