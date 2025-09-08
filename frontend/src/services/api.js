export async function Login(username, password) {
    const response = await fetch("http://localhost:8000/api/users/login/", {
        method: "POST",
        headers: {"Content-type": "application/json"},
        body: JSON.stringify({username, password}),
    });
    return response.json();
}