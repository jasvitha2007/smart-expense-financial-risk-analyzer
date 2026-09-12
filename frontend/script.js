function analyzeFile() {

    console.log("=== ANALYZE STARTED ===");

    const fileInput = document.getElementById("csvFile");
    const button = document.getElementById("analyzeBtn");
    const status = document.getElementById("status");
    const dashboard = document.getElementById("dashboard");

    console.log("File input:", fileInput);
    console.log("Dashboard:", dashboard);

    // Check file
    if (!fileInput.files || fileInput.files.length === 0) {

        status.textContent =
            "❌ Please select a CSV file first.";

        console.log("NO FILE SELECTED");

        return;
    }

    const file = fileInput.files[0];

    console.log("FILE:", file.name);
    console.log("SIZE:", file.size);

    // Disable button
    button.disabled = true;

    status.textContent =
        "⏳ Analyzing your financial data...";

    // Create form data
    const formData = new FormData();

    formData.append("file", file);

    console.log("FormData created");

    // ------------------------------------
    // CREATE REQUEST
    // ------------------------------------

    const xhr = new XMLHttpRequest();

    xhr.open(
        "POST",
        "http://127.0.0.1:8000/predict",
        true
    );

    xhr.onreadystatechange = function () {

        console.log(
            "READY STATE:",
            xhr.readyState,
            "STATUS:",
            xhr.status
        );

        // Request completed
        if (xhr.readyState === 4) {

            button.disabled = false;

            // -----------------------------
            // SUCCESS
            // -----------------------------

            if (xhr.status === 200) {

                console.log(
                    "SERVER RESPONSE RECEIVED"
                );

                console.log(
                    xhr.responseText
                );

                try {

                    const data =
                        JSON.parse(
                            xhr.responseText
                        );

                    console.log(
                        "JSON PARSED:",
                        data
                    );

                    showDashboard(data);

                    status.textContent =
                        "✅ Analysis completed successfully!";

                }
                catch (error) {

                    console.error(
                        "JSON ERROR:",
                        error
                    );

                    status.textContent =
                        "❌ Server returned invalid data.";

                }

            }

            // -----------------------------
            // ERROR
            // -----------------------------

            else {

                console.error(
                    "SERVER ERROR:",
                    xhr.status,
                    xhr.responseText
                );

                status.textContent =
                    "❌ Backend error: " +
                    xhr.status;

            }

        }

    };


    xhr.onerror = function () {

        console.error(
            "NETWORK ERROR"
        );

        button.disabled = false;

        status.textContent =
            "❌ Cannot connect to FastAPI.";

    };


    console.log(
        "SENDING REQUEST..."
    );

    xhr.send(formData);

}


// ========================================
// DISPLAY DASHBOARD
// ========================================

function showDashboard(data) {

    console.log(
        "=== DISPLAY DASHBOARD ==="
    );

    const dashboard =
        document.getElementById(
            "dashboard"
        );

    // SHOW DASHBOARD FIRST
    dashboard.classList.remove(
        "hidden"
    );

    console.log(
        "Dashboard class:",
        dashboard.className
    );


    // ====================================
    // FINANCIAL SUMMARY
    // ====================================

    const summary =
        data.financial_summary;

    document.getElementById(
        "totalIncome"
    ).textContent =
        formatCurrency(
            summary.total_income
        );

    document.getElementById(
        "totalExpense"
    ).textContent =
        formatCurrency(
            summary.total_expense
        );

    document.getElementById(
        "totalSavings"
    ).textContent =
        formatCurrency(
            summary.total_savings
        );


    // ====================================
    // FINANCIAL HEALTH
    // ====================================

    const health =
        data.financial_health;

    document.getElementById(
        "healthScore"
    ).textContent =
        health.financial_health_score +
        " / 100";

    document.getElementById(
        "healthStatus"
    ).textContent =
        health.health_status;

    document.getElementById(
        "riskLevel"
    ).textContent =
        health.risk_level;

    document.getElementById(
        "expenseRatio"
    ).textContent =
        Number(
            health.expense_ratio
        ).toFixed(2) + "%";

    document.getElementById(
        "savingsRate"
    ).textContent =
        Number(
            health.savings_rate
        ).toFixed(2) + "%";

    document.getElementById(
        "anomalyRate"
    ).textContent =
        Number(
            health.anomaly_rate
        ).toFixed(2) + "%";


    // ====================================
    // CATEGORY EXPENSES
    // ====================================

    showCategories(
        data.category_expenses
    );
    showMonthlyChart(
    data.monthly_expenses
);


    // ====================================
    // PREDICTION
    // ====================================

    document.getElementById(
        "nextMonthExpense"
    ).textContent =
        formatNumber(
            data.prediction.next_month_expense
        );

    document.getElementById(
        "bestModel"
    ).textContent =
        data.prediction.best_model;


    // ====================================
    // ANOMALIES
    // ====================================

    showAnomalies(
        data.anomalies
    );


    // ====================================
    // RECOMMENDATIONS
    // ====================================

    const list =
        document.getElementById(
            "recommendations"
        );

    list.innerHTML = "";

    health.recommendations.forEach(
        function (recommendation) {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                recommendation;

            list.appendChild(li);

        }
    );


    // ====================================
    // MODEL COMPARISON
    // ====================================

    showModels(
        data.prediction.model_comparison
    );


    console.log(
        "=== DASHBOARD FINISHED ==="
    );
}


