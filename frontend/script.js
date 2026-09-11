const form = document.getElementById("financialForm");
const result = document.getElementById("result");


form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const income = Number(document.getElementById("income").value);
    const expenses = Number(document.getElementById("expenses").value);
    const savings = Number(document.getElementById("savings").value);
    const debt = Number(document.getElementById("debt").value);


    const data = {
        income: income,
        expenses: expenses,
        savings: savings,
        debt: debt
    };


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        const prediction = await response.json();


        let recommendationsHTML = "";

        prediction.recommendations.forEach(function(item) {

            recommendationsHTML += `
                <li>${item}</li>
            `;

        });


        result.innerHTML = `
            <h2>Financial Risk: ${prediction.risk}</h2>

            <p>Risk Score: ${prediction.risk_score}</p>

            <h3>Recommendations</h3>

            <ul>
                ${recommendationsHTML}
            </ul>
        `;


    } catch (error) {

        result.innerHTML = `
            <p>Unable to connect to backend.</p>
        `;

        console.error(error);
    }

});