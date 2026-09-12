/* =======================================
   CarbonTrace AI
   Frontend Application
======================================= */


/* =======================================
   DOM Elements
======================================= */

const pdfFile =
    document.getElementById("pdfFile");

const fileName =
    document.getElementById("fileName");

const processBtn =
    document.getElementById("processBtn");

const message =
    document.getElementById("message");

const dashboard =
    document.getElementById("dashboard");


/* =======================================
   Dashboard Elements
======================================= */

const totalEmission =
    document.getElementById("totalEmission");

const scope1 =
    document.getElementById("scope1");

const scope2 =
    document.getElementById("scope2");

const scope3 =
    document.getElementById("scope3");

const recordsContainer =
    document.getElementById("records");

const auditContainer =
    document.getElementById("audit");


/* =======================================
   Compliance Elements
======================================= */

const riskSummary =
    document.getElementById("riskSummary");

const complianceFindings =
    document.getElementById("complianceFindings");


/* =======================================
   File Selection
======================================= */

pdfFile.addEventListener(
    "change",
    () => {

        if (pdfFile.files.length > 0) {

            fileName.textContent =
                pdfFile.files[0].name;

            message.textContent =
                "PDF selected. Ready to process.";

        } else {

            fileName.textContent =
                "No file selected";

            message.textContent =
                "";

        }

    }
);


/* =======================================
   Process PDF
======================================= */

processBtn.addEventListener(
    "click",
    async () => {

        /* ---------------------------------
           Check file selection
        --------------------------------- */

        if (pdfFile.files.length === 0) {

            message.textContent =
                "Please select a PDF first.";

            return;
        }


        /* ---------------------------------
           Get selected file
        --------------------------------- */

        const file =
            pdfFile.files[0];


        /* ---------------------------------
           Create FormData
        --------------------------------- */

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );


        /* ---------------------------------
           Disable button
        --------------------------------- */

        processBtn.disabled = true;

        message.textContent =
            "Processing document...";


        try {

            /* -----------------------------
               Send PDF to FastAPI
            ----------------------------- */

            const response =
                await fetch(
                    "/emissions",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            /*
             * Read response as text first.
             *
             * This prevents:
             * "Unexpected end of JSON input"
             *
             * when the backend returns
             * an empty or invalid response.
             */

            const responseText =
                await response.text();


            /* -----------------------------
               Parse JSON safely
            ----------------------------- */

            let data;

            try {

                data =
                    JSON.parse(responseText);

            } catch {

                throw new Error(
                    "Server returned an invalid response."
                );

            }


            /* -----------------------------
               Check HTTP status
            ----------------------------- */

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Processing failed"
                );

            }


            /* -----------------------------
               Display dashboard
            ----------------------------- */

            displayDashboard(data);


            message.textContent =
                "Document processed successfully.";

        }


        catch (error) {

            console.error(error);

            message.textContent =
                "Error: " + error.message;

        }


        finally {

            processBtn.disabled = false;

        }

    }
);


/* =======================================
   Display Dashboard
======================================= */

function displayDashboard(data) {

    /* ------------------------------------
       Show dashboard
    ------------------------------------ */

    dashboard.classList.remove(
        "hidden"
    );


    /* ------------------------------------
       Emission Summary
    ------------------------------------ */

    totalEmission.textContent =
        formatNumber(
            data.total_kg_co2e
        );


    scope1.textContent =
        formatNumber(
            data.scope_1_kg_co2e
        );


    scope2.textContent =
        formatNumber(
            data.scope_2_kg_co2e
        );


    scope3.textContent =
        formatNumber(
            data.scope_3_kg_co2e
        );


    /* ------------------------------------
       Emission Records
    ------------------------------------ */

    displayRecords(
        data.records || []
    );


    /* ------------------------------------
       Audit Trail
    ------------------------------------ */

    displayAudit(
        data.records || []
    );


    /* ------------------------------------
       Compliance
    ------------------------------------ */

    if (data.compliance) {

        displayCompliance(
            data.compliance
        );

    } else {

        displayComplianceUnavailable();

    }


    /* ------------------------------------
       Scroll to dashboard
    ------------------------------------ */

    dashboard.scrollIntoView({
        behavior: "smooth"
    });

}


/* =======================================
   Emission Records
======================================= */

function displayRecords(records) {

    recordsContainer.innerHTML = "";


    if (records.length === 0) {

        recordsContainer.innerHTML =
            "<p>No emission records found.</p>";

        return;
    }


    records.forEach(
        record => {

            const div =
                document.createElement("div");


            div.className =
                "record";


            div.innerHTML = `

                <div>

                    <strong>
                        ${record.activity}
                    </strong>

                    <br>

                    ${record.quantity}
                    ${record.unit}

                </div>


                <div class="scope">

                    Scope ${record.scope}

                    <br>

                    ${formatNumber(
                        record.emissions_kg_co2e
                    )}

                    kg CO₂e

                </div>

            `;


            recordsContainer.appendChild(
                div
            );

        }
    );

}


/* =======================================
   Audit Trail
======================================= */

