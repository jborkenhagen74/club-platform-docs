const apiBase = "https://localhost:8443/api/v1";

document.querySelector("#load").addEventListener("click", async () => {
  const response = await fetch(`${apiBase}/me`, {
    credentials: "include",
    headers: { "Accept": "application/json" }
  });
  const output = document.querySelector("#output");
  output.textContent = response.ok
    ? JSON.stringify(await response.json(), null, 2)
    : `HTTP ${response.status}`;
});
