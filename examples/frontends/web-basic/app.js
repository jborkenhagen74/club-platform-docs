'use strict';
// Same-origin HTTPS proxy serves this directory and forwards /api to the host.
// Never keep credentials or tokens in localStorage, sessionStorage or URLs.
let token = '';
let cursor = null;
const get = id => document.getElementById(id);
function signedOut() {
  token = '';
  cursor = null;
  get('people').replaceChildren();
  get('more').hidden = true;
  get('session').hidden = true;
  get('login-form').hidden = false;
}
async function request(path, body) {
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  const response = await fetch(path, {
    method: body === undefined ? 'GET' : 'POST', headers,
    body: body === undefined ? undefined : JSON.stringify(body),
    cache: 'no-store', credentials: 'omit', redirect: 'error'
  });
  if (response.status === 401) signedOut();
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(`${response.status}: ${error.error || 'request_failed'}`);
  }
  return response.status === 204 ? null : response.json();
}
async function listPeople(append = false) {
  const path = '/api/v1/persons' + (append && cursor ? `?after=${encodeURIComponent(cursor)}` : '');
  const page = await request(path);
  if (!append) get('people').replaceChildren();
  for (const person of page.items) {
    const item = document.createElement('li');
    item.textContent = `${person.given_name} ${person.family_name}`;
    get('people').append(item);
  }
  cursor = page.next_cursor;
  get('more').hidden = cursor === null;
  get('status').textContent = `${page.items.length} records received.`;
}
async function perform(button, action) {
  button.disabled = true;
  try { await action(); }
  catch (error) { get('status').textContent = error.message; }
  finally { button.disabled = false; }
}
get('login-form').addEventListener('submit', event => {
  event.preventDefault();
  void perform(event.submitter || get('login-form').querySelector('button'), async () => {
    try {
      const session = await request('/api/v1/auth/login', {login: get('login').value, password: get('password').value});
      token = session.token;
      get('login-form').hidden = true;
      get('session').hidden = false;
      await listPeople();
    } finally { get('password').value = ''; }
  });
});
get('refresh').addEventListener('click', event => void perform(event.target, () => listPeople()));
get('more').addEventListener('click', event => void perform(event.target, () => listPeople(true)));
get('logout').addEventListener('click', event => void perform(event.target, async () => {
  try {
    await request('/api/v1/auth/logout', {});
    get('status').textContent = 'Signed out.';
  } finally { signedOut(); }
}));
