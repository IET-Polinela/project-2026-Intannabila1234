// api.js
// Utility to call backend APIs using Fetch and attaching bearer token.

// Generic request helper
export async function requestAPI(endpoint, method = 'GET', bodyData = null) {
  const headers = {
    'Accept': 'application/json',
  };

  // If we have JSON body, set header
  if (bodyData) headers['Content-Type'] = 'application/json';

  // Attach Authorization header if access token exists
  const token = localStorage.getItem('access_token');
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const options = {
    method,
    headers,
  };

  if (bodyData) options.body = JSON.stringify(bodyData);

  try {
    const res = await fetch(endpoint, options);
    const text = await res.text();
    // Try parse JSON when possible
    const data = text ? JSON.parse(text) : {};

    if (!res.ok) {
      // Throw a useful error
      const err = new Error(data.detail || data.message || 'API request failed');
      err.status = res.status;
      err.data = data;
      throw err;
    }

    return data;
  } catch (err) {
    // Network or parsing error
    throw err;
  }
}
