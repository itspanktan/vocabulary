import { useEffect, useState } from 'react'
import { createWord, deleteWord, listWords } from './api/wordsApi'
import WordForm from './components/WordForm'
import WordList from './components/WordList'

export default function App() {
  const [words, setWords] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    listWords().then(setWords).catch((err) => setError(err.message))
  }, [])

  async function handleCreate(word) {
    try {
      const created = await createWord(word)
      setWords((current) => [...current, created])
      setError(null)
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDelete(wordId) {
    try {
      await deleteWord(wordId)
      setWords((current) => current.filter((word) => word.id !== wordId))
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <main>
      <h1>Vocabulary</h1>
      {error && <p role="alert">{error}</p>}
      <WordForm onSubmit={handleCreate} />
      <WordList words={words} onDelete={handleDelete} />
    </main>
  )
}
