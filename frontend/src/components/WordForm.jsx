import { useState } from 'react'

const PARTS_OF_SPEECH = [
  'noun',
  'verb',
  'adjective',
  'adverb',
  'pronoun',
  'preposition',
  'conjunction',
  'interjection',
]

export default function WordForm({ onSubmit }) {
  const [text, setText] = useState('')
  const [partOfSpeech, setPartOfSpeech] = useState(PARTS_OF_SPEECH[0])
  const [definition, setDefinition] = useState('')

  function handleSubmit(event) {
    event.preventDefault()
    onSubmit({
      text,
      part_of_speech: partOfSpeech,
      definitions: definition ? [{ text: definition }] : [],
    })
    setText('')
    setDefinition('')
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Word"
        required
      />
      <select value={partOfSpeech} onChange={(event) => setPartOfSpeech(event.target.value)}>
        {PARTS_OF_SPEECH.map((part) => (
          <option key={part} value={part}>
            {part}
          </option>
        ))}
      </select>
      <input
        value={definition}
        onChange={(event) => setDefinition(event.target.value)}
        placeholder="Definition"
      />
      <button type="submit">Add word</button>
    </form>
  )
}
