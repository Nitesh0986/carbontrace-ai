const pdfFile = document.getElementById("pdfFile");
const fileName = document.getElementById("fileName");
const processBtn = document.getElementById("processBtn");
const message = document.getElementById("message");

const dashboard = document.getElementById("dashboard");

const totalEmission = document.getElementById("totalEmission");
const scope1 = document.getElementById("scope1");
const scope2 = document.getElementById("scope2");
const scope3 = document.getElementById("scope3");

const recordsContainer = document.getElementById("records");
const auditContainer = document.getElementById("audit");


/* ---------------------------------------
   File selection
--------------------------------------- */

pdfFile.addEventListener("change", () => {

    if (pdfFile.files.length > 0) {

        fileName.textContent =
            pdfFile.files[0].name;

    } else {

        fileName.textContent =
            "No file selected";
    }

});


/* ---------------------------------------
   Process PDF
--------------------------------------- */

processBtn.addEventListener("click", async () => {

    if (pdfFile.files.length === 0) {

        message.textContent =
            "Please select a PDF first.";

        return;
    }


    const file = pdfFile.files[0];

    const formData = new FormData();

    formData.append("file", file);


    processBtn.disabled = true;

    message.textContent =
        "Processing document...";


    try {

        const response = await fetch(
            "/emissions",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Processing failed"
            );
        }


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

});


/* ---------------------------------------
   Display Dashboard
--------------------------------------- */

function displayDashboard(data) {

    dashboard.classList.remove("hidden");


    totalEmission.textContent =
        formatNumber(data.total_kg_co2e);

    scope1.textContent =
        formatNumber(data.scope_1_kg_co2e);

    scope2.textContent =
        formatNumber(data.scope_2_kg_co2e);

    scope3.textContent =
        formatNumber(data.scope_3_kg_co2e);


    displayRecords(data.records);

    displayAudit(data.records);


    dashboard.scrollIntoView({
        behavior: "smooth"
    });

}


/* ---------------------------------------
   Emission records
--------------------------------------- */

function displayRecords(records) {

    recordsContainer.innerHTML = "";


    records.forEach(record => {

        const div =
            document.createElement("div");

        div.className = "record";


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
                ${formatNumber(record.emissions_kg_co2e)}
                kg CO₂e
            </div>
        `;


        recordsContainer.appendChild(div);

    });

}


/* ---------------------------------------
   Audit trail
--------------------------------------- */

function displayAudit(records) {

    auditContainer.innerHTML = "";


    records.forEach((record, index) => {

        const div =
            document.createElement("div");

        div.className =
            "audit-record";


        div.innerHTML = `
            <strong>
                Audit Record #${index + 1}
            </strong>

            <p>
                Activity:
                ${record.activity}
            </p>

            <p>
                Quantity:
                ${record.quantity}
                ${record.unit}
            </p>

            <p>
                Scope:
                Scope ${record.scope}
            </p>

            <p>
                Emission Factor:
                ${record.emission_factor}
                ${record.factor_unit}
            </p>

            <p>
                Calculation:
                ${record.calculation}
            </p>

            <p>
                Result:
                ${formatNumber(record.emissions_kg_co2e)}
                kg CO₂e
            </p>
        `;


        auditContainer.appendChild(div);

    });

}


/* ---------------------------------------
   Number formatting
--------------------------------------- */

function formatNumber(number) {

    return Number(number).toLocaleString(
        undefined,
        {
            maximumFractionDigits: 2
        }
    );

}