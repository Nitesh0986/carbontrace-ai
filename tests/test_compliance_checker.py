from backend.services.compliance_checker import check_compliance


def test_compliance_passes_valid_calculation():

    records = [
        {
            "activity": "diesel",
            "quantity": 300,
            "emission_factor": 2.5,
            "emissions_kg_co2e": 750,
            "scope": 1,
        }
    ]

    result = check_compliance(
        records,
        "The company consumed diesel."
    )

    assert result["overall_risk"] == "MEDIUM"

    calculation_finding = next(
        finding
        for finding in result["findings"]
        if finding["type"] == "calculation"
    )

    assert calculation_finding["status"] == "PASS"


def test_compliance_detects_calculation_error():

    records = [
        {
            "activity": "diesel",
            "quantity": 300,
            "emission_factor": 2.5,
            "emissions_kg_co2e": 700,
            "scope": 1,
        }
    ]

    result = check_compliance(
        records,
        "The company consumed diesel."
    )

    assert result["overall_risk"] == "HIGH"


def test_detects_greenwashing_claim():

    records = [
        {
            "activity": "electricity",
            "quantity": 1000,
            "emission_factor": 0.5,
            "emissions_kg_co2e": 500,
            "scope": 2,
        }
    ]

    result = check_compliance(
        records,
        "The company uses 100% renewable energy."
    )

    greenwashing = next(
        finding
        for finding in result["findings"]
        if finding["type"] == "greenwashing"
    )

    assert greenwashing["status"] == "REVIEW"
    assert "100% renewable" in greenwashing["claims"]


def test_valid_scopes_pass():

    records = [
        {
            "activity": "electricity",
            "quantity": 1000,
            "emission_factor": 0.5,
            "emissions_kg_co2e": 500,
            "scope": 2,
        }
    ]

    result = check_compliance(
        records,
        "Purchased electricity."
    )

    scope_finding = next(
        finding
        for finding in result["findings"]
        if finding["type"] == "scope"
    )

    assert scope_finding["status"] == "PASS"