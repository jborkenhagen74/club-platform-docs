// Serve this example behind the same-origin /api/v1 proxy as the real portal.
let token = "";
const output = document.querySelector("#output");
async function api(path, body) {
  const response = await fetch("/api/v1" + path, {
    method: body === undefined ? "GET" : "POST",
    headers: {Accept: "application/json", ...(token ? {Authorization: "Bearer " + token} : {}),
      ...(body === undefined ? {} : {"Content-Type": "application/json"})},
    body: body === undefined ? undefined : JSON.stringify(body),
    cache: "no-store", redirect: "error", signal: AbortSignal.timeout(15000)
  });
  if (response.status === 401) token = "";
  if (!response.ok) throw Error("HTTP " + response.status);
  return response.status === 204 ? null : response.json();
}
async function run(fn) {
  try { output.textContent = JSON.stringify(await fn(), null, 2); }
  catch (error) { output.textContent = error.message; }
}
document.querySelector("#login").addEventListener("submit", event => {
  event.preventDefault();
  const fields = new FormData(event.currentTarget);
  const login = fields.get("login"), password = fields.get("password");
  event.currentTarget.elements.password.value = "";
  run(async () => {
    token = "";
    const session = await api("/auth/login", {login, password});
    token = session.token;
    return {user_id: session.user_id, login: session.login, expires_at: session.expires_at};
  });
});
document.querySelector("#load").addEventListener("click", () => run(() => api("/auth/me")));
document.querySelector("#logout").addEventListener("click", () => run(async () => {
  try { await api("/auth/logout", {}); } finally { token = ""; }
  return "Signed out";
}));