function displayAudit(records) {

    auditContainer.innerHTML = "";


    if (records.length === 0) {

        auditContainer.innerHTML =
            "<p>No audit records found.</p>";

        return;
    }


    records.forEach(
        (record, index) => {

            const div =
                document.createElement("div");


            div.className =
                "audit-record";


            div.innerHTML = `

                <strong>
                    Audit Record #${index + 1}
                </strong>


                <p>

                    <strong>
                        Record ID:
                    </strong>

                    ${record.record_id || "N/A"}

                </p>


                <p>

                    <strong>
                        Source Document:
                    </strong>

                    ${record.source_document ||
                    "Uploaded ESG Document"}

                </p>


                <p>

                    <strong>
                        Activity:
                    </strong>

                    ${record.activity || "N/A"}

                </p>


                <p>

                    <strong>
                        Quantity:
                    </strong>

                    ${record.quantity || 0}
                    ${record.unit || ""}

                </p>


                <p>

                    <strong>
                        Context:
                    </strong>

                    ${record.context || "N/A"}

                </p>


                <p>

                    <strong>
                        Scope:
                    </strong>

                    Scope ${record.scope || "N/A"}

                </p>


                <p>

                    <strong>
                        Emission Factor:
                    </strong>

                    ${record.emission_factor ?? "N/A"}
                    ${record.factor_unit || ""}

                </p>


                <p>

                    <strong>
                        Factor Source:
                    </strong>

                    ${record.factor_source ||
                    "Configured emission-factor dataset"}

                </p>


                <p>

                    <strong>
                        Factor Version:
                    </strong>

                    ${record.factor_version ||
                    "N/A"}

                </p>


                <p>

                    <strong>
                        Calculation:
                    </strong>

                    ${record.calculation ||
                    `${record.quantity} × ${record.emission_factor}`}

                </p>


                <p>

                    <strong>
                        Result:
                    </strong>

                    ${formatNumber(
                        record.emissions_kg_co2e
                    )}

                    kg CO₂e

                </p>


                <p>

                    <strong>
                        Validation:
                    </strong>

                    ${record.validation_status ||
                    "VALIDATED"}

                </p>


                <p>

                    <strong>
                        Timestamp:
                    </strong>

                    ${record.timestamp ||
                    "N/A"}

                </p>

            `;


            auditContainer.appendChild(
                div
            );

        }
    );

}


/* =======================================
   Compliance Results
======================================= */

function displayCompliance(
    compliance
) {

    /* ------------------------------------
       Clear previous results
    ------------------------------------ */

    riskSummary.innerHTML = "";

    complianceFindings.innerHTML = "";


    /* ------------------------------------
       Overall Risk
    ------------------------------------ */

    const risk =
        document.createElement("div");


    risk.className =
        "risk-card";


    risk.innerHTML = `

        <h3>
            Overall Compliance Risk
        </h3>


        <div class="risk-level">

            ${compliance.overall_risk || "REVIEW"}

        </div>

    `;


    riskSummary.appendChild(
        risk
    );


    /* ------------------------------------
       Individual Findings
    ------------------------------------ */

    const findings =
        compliance.findings || [];


    if (findings.length === 0) {

        complianceFindings.innerHTML = `
            <div class="warning">
                No compliance findings were returned.
            </div>
        `;

        return;
    }


    findings.forEach(
        finding => {

            const div =
                document.createElement("div");


            /* --------------------------------
               Determine CSS class
            -------------------------------- */

            if (
                finding.status === "PASS"
            ) {

                div.className =
                    "success";

            }

            else if (
                finding.severity === "HIGH"
            ) {

                div.className =
                    "danger";

            }

            else {

                div.className =
                    "warning";

            }


            /* --------------------------------
               Format finding title
            -------------------------------- */

            const title =
                String(
                    finding.type ||
                    "COMPLIANCE CHECK"
                )
                .replaceAll(
                    "_",
                    " "
                )
                .toUpperCase();


            /* --------------------------------
               Main finding
            -------------------------------- */

            div.innerHTML = `

                <strong>
                    ${title}
                </strong>


                <br><br>


                <strong>
                    Status:
                </strong>

                ${finding.status || "REVIEW"}


                <br>


                <strong>
                    Severity:
                </strong>

                ${finding.severity || "MEDIUM"}


                <br><br>


                ${finding.message || ""}

            `;


            /* --------------------------------
               Detected Claims
            -------------------------------- */

            if (
                finding.claims &&
                finding.claims.length > 0
            ) {

                div.innerHTML += `

                    <br><br>

                    <strong>
                        Detected Claims:
                    </strong>

                    ${finding.claims.join(
                        ", "
                    )}

                `;

            }


            /* --------------------------------
               Affected Activities
            -------------------------------- */

            if (
                finding.activities &&
                finding.activities.length > 0
            ) {

                div.innerHTML += `

                    <br><br>

                    <strong>
                        Affected Activities:
                    </strong>

                    ${finding.activities.join(
                        ", "
                    )}

                `;

            }


            complianceFindings.appendChild(
                div
            );

        }
    );

}


/* =======================================
   Compliance Unavailable
======================================= */

function displayComplianceUnavailable() {

    riskSummary.innerHTML = `

        <div class="risk-card">

            <h3>
                Overall Compliance Risk
            </h3>

            <div class="risk-level">
                REVIEW
            </div>

        </div>

    `;


    complianceFindings.innerHTML = `

        <div class="warning">

            Compliance results were not returned
            by the backend.

        </div>

    `;

}


/* =======================================
   Number Formatting
======================================= */

function formatNumber(number) {

    return Number(
        number || 0
    ).toLocaleString(
        undefined,
        {
            maximumFractionDigits: 2
        }
    );

}