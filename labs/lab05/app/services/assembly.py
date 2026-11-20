# ЛР5: стандартные зависимости пока создаёт сам сервис.
# Перенесите их сюда, сохранив явно переданные объекты.
from app.services.customer_service import CustomerService
from app.support.types import Repository
from app.domain.eligibility import AllowedCategoryRule, AllowedOperationRule

def build_service(repository=None, rules=None):
    repository = repository if repository is not None else Repository("customer_id")
    rules = () if rules is None else rules
    return CustomerService(repository, rules)
