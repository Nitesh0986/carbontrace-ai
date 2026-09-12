"""
CarbonTrace AI
Compliance & Greenwashing Checker

Checks emission records and document text for:
- Calculation validation
- Scope validation
- Emission-factor verification status
- Unsupported environmental claims
"""


import re


def check_compliance(
    records: list[dict],
    document_text: str,
) -> dict:
    """
    Perform basic ESG compliance checks.
    """

    findings = []

    # --------------------------------------------------
    # 1. Validate calculations
    # --------------------------------------------------

    calculation_errors = []

    for record in records:

        expected = (
            record["quantity"]
            * record["emission_factor"]
        )

        actual = record["emissions_kg_co2e"]

        if abs(expected - actual) > 0.000001:

            calculation_errors.append(
                record["activity"]
            )

    if calculation_errors:

        findings.append({
            "type": "calculation",
            "severity": "HIGH",
            "status": "FAIL",
            "message": (
                "Emission calculation mismatch detected."
            ),
            "activities": calculation_errors,
        })

    else:

        findings.append({
            "type": "calculation",
            "severity": "LOW",
            "status": "PASS",
            "message": (
                "All emission calculations "
                "were verified deterministically."
            ),
        })


    # --------------------------------------------------
    # 2. Validate scopes
    # --------------------------------------------------

    invalid_scopes = []

    for record in records:

        if record["scope"] not in {1, 2, 3}:

            invalid_scopes.append(
                record["activity"]
            )

    if invalid_scopes:

        findings.append({
            "type": "scope",
            "severity": "HIGH",
            "status": "FAIL",
            "message": (
                "Invalid emission scope detected."
            ),
            "activities": invalid_scopes,
        })

    else:

        findings.append({
            "type": "scope",
            "severity": "LOW",
            "status": "PASS",
            "message": (
                "All emission activities have "
                "valid Scope 1, 2, or 3 classifications."
            ),
        })


    # --------------------------------------------------
    # 3. Emission factor verification
    # --------------------------------------------------

    findings.append({
        "type": "emission_factor",
        "severity": "MEDIUM",
        "status": "REVIEW",
        "message": (
            "Emission factors were retrieved from the "
            "configured factor dataset. Verify the "
            "factor source and version before formal reporting."
        ),
    })


    # --------------------------------------------------
    # 4. Greenwashing / unsupported claims
    # --------------------------------------------------

    text = document_text.lower()

    green_claim_patterns = [
        r"\b100%\s+renewable\b",
        r"\bcarbon[- ]neutral\b",
        r"\bnet[- ]zero\b",
        r"\bzero[- ]carbon\b",
        r"\bcarbon[- ]free\b",
        r"\bgreen\s+energy\b",
    ]

    detected_claims = []

    for pattern in green_claim_patterns:

        matches = re.findall(pattern, text)

        for match in matches:
            detected_claims.append(match)


    if detected_claims:

        findings.append({
            "type": "greenwashing",
            "severity": "MEDIUM",
            "status": "REVIEW",
            "message": (
                "Environmental claim detected. "
                "Supporting evidence should be verified "
                "before accepting the claim."
            ),
            "claims": detected_claims,
        })

    else:

        findings.append({
            "type": "greenwashing",
            "severity": "LOW",
            "status": "PASS",
            "message": (
                "No high-risk environmental marketing "
                "claims were detected in the document."
            ),
        })


    # --------------------------------------------------
    # Overall risk
    # --------------------------------------------------

    severities = [
        finding["severity"]
        for finding in findings
        if finding["status"] != "PASS"
    ]

    if "HIGH" in severities:

        overall_risk = "HIGH"

    elif "MEDIUM" in severities:

        overall_risk = "MEDIUM"

    else:

        overall_risk = "LOW"


    return {
        "overall_risk": overall_risk,
        "findings": findings,
    }