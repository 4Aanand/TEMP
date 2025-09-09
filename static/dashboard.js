const chart1 = new Chart(document.getElementById('chart1').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Temperature (°F)', data: [], borderColor: 'red', fill: false },
            { label: 'Vibration (g)', data: [], borderColor: 'blue', fill: false }
        ]
    },
    options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
    }
});

const chart2 = new Chart(document.getElementById('chart2').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Temperature (°F)', data: [], borderColor: 'green', fill: false },
            { label: 'Vibration (g)', data: [], borderColor: 'orange', fill: false }
        ]
    },
    options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
    }
});

// async function fetchData() {
//     try {
//         const res1 = await fetch('/data?machine_id=MCH-001');
//         const data1 = await res1.json();
//         chart1.data.labels.push(new Date().toLocaleTimeString());
//         chart1.data.datasets[0].data.push(data1.temperature);
//         chart1.data.datasets[1].data.push(data1.vibration);
//         chart1.update();
//         document.getElementById('status1').innerText = `Status: ${data1.status}`;

//         const res2 = await fetch('/data?machine_id=MCH-002');
//         const data2 = await res2.json();
//         chart2.data.labels.push(new Date().toLocaleTimeString());
//         chart2.data.datasets[0].data.push(data2.temperature);
//         chart2.data.datasets[1].data.push(data2.vibration);
//         chart2.update();
//         document.getElementById('status2').innerText = `Status: ${data2.status}`;
//     } catch (error) {
//         console.error("Failed to fetch data:", error);
//     }
// }

// setInterval(fetchData, 3000);
async function fetchData() {
    try {
        const res1 = await fetch('/data?machine_id=MCH-001');
        const data1 = await res1.json();

        chart1.data.labels.push(new Date().toLocaleTimeString());
        chart1.data.datasets[0].data.push(data1.temperature);
        chart1.data.datasets[1].data.push(data1.vibration);
        chart1.update();

        const status1 = document.getElementById('status1');
        status1.innerText = `Status: ${data1.status} | Risk: ${data1.risk_level} | Failure Probability: ${data1.failure_probability}%`;
        applyRiskColor(status1, data1.risk_level);

        const res2 = await fetch('/data?machine_id=MCH-002');
        const data2 = await res2.json();

        chart2.data.labels.push(new Date().toLocaleTimeString());
        chart2.data.datasets[0].data.push(data2.temperature);
        chart2.data.datasets[1].data.push(data2.vibration);
        chart2.update();

        const status2 = document.getElementById('status2');
        status2.innerText = `Status: ${data2.status} | Risk: ${data2.risk_level} | Failure Probability: ${data2.failure_probability}%`;
        applyRiskColor(status2, data2.risk_level);

    } catch (error) {
        console.error("Failed to fetch data:", error);
    }
}

function applyRiskColor(element, riskLevel) {
    element.classList.remove('low', 'moderate', 'high', 'critical');

    if (riskLevel.includes('Low')) element.classList.add('low');
    else if (riskLevel.includes('Moderate')) element.classList.add('moderate');
    else if (riskLevel.includes('High')) element.classList.add('high');
    else if (riskLevel.includes('Critical')) element.classList.add('critical');
}

setInterval(fetchData, 3000);