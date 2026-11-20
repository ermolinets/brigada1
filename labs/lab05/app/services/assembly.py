from app.services.customer_service import CustomerService
from app.support.types import Repository
from app.domain.eligibility import AllowedCategoryRule, AllowedOperationRule

def build_service(repository=None, rules=None):
    repository = repository if repository is not None else Repository("customer_id")
    if rules is None:
        rules = (AllowedCategoryRule({"STANDARD", "PREMIUM"}), AllowedOperationRule({"PURCHASE"}))
    return CustomerService(repository, rules)
