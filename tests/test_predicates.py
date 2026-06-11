from cak.predicates import Truth, evaluate, evaluate_all


def test_numeric_comparisons() -> None:
    context = {"amount": 500}
    assert evaluate("amount > 0", context) is Truth.TRUE
    assert evaluate("amount > 10000", context) is Truth.FALSE
    assert evaluate("amount <= 500", context) is Truth.TRUE
    assert evaluate("amount != 500", context) is Truth.FALSE


def test_string_equality_and_nesting() -> None:
    context = {"invoice": {"status": "draft", "id": "inv_001"}}
    assert evaluate('invoice.status == "draft"', context) is Truth.TRUE
    assert evaluate('invoice.status == "sent"', context) is Truth.FALSE
    assert evaluate("invoice.id.present", context) is Truth.TRUE
    assert evaluate("invoice.missing.present", context) is Truth.FALSE


def test_unevaluable_is_unknown_not_a_guess() -> None:
    context = {"amount": 500}
    assert evaluate("customer.exists(email=x)", context) is Truth.UNKNOWN
    assert evaluate("missing_field > 3", context) is Truth.UNKNOWN
    assert evaluate("amount > not_a_literal", context) is Truth.UNKNOWN


def test_type_mismatch_is_unknown() -> None:
    assert evaluate("amount > 10", {"amount": "lots"}) is Truth.UNKNOWN


def test_evaluate_all_preserves_predicates() -> None:
    results = evaluate_all(["amount > 0", "due_date.present"], {"amount": 1})
    assert results["amount > 0"] is Truth.TRUE
    assert results["due_date.present"] is Truth.FALSE
