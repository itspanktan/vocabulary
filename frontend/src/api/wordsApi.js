const BASE_URL = '/api/words'

async function parseOrThrow(response) {
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed with status ${response.status}`)
  }
  return response.status === 204 ? null : response.json()
}

export async function listWords() {
  return parseOrThrow(await fetch(BASE_URL))
}

export async function createWord(word) {
  return parseOrThrow(
    await fetch(BASE_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(word),
    }),
  )
}

export async function deleteWord(wordId) {
  return parseOrThrow(await fetch(`${BASE_URL}/${wordId}`, { method: 'DELETE' }))
}
