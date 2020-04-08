export const getDemoDocument = () => {
    return fetch("http://localhost:5001/api/v1/get/doc", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({doc_id: -1})
        }
    ).then(
        response => response.json()
    ).then(response => response);
};
