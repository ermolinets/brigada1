# Исходные проверки ЛР5

Успешных проверок: **17**. Ожидаемых падений: **11**.

Не завершены использование переданных зависимостей, сборка и основной путь операции. Проверки вызывают разные конфигурации и ошибающегося исполнителя; ошибка не должна превращаться в успешный результат или повторную операцию.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_availability_does_not_cache_state`
- `tests.test_progression::test_progression_dependency_called_once_and_retained`
- `tests.test_progression::test_progression_extra_lab05`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_basic_lifecycle_and_isolation`
- `tests.test_contract::test_checks_do_not_change_entity`
- `tests.test_contract::test_closed_is_terminal`
- `tests.test_contract::test_dependency_failure_is_not_permission`
- `tests.test_contract::test_injection_and_container_copy`
- `tests.test_contract::test_rules_used_by_service`
- `tests.test_contract::test_wrong_rule_result_is_rejected`
- `tests.test_review_contract::test_review_first_refusal_and_mandatory_availability`

## Порядок проверки

Из корня проекта: `python check.py lab05`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
