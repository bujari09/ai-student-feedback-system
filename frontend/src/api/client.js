const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`
    try {
      const body = await response.json()
      if (Array.isArray(body.detail)) {
        message = body.detail.map((d) => `${d.loc.at(-1)}: ${d.msg}`).join(' · ')
      } else if (body.detail) {
        message = body.detail
      }
    } catch {
      // keep the HTTP status message
    }
    throw new Error(message)
  }
  return response.json()
}

export const api = {
  health: () => request('/api/health'),
  analytics: () => request('/api/analytics'),
  listFeedback: (limit = 100) => request(`/api/feedback?limit=${limit}`),
  createFeedback: (payload) =>
    request('/api/feedback', { method: 'POST', body: JSON.stringify(payload) }),
}
