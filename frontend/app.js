(function () {

    "use strict";


    // =========================================================
    // CARBONTRACE AI
    // Frontend Application
    // =========================================================


    const API_BASE_URL =
        window.location.origin;


    // =========================================================
    // APPLICATION STATE
    // =========================================================

    let currentFile = null;

    let currentResult = null;

    let currentRecords = [];

    let currentAuditRecords = [];



    // =========================================================
    // DOM HELPERS
    // =========================================================

    function getElement(id) {

        return document.getElementById(id);

    }


    function setText(id, value) {

        const element =
            getElement(id);

        if (element) {

            element.textContent =
                value;

        }

    }


    function setHTML(id, value) {

        const element =
            getElement(id);

        if (element) {

            element.innerHTML =
                value;

        }

    }


    function setWidth(id, value) {

        const element =
            getElement(id);

        if (!element) {

            return;

        }


        const safeValue =
            Math.max(
                0,
                Math.min(
                    100,
                    Number(value) || 0
                )
            );


        element.style.width =
            `${safeValue}%`;

    }



    // =========================================================
    // FORMATTING
    // =========================================================

    function numberValue(value) {

        const number =
            Number(value);

        return Number.isFinite(number)
            ? number
            : 0;

    }


    function formatNumber(
        value,
        decimals = 2
    ) {

        const number =
            Number(value);

        if (!Number.isFinite(number)) {

            return "--";

        }


        return number.toLocaleString(
            undefined,
            {
                minimumFractionDigits:
                    decimals,

                maximumFractionDigits:
                    decimals
            }
        );

    }


    function formatKg(value) {

        return (
            formatNumber(value, 2) +
            " kg CO₂e"
        );

    }


    function escapeHTML(value) {

        if (
            value === null ||
            value === undefined
        ) {

            return "";

        }


        return String(value)
            .replace(
                /&/g,
                "&amp;"
            )
            .replace(
                /</g,
                "&lt;"
            )
            .replace(
                />/g,
                "&gt;"
            )
            .replace(
                /"/g,
                "&quot;"
            )
            .replace(
                /'/g,
                "&#039;"
            );

    }



    // =========================================================
    // STATUS CLASS
    // =========================================================

    function getStatusClass(status) {

        const value =
            String(status || "")
                .toUpperCase();


        if (
            value === "PASS" ||
            value === "LOW" ||
            value === "READY" ||
            value === "VALIDATED" ||
            value === "VERIFIED"
        ) {

            return "status-pass";

        }


        if (
            value === "REVIEW" ||
            value === "MEDIUM" ||
            value === "PENDING"
        ) {

            return "status-review";

        }


        if (
            value === "FAIL" ||
            value === "HIGH" ||
            value === "BLOCKED" ||
            value === "ERROR"
        ) {

            return "status-fail";

        }


        return "status-neutral";

    }



    // =========================================================
    // HEALTH CHECK
    // =========================================================

    async function checkHealth() {

        const health =
            getElement(
                "health-status"
            );


        try {

            const response =
                await fetch(
                    `${API_BASE_URL}/health`
                );


            if (!response.ok) {

                throw new Error(
                    "Health endpoint failed"
                );

            }


            const data =
                await response.json();


            if (health) {

                if (
                    data.status === "ok"
                ) {

                    health.textContent =
                        "API Online";

                } else {

                    health.textContent =
                        "API Unavailable";

                }

            }


            return data;

        }

        catch (error) {

            console.error(
                "Health check error:",
                error
            );


            if (health) {

                health.textContent =
                    "API Offline";

            }


            return null;

        }

    }



    // =========================================================
    // LYZR STATUS
    // =========================================================

    async function checkLyzrStatus() {

        const badge =
            getElement(
                "lyzr-status-badge"
            );


        const pill =
            getElement(
                "lyzr-status-pill"
            );


        const pulse =
            getElement(
                "agent-pulse"
            );


        if (badge) {

            badge.textContent =
                "CHECKING...";

        }


        try {

            const response =
                await fetch(
                    `${API_BASE_URL}/lyzr-status`
                );


            if (!response.ok) {

                throw new Error(
                    "Lyzr status failed"
                );

            }


            const data =
                await response.json();


            const status =
                String(
                    data.agent ||
                    data.status ||
                    "READY"
                ).toUpperCase();


            const ready =
                status === "READY" ||
                status === "HEALTHY";


            if (badge) {

                badge.textContent =
                    ready
                        ? "LYZR READY"
                        : status;

            }


            if (pill) {

                pill.textContent =
                    ready
                        ? "● Lyzr Ready"
                        : "● Lyzr Not Ready";

            }


            if (pulse) {

                pulse.textContent =
                    ready
                        ? "●"
                        : "○";

            }


            return data;

        }

        catch (error) {

            console.error(
                "Lyzr status error:",
                error
            );


            if (badge) {

                badge.textContent =
                    "LYZR NOT READY";

            }


            if (pill) {

                pill.textContent =
                    "● Lyzr Unavailable";

            }


            return null;

        }

    }



    // =========================================================
    // RESET DASHBOARD
    // =========================================================

    function resetDashboard() {

        setText(
            "kpi-total-co2e",
            "0"
        );

        setText(
            "kpi-scope1",
            "0"
        );

        setText(
            "kpi-scope2",
            "0"
        );

        setText(
            "kpi-scope3",
            "0"
        );

        setText(
            "kpi-records-count",
            "0"
        );

        setText(
            "kpi-pass-rate",
            "—"
        );


        setText(
            "dist-scope1-text",
            "0%"
        );

        setText(
            "dist-scope2-text",
            "0%"
        );

        setText(
            "dist-scope3-text",
            "0%"
        );


        setWidth(
            "dist-scope1-bar",
            0
        );

        setWidth(
            "dist-scope2-bar",
            0
        );

        setWidth(
            "dist-scope3-bar",
            0
        );


        setText(
            "data-quality-score",
            "—"
        );

        setText(
            "metric-primary-share",
            "—"
        );

        setText(
            "metric-temporal-correlation",
            "—"
        );

        setText(
            "metric-geo-match",
            "—"
        );


        setText(
            "factor-source",
            "—"
        );

        setText(
            "factor-vintage",
            "—"
        );

        setText(
            "factor-methodology",
            "—"
        );

        setText(
            "factor-region",
            "—"
        );

        setText(
            "factor-value",
            "—"
        );

        setText(
            "factor-status",
            "—"
        );


        setHTML(
            "emission-table-body",
            `
            <tr>
                <td colspan="7">
                    No records loaded yet.
                </td>
            </tr>
            `
        );


        setText(
            "table-row-count",
            "0 records"
        );


        setHTML(
            "audit-trail-container",
            `
            <p>
                No audit records yet.
            </p>
            `
        );

    }



    // =========================================================
    // FILE INPUT
    // =========================================================

    function setupFileInput() {

        const input =
            getElement(
                "document-file-input"
            );


        const fileName =
            getElement(
                "selected-file-name"
            );


        if (!input) {

            console.error(
                "❌ document-file-input not found"
            );

            return;

        }


        console.log(
            "✅ File input connected"
        );


        input.addEventListener(
            "change",
            function (event) {

                const files =
                    event.target.files;


                if (
                    !files ||
                    files.length === 0
                ) {

                    currentFile =
                        null;


                    if (fileName) {

                        fileName.textContent =
                            "No file selected";

                    }

                    return;

                }


                const file =
                    files[0];


                currentFile =
                    file;


                console.log(
                    "📄 Selected file:",
                    file.name
                );


                console.log(
                    "📦 File type:",
                    file.type
                );


                console.log(
                    "📏 File size:",
                    file.size
                );


                if (fileName) {

                    fileName.textContent =
                        file.name;

                }


                setText(
                    "upload-status",
                    `Selected: ${file.name}`
                );


                setText(
                    "message",
                    ""
                );

            }
        );

    }



    // =========================================================
    // FILE VALIDATION
    // =========================================================

    function validateFile(file) {

        if (!file) {

            return {
                valid: false,
                message:
                    "Please select a PDF or CSV file first."
            };

        }


        const name =
            String(
                file.name || ""
            ).toLowerCase();


        const validPDF =
            name.endsWith(".pdf");


        const validCSV =
            name.endsWith(".csv");


        if (
            !validPDF &&
            !validCSV
        ) {

            return {
                valid: false,
                message:
                    "Only PDF and CSV files are supported."
            };

        }


        return {
            valid: true,
            message: ""
        };

    }



    // =========================================================
    // PROGRESS
    // =========================================================

    function showProgress(
        percentage
    ) {

        const wrapper =
            getElement(
                "upload-progress-wrapper"
            );


        const bar =
            getElement(
                "upload-progress-bar"
            );


        const pct =
            getElement(
                "upload-pct"
            );


        if (wrapper) {

            wrapper.style.display =
                "block";

        }


        if (bar) {

            bar.style.width =
                `${percentage}%`;

        }


        if (pct) {

            pct.textContent =
                `${percentage}%`;

        }

    }



    // =========================================================
    // UPLOAD DOCUMENT
    // =========================================================

    async function uploadDocument(
        file
    ) {

        const validation =
            validateFile(file);


        if (!validation.valid) {

            alert(
                validation.message
            );

            return;

        }


        currentFile =
            file;


        const button =
            getElement(
                "btn-upload-ingest"
            );


        const status =
            getElement(
                "upload-status"
            );


        if (button) {

            button.disabled =
                true;

            button.textContent =
                "Processing...";

        }


        setText(
            "selected-file-name",
            file.name
        );


        setText(
            "upload-status",
            "Preparing document..."
        );


        showProgress(10);


        const formData =
            new FormData();


        /*
         * IMPORTANT:
         *
         * FastAPI backend expects:
         *
         * file
         *
         * Therefore:
         *
         * formData.append("file", file)
         */

        formData.append(
            "file",
            file
        );


        try {

            setText(
                "upload-status",
                "Uploading document..."
            );


            showProgress(25);


            console.log(
                "🚀 Sending file to:",
                `${API_BASE_URL}/emissions`
            );


            const response =
                await fetch(
                    `${API_BASE_URL}/emissions`,
                    {
                        method: "POST",
                        body: formData
                    }
                );


            console.log(
                "📡 Backend status:",
                response.status
            );


            showProgress(50);


            const contentType =
                response.headers.get(
                    "content-type"
                ) || "";


            let data;


            if (
                contentType.includes(
                    "application/json"
                )
            ) {

                data =
                    await response.json();

            } else {

                const text =
                    await response.text();


                data = {
                    detail: text
                };

            }


            console.log(
                "📊 Backend response:",
                data
            );


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    data.message ||
                    `Backend error: ${response.status}`
                );

            }


            showProgress(75);


            setText(
                "upload-status",
                "Document processed. Rendering results..."
            );


            currentResult =
                data;


            renderResult(
                data
            );


            showProgress(100);


            setText(
                "upload-status",
                "✓ Processing complete"
            );


            setText(
                "message",
                "Document successfully processed."
            );


            console.log(
                "✅ CarbonTrace processing complete"
            );

        }

        catch (error) {

            console.error(
                "❌ Upload error:",
                error
            );


            showProgress(100);


            setText(
                "upload-status",
                "Processing failed"
            );


            setText(
                "message",
                error.message
            );


            alert(
                "CarbonTrace processing failed:\n\n" +
                error.message
            );

        }

        finally {

            if (button) {

                button.disabled =
                    false;

                button.textContent =
                    "Process Document";

            }

        }

    }



    // =========================================================
    // UPLOAD BUTTON
    // =========================================================

    function setupUploadButton() {

        const button =
            getElement(
                "btn-upload-ingest"
            );


        const input =
            getElement(
                "document-file-input"
            );


        if (!button) {

            console.error(
                "❌ Upload button not found"
            );

            return;

        }


        button.addEventListener(
            "click",
            function () {

                console.log(
                    "🟢 Process Document clicked"
                );


                const file =
                    input &&
                    input.files &&
                    input.files.length > 0
                        ? input.files[0]
                        : currentFile;


                if (!file) {

                    alert(
                        "Please choose a PDF or CSV file first."
                    );

                    return;

                }


                uploadDocument(
                    file
                );

            }
        );

    }



    // =========================================================
    // RENDER KPI
    // =========================================================

    function renderKPI(
        data
    ) {

        const scope1 =
            numberValue(
                data.scope_1_kg_co2e ??
                data.scope1_kg_co2e
            );


        const scope2 =
            numberValue(
                data.scope_2_kg_co2e ??
                data.scope2_kg_co2e
            );


        const scope3 =
            numberValue(
                data.scope_3_kg_co2e ??
                data.scope3_kg_co2e
            );


        const total =
            data.total_kg_co2e !== undefined
                ? numberValue(
                    data.total_kg_co2e
                )
                : (
                    scope1 +
                    scope2 +
                    scope3
                );


        setText(
            "kpi-total-co2e",
            formatNumber(total, 2)
        );


        setText(
            "kpi-scope1",
            formatNumber(scope1, 2)
        );


        setText(
            "kpi-scope2",
            formatNumber(scope2, 2)
        );


        setText(
            "kpi-scope3",
            formatNumber(scope3, 2)
        );


        const records =
            getRecords(data);


        setText(
            "kpi-records-count",
            String(records.length)
        );


        /*
         * Do NOT claim 100%.
         *
         * Only show backend supplied
         * validation/pass rate.
         */

        const passRate =
            data.pass_rate ??
            data.validation_pass_rate ??
            data.compliance?.pass_rate;


        if (
            passRate !== undefined
        ) {

            setText(
                "kpi-pass-rate",
                `${passRate}%`
            );

        } else {

            setText(
                "kpi-pass-rate",
                "—"
            );

        }


        // Distribution

        if (total > 0) {

            const p1 =
                (scope1 / total) * 100;


            const p2 =
                (scope2 / total) * 100;


            const p3 =
                (scope3 / total) * 100;


            setText(
                "dist-scope1-text",
                `${p1.toFixed(1)}%`
            );


            setText(
                "dist-scope2-text",
                `${p2.toFixed(1)}%`
            );


            setText(
                "dist-scope3-text",
                `${p3.toFixed(1)}%`
            );


            setWidth(
                "dist-scope1-bar",
                p1
            );


            setWidth(
                "dist-scope2-bar",
                p2
            );


            setWidth(
                "dist-scope3-bar",
                p3
            );

        }

    }



    // =========================================================
    // GET RECORDS
    // =========================================================

    function getRecords(
        data
    ) {

        if (
            Array.isArray(
                data.records
            )
        ) {

            return data.records;

        }


        if (
            Array.isArray(
                data.audit_records
            )
        ) {

            return data.audit_records;

        }


        if (
            Array.isArray(
                data.audit_trail
            )
        ) {

            return data.audit_trail;

        }


        return [];

    }



    // =========================================================
    // RENDER EMISSION TABLE
    // =========================================================

    function renderRecords(
        records
    ) {

        currentRecords =
            Array.isArray(records)
                ? records
                : [];


        const table =
            getElement(
                "emission-table-body"
            );


        if (!table) {

            return;

        }


        if (
            currentRecords.length === 0
        ) {

            table.innerHTML =
                `
                <tr>
                    <td colspan="7">
                        No emission records found.
                    </td>
                </tr>
                `;


            setText(
                "table-row-count",
                "0 records"
            );


            return;

        }


        table.innerHTML =
            currentRecords
                .map(
                    function (record) {

                        const activity =
                            escapeHTML(
                                record.activity ||
                                "--"
                            );


                        const quantity =
                            formatNumber(
                                record.quantity,
                                2
                            );


                        const unit =
                            escapeHTML(
                                record.unit ||
                                "--"
                            );


                        const scope =
                            record.scope !== undefined
                                ? `Scope ${record.scope}`
                                : "--";


                        const factor =
                            record.emission_factor !== undefined
                                ? formatNumber(
                                    record.emission_factor,
                                    4
                                )
                                : "--";


                        const factorUnit =
                            escapeHTML(
                                record.factor_unit ||
                                ""
                            );


                        const emissions =
                            record.emissions_kg_co2e !== undefined
                                ? formatKg(
                                    record.emissions_kg_co2e
                                )
                                : "--";


                        const status =
                            record.validation_status ||
                            record.assurance_status ||
                            record.factor_status ||
                            "REVIEW";


                        const context =
                            escapeHTML(
                                record.context ||
                                ""
                            );


                        return `
                        <tr>

                            <td>
                                <strong>
                                    ${activity}
                                </strong>

                                <br>

                                <small>
                                    ${context}
                                </small>
                            </td>


                            <td>
                                ${quantity}
                            </td>


                            <td>
                                ${unit}
                            </td>


                            <td>
                                ${scope}
                            </td>


                            <td>
                                ${factor}
                                ${factorUnit}
                            </td>


                            <td>
                                ${emissions}
                            </td>


                            <td>
                                <span class="${getStatusClass(status)}">
                                    ${escapeHTML(status)}
                                </span>
                            </td>

                        </tr>
                        `;

                    }
                )
                .join("");


        setText(
            "table-row-count",
            `${currentRecords.length} records`
        );

    }



    // =========================================================
    // CATEGORY BREAKDOWN
    // =========================================================

    function renderBreakdown(
        records
    ) {

        const container =
            getElement(
                "distribution-breakdown-list"
            );


        if (!container) {

            return;

        }


        if (
            !records ||
            records.length === 0
        ) {

            container.innerHTML =
                "<p>No category data available.</p>";

            return;

        }


        const totals = {};


        records.forEach(
            function (record) {

                const activity =
                    record.activity ||
                    "unknown";


                const value =
                    numberValue(
                        record.emissions_kg_co2e
                    );


                totals[activity] =
                    (
                        totals[activity] ||
                        0
                    ) + value;

            }
        );


        const entries =
            Object.entries(
                totals
            ).sort(
                function (a, b) {

                    return b[1] - a[1];

                }
            );


        const total =
            entries.reduce(
                function (sum, item) {

                    return sum + item[1];

                },
                0
            );


        container.innerHTML =
            entries
                .map(
                    function (
                        [activity, value]
                    ) {

                        const share =
                            total > 0
                                ? (
                                    value /
                                    total
                                ) * 100
                                : 0;


                        return `
                        <div>

                            <strong>
                                ${escapeHTML(activity)}
                            </strong>

                            <span>
                                ${formatKg(value)}
                                (${share.toFixed(1)}%)
                            </span>

                        </div>
                        `;

                    }
                )
                .join("");

    }



    // =========================================================
    // FACTOR EVIDENCE
    // =========================================================

    function renderFactorEvidence(
        records
    ) {

        if (
            !records ||
            records.length === 0
        ) {

            return;

        }


        const record =
            records[0];


        setText(
            "factor-source",
            record.factor_source ||
            record.source ||
            "Configured factor dataset"
        );


        setText(
            "factor-vintage",
            String(
                record.factor_year ||
                record.factor_version ||
                "N/A"
            )
        );


        setText(
            "factor-methodology",
            record.factor_methodology ||
            "Configured methodology"
        );


        setText(
            "factor-region",
            record.factor_region ||
            "N/A"
        );


        const factor =
            record.emission_factor;


        if (
            factor !== undefined
        ) {

            setText(
                "factor-value",
                `${formatNumber(factor, 4)} ${
                    record.factor_unit || ""
                }`
            );

        }


        setText(
            "factor-status",
            record.factor_status ||
            "CONFIGURED"
        );

    }



    // =========================================================
    // DATA QUALITY
    // =========================================================

    function renderDataQuality(
        data
    ) {

        const quality =
            data.data_quality ||
            data.data_quality_score;


        if (
            typeof quality === "number"
        ) {

            setText(
                "data-quality-score",
                `${formatNumber(quality, 1)}%`
            );


            setText(
                "metric-primary-share",
                `${formatNumber(quality, 1)}%`
            );


            setText(
                "metric-temporal-correlation",
                `${formatNumber(quality, 1)}%`
            );


            setText(
                "metric-geo-match",
                `${formatNumber(quality, 1)}%`
            );


            setWidth(
                "metric-primary-bar",
                quality
            );


            setWidth(
                "metric-temporal-bar",
                quality
            );


            setWidth(
                "metric-geo-bar",
                quality
            );


            return;

        }


        if (
            quality &&
            typeof quality === "object"
        ) {

            const score =
                numberValue(
                    quality.score ??
                    quality.data_quality_score
                );


            const primary =
                numberValue(
                    quality.primary_share ??
                    score
                );


            const temporal =
                numberValue(
                    quality.temporal_correlation ??
                    score
                );


            const geo =
                numberValue(
                    quality.geo_match ??
                    score
                );


            setText(
                "data-quality-score",
                `${formatNumber(score, 1)}%`
            );


            setText(
                "metric-primary-share",
                `${formatNumber(primary, 1)}%`
            );


            setText(
                "metric-temporal-correlation",
                `${formatNumber(temporal, 1)}%`
            );


            setText(
                "metric-geo-match",
                `${formatNumber(geo, 1)}%`
            );


            setWidth(
                "metric-primary-bar",
                primary
            );


            setWidth(
                "metric-temporal-bar",
                temporal
            );


            setWidth(
                "metric-geo-bar",
                geo
            );

        }

    }



    // =========================================================
    // DISCLOSURE READINESS
    // =========================================================

    function renderDisclosure(
        data
    ) {

        const readiness =
            data.disclosure_readiness;


        if (
            readiness &&
            typeof readiness === "object"
        ) {

            if (
                readiness.csrd !== undefined
            ) {

                setText(
                    "badge-csrd-points",
                    `CSRD: ${readiness.csrd}`
                );

            }


            if (
                readiness.sec !== undefined
            ) {

                setText(
                    "badge-sec-status",
                    `SEC: ${readiness.sec}`
                );

            }


            if (
                readiness.ghg !== undefined
            ) {

                setText(
                    "badge-ghg-status",
                    `GHG: ${readiness.ghg}`
                );

            }


            return;

        }


        if (
            data.disclosure_readiness_score !== undefined
        ) {

            const score =
                numberValue(
                    data.disclosure_readiness_score
                );


            setText(
                "badge-csrd-points",
                `Disclosure Readiness: ${formatNumber(score, 1)}%`
            );

        }

    }



    // =========================================================
    // COMPLIANCE
    // =========================================================

    function renderCompliance(
        data
    ) {

        const compliance =
            data.compliance || {};


        const risk =
            compliance.overall_risk ||
            data.overall_risk ||
            null;


        if (risk) {

            setText(
                "riskSummary",
                `Overall Risk: ${risk}`
            );

        } else {

            setText(
                "riskSummary",
                "No overall risk supplied by backend."
            );

        }


        const findings =
            Array.isArray(
                compliance.findings
            )
                ? compliance.findings
                : [];


        if (
            findings.length === 0
        ) {

            setText(
                "complianceFindings",
                "No compliance findings returned."
            );

        } else {

            setHTML(
                "complianceFindings",

                findings
                    .map(
                        function (finding) {

                            const type =
                                finding.type ||
                                "CHECK";


                            const status =
                                finding.status ||
                                "REVIEW";


                            const message =
                                finding.message ||
                                finding.description ||
                                "";


                            return `
                            <div class="${getStatusClass(status)}">

                                <strong>
                                    ${escapeHTML(type)}
                                </strong>

                                <span>
                                    ${escapeHTML(status)}
                                </span>

                                <p>
                                    ${escapeHTML(message)}
                                </p>

                            </div>
                            `;

                        }
                    )
                    .join("")
            );

        }


        /*
         * Individual compliance checks
         */

        const checks = [
            {
                type:
                    "CALCULATION_INTEGRITY",

                id:
                    "badge-calc-integrity",

                label:
                    "Calculation Integrity"
            },

            {
                type:
                    "SCOPE_CLASSIFICATION",

                id:
                    "badge-scope-classification",

                label:
                    "Scope Classification"
            },

            {
                type:
                    "EMISSION_FACTOR_TRACEABILITY",

                id:
                    "badge-factor-traceability",

                label:
                    "Factor Traceability"
            },

            {
                type:
                    "DATA_COMPLETENESS",

                id:
                    "badge-data-completeness",

                label:
                    "Data Completeness"
            },

            {
                type:
                    "GREENWASHING_CLAIM",

                id:
                    "badge-greenwash-detection",

                label:
                    "Greenwashing Detection"
            }
        ];


        checks.forEach(
            function (check) {

                const finding =
                    findings.find(
                        function (item) {

                            return String(
                                item.type || ""
                            ).toUpperCase() ===
                                check.type;

                        }
                    );


                if (finding) {

                    setText(
                        check.id,
                        `${check.label}: ${
                            finding.status || "REVIEW"
                        }`
                    );

                }

            }
        );

    }



    // =========================================================
    // AUDIT TRAIL
    // =========================================================

    function renderAudit(
        records
    ) {

        currentAuditRecords =
            Array.isArray(records)
                ? records
                : [];


        const container =
            getElement(
                "audit-trail-container"
            );


        if (!container) {

            return;

        }


        if (
            currentAuditRecords.length === 0
        ) {

            container.innerHTML =
                "<p>No audit records found.</p>";

            return;

        }


        container.innerHTML =
            currentAuditRecords
                .map(
                    function (record) {

                        const id =
                            record.record_id ||
                            record.id ||
                            "N/A";


                        const source =
                            record.source_document ||
                            "Unknown";


                        const timestamp =
                            record.timestamp ||
                            "N/A";


                        const quantity =
                            formatNumber(
                                record.quantity,
                                2
                            );


                        const factor =
                            formatNumber(
                                record.emission_factor,
                                4
                            );


                        const emissions =
                            formatNumber(
                                record.emissions_kg_co2e,
                                2
                            );


                        const status =
                            record.validation_status ||
                            record.status ||
                            "REVIEW";


                        const equation =
                            record.calculation ||
                            `${quantity} × ${factor} = ${emissions} kg CO₂e`;


                        return `
                        <div class="audit-record">

                            <strong>
                                ${escapeHTML(id)}
                            </strong>

                            <p>
                                Source:
                                ${escapeHTML(source)}
                            </p>

                            <p>
                                ${escapeHTML(equation)}
                            </p>

                            <p>
                                ${escapeHTML(timestamp)}
                            </p>

                            <span class="${getStatusClass(status)}">
                                ${escapeHTML(status)}
                            </span>

                        </div>
                        `;

                    }
                )
                .join("");

    }



    // =========================================================
    // COMPLETE RESULT
    // =========================================================

    function renderResult(
        data
    ) {

        console.log(
            "🎯 Rendering backend result:",
            data
        );


        const dashboard =
            getElement(
                "dashboard"
            );


        if (dashboard) {

            dashboard.classList.remove(
                "hidden"
            );


            dashboard.style.display =
                "block";

        }


        const records =
            getRecords(data);


        renderKPI(
            data
        );


        renderRecords(
            records
        );


        renderBreakdown(
            records
        );


        renderDataQuality(
            data
        );


        renderDisclosure(
            data
        );


        renderFactorEvidence(
            records
        );


        renderCompliance(
            data
        );


        const auditRecords =
            Array.isArray(
                data.audit_trail
            )
                ? data.audit_trail
                : (
                    Array.isArray(
                        data.audit_records
                    )
                        ? data.audit_records
                        : records
                );


        renderAudit(
            auditRecords
        );


        if (
            data.filename
        ) {

            setText(
                "upload-status",
                `Processed: ${data.filename}`
            );

        }

    }



    // =========================================================
    // REFRESH EMISSIONS
    // =========================================================

    async function fetchEmissions() {

        if (!currentFile) {

            alert(
                "Please upload a document first."
            );

            return;

        }


        await uploadDocument(
            currentFile
        );

    }



    // =========================================================
    // REFRESH BUTTON
    // =========================================================

    function setupRefreshButton() {

        const button =
            getElement(
                "btn-fetch-emissions"
            );


        if (!button) {

            return;

        }


        button.addEventListener(
            "click",
            function () {

                fetchEmissions();

            }
        );

    }



    // =========================================================
    // AUDIT REFRESH
    // =========================================================

    async function triggerAudit() {

        if (!currentFile) {

            alert(
                "Please process a document first."
            );

            return;

        }


        try {

            const formData =
                new FormData();


            formData.append(
                "file",
                currentFile
            );


            const response =
                await fetch(
                    `${API_BASE_URL}/audit`,
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Audit request failed."
                );

            }


            const records =
                data.audit_trail ||
                data.audit_records ||
                [];


            renderAudit(
                records
            );


        }

        catch (error) {

            console.error(
                "Audit error:",
                error
            );


            alert(
                "Audit refresh failed:\n\n" +
                error.message
            );

        }

    }



    // =========================================================
    // AUDIT BUTTON
    // =========================================================

    function setupAuditButton() {

        const button =
            getElement(
                "btn-trigger-audit"
            );


        if (!button) {

            return;

        }


        button.addEventListener(
            "click",
            triggerAudit
        );

    }



    // =========================================================
    // TABLE SEARCH
    // =========================================================

    function setupTableSearch() {

        const input =
            getElement(
                "table-search-input"
            );


        if (!input) {

            return;

        }


        input.addEventListener(
            "input",
            function () {

                const query =
                    input.value
                        .trim()
                        .toLowerCase();


                const filtered =
                    currentRecords.filter(
                        function (record) {

                            return JSON.stringify(
                                record
                            )
                                .toLowerCase()
                                .includes(
                                    query
                                );

                        }
                    );


                renderRecords(
                    filtered
                );

            }
        );

    }



    // =========================================================
    // EXPORT CSV
    // =========================================================

    function exportCSV() {

        if (
            currentAuditRecords.length === 0
        ) {

            alert(
                "No audit records available to export."
            );

            return;

        }


        const headers = [
            "record_id",
            "source_document",
            "activity",
            "quantity",
            "unit",
            "context",
            "scope",
            "emission_factor",
            "factor_unit",
            "emissions_kg_co2e",
            "validation_status"
        ];


        const rows =
            currentAuditRecords.map(
                function (record) {

                    return headers.map(
                        function (header) {

                            const value =
                                record[header] ??
                                "";


                            return `"${String(value)
                                .replace(
                                    /"/g,
                                    '""'
                                )}"`;

                        }
                    ).join(",");

                }
            );


        const csv =
            [
                headers.join(","),
                ...rows
            ].join("\n");


        const blob =
            new Blob(
                [csv],
                {
                    type:
                        "text/csv;charset=utf-8;"
                }
            );


        const url =
            URL.createObjectURL(
                blob
            );


        const link =
            document.createElement(
                "a"
            );


        link.href =
            url;


        link.download =
            "carbontrace-audit.csv";


        document.body.appendChild(
            link
        );


        link.click();


        document.body.removeChild(
            link
        );


        URL.revokeObjectURL(
            url
        );

    }



    // =========================================================
    // EXPORT BUTTONS
    // =========================================================

    function setupExportButtons() {

        const auditButton =
            getElement(
                "btn-export-audit"
            );


        const csvButton =
            getElement(
                "btn-export-csv"
            );


        const packButton =
            getElement(
                "btn-export-pack"
            );


        if (auditButton) {

            auditButton.addEventListener(
                "click",
                exportCSV
            );

        }


        if (csvButton) {

            csvButton.addEventListener(
                "click",
                exportCSV
            );

        }


        if (packButton) {

            packButton.addEventListener(
                "click",
                function () {

                    if (!currentResult) {

                        alert(
                            "Process a document first."
                        );

                        return;

                    }


                    alert(
                        "The current MVP provides the verified audit ledger and compliance results. Full ZIP assurance-pack generation is not yet implemented."
                    );

                }
            );

        }

    }



    // =========================================================
    // SAMPLE BUTTON
    // =========================================================

    function setupSampleButton() {

        const button =
            getElement(
                "btn-load-sample"
            );


        if (!button) {

            return;

        }


        button.addEventListener(
            "click",
            function () {

                alert(
                    "Please choose your actual sample_emission_report.pdf using the file picker."
                );

            }
        );

    }



    // =========================================================
    // INITIALIZE
    // =========================================================

    function initialize() {

        console.log(
            "================================"
        );


        console.log(
            "CarbonTrace AI starting..."
        );


        console.log(
            "API:",
            API_BASE_URL
        );


        console.log(
            "================================"
        );


        resetDashboard();


        setupFileInput();

        setupUploadButton();

        setupRefreshButton();

        setupAuditButton();

        setupTableSearch();

        setupExportButtons();

        setupSampleButton();


        checkHealth();

        checkLyzrStatus();


        console.log(
            "✅ CarbonTrace AI ready"
        );

    }



    // =========================================================
    // DOM READY
    // =========================================================

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initialize
        );

    } else {

        initialize();

    }


})();