// ========================================
// CURRENCY
// ========================================

function formatCurrency(value) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 2
        }
    ).format(value);

}


function formatNumber(value) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            maximumFractionDigits: 2
        }
    ).format(value);

}


// ========================================
// CATEGORY
// ========================================

function showCategories(categories) {

    const chart =
        document.getElementById(
            "categoryChart"
        );

    chart.innerHTML = "";

    const entries =
        Object.entries(categories);

    if (entries.length === 0) {

        chart.textContent =
            "No category data available.";

        return;
    }

    const max =
        Math.max(
            ...entries.map(
                item => Number(item[1])
            )
        );

    entries.forEach(
        function ([category, amount]) {

            const percentage =
                (
                    Number(amount) / max
                ) * 100;

            const row =
                document.createElement(
                    "div"
                );

            row.className =
                "category-row";

            row.innerHTML = `
                <div class="category-header">
                    <span>${category}</span>
                    <strong>
                        ${formatCurrency(amount)}
                    </strong>
                </div>

                <div class="bar">
                    <div
                        class="bar-fill"
                        style="width:${percentage}%"
                    ></div>
                </div>
            `;

            chart.appendChild(row);

        }
    );
}
// ========================================
// MONTHLY SPENDING TREND
// ========================================

function showMonthlyChart(monthlyExpenses) {

    const chart =
        document.getElementById(
            "monthlyChart"
        );

    chart.innerHTML = "";

    if (
        !monthlyExpenses ||
        monthlyExpenses.length === 0
    ) {

        chart.textContent =
            "No monthly spending data available.";

        return;
    }

    const maxAmount =
        Math.max(
            ...monthlyExpenses.map(
                item => Number(item.amount)
            )
        );

    monthlyExpenses.forEach(
        function (item) {

            const percentage =
                maxAmount > 0
                    ? (Number(item.amount) / maxAmount) * 100
                    : 0;

            const row =
                document.createElement(
                    "div"
                );

            row.className =
                "monthly-row";

            row.innerHTML = `
                <div class="monthly-header">

                    <span>
                        ${item.month}
                    </span>

                    <strong>
                        ${formatCurrency(item.amount)}
                    </strong>

                </div>

                <div class="monthly-bar">

                    <div
                        class="monthly-bar-fill"
                        style="width:${percentage}%"
                    ></div>

                </div>
            `;

            chart.appendChild(row);

        }
    );
}


// ========================================
// ANOMALIES
// ========================================

function showAnomalies(anomalies) {

    const table =
        document.getElementById(
            "anomalyTable"
        );

    table.innerHTML = "";

    if (!anomalies.length) {

        table.innerHTML = `
            <tr>
                <td colspan="4">
                    No unusual transactions detected.
                </td>
            </tr>
        `;

        return;
    }

    anomalies.forEach(
        function (item) {

            const row =
                document.createElement(
                    "tr"
                );

            row.innerHTML = `
                <td>${item.Date}</td>

                <td>
                    ${item["Transaction Description"]}
                </td>

                <td>
                    ${item.Category}
                </td>

                <td>
                    ${formatCurrency(
                        item.Amount
                    )}
                </td>
            `;

            table.appendChild(row);

        }
    );
}


// ========================================
// MODEL TABLE
// ========================================

function showModels(models) {

    const table =
        document.getElementById(
            "modelTable"
        );

    table.innerHTML = "";

    models.forEach(
        function (model) {

            const row =
                document.createElement(
                    "tr"
                );

            row.innerHTML = `
                <td>${model.Model}</td>

                <td>
                    ${Number(
                        model.MAE
                    ).toFixed(2)}
                </td>

                <td>
                    ${Number(
                        model.RMSE
                    ).toFixed(2)}
                </td>

                <td>
                    ${
                        model.R2 === null
                        ? "N/A"
                        : Number(
                            model.R2
                        ).toFixed(2)
                    }
                </td>
            `;

            table.appendChild(row);

        }
    );
}