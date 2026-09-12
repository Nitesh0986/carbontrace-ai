from backend.services.scope_classifier import classify_scope


def test_company_owned_diesel():
    result = classify_scope(
        "diesel",
        "company-owned truck"
    )

    assert result == 1


def test_purchased_electricity():
    result = classify_scope(
        "electricity",
        "purchased electricity"
    )

    assert result == 2


def test_third_party_freight():
    result = classify_scope(
        "freight",
        "third-party logistics provider"
    )

    assert result == 3


def test_business_travel():
    result = classify_scope(
        "business_travel",
        "employee business flight"
    )

    assert result == 3