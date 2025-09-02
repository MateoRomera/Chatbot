const BACKEND_URL = "http://127.0.0.1:8000/api";

// Función única para llamadas API
async function apiCall(endpoint, params = {}) {
    try {
        const queryString = new URLSearchParams(params).toString();
        const resp = await fetch(`${BACKEND_URL}/${endpoint}?${queryString}`);
        if (!resp.ok) throw new Error("Backend devolvió un estado no OK");
        const data = await resp.json();

        if (data.success) {
            return data.data;
        } else {
            throw new Error(data.error || "Error desconocido en backend");
        }
    } catch (err) {
        console.error(`❌ Error en apiCall(${endpoint}):`, err);
        throw err;
    }
}

// Chat IA
async function sendChatQuery(userInput) {
    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += `<p><strong>Usuario:</strong> ${userInput}</p>`;

    try {
        const data = await apiCall("ask", { query: userInput });
        chatBox.innerHTML += `<p><strong>IA:</strong> ${data.response}</p>`;
    } catch (err) {
        chatBox.innerHTML += `<p><strong>Error:</strong> ${err.message}</p>`;
    }
}

// Query estructurada
async function sendStructuredQuery(params) {
    const resultsBox = document.getElementById("resultsBox");
    resultsBox.innerHTML = `<p><em>Buscando...</em></p>`;

    try {
        const data = await apiCall("structured_query", params);
        resultsBox.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    } catch (err) {
        resultsBox.innerHTML = `<p><strong>Error:</strong> ${err.message}</p>`;
    }
}
