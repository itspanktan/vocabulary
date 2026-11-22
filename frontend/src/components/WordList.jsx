export default function WordList({ words, onDelete }) {
  if (words.length === 0) {
    return <p>No words yet. Add one below.</p>
  }

  return (
    <ul>
      {words.map((word) => (
        <li key={word.id}>
          <strong>{word.text}</strong> ({word.part_of_speech})
          <ul>
            {word.definitions.map((definition, index) => (
              <li key={index}>{definition.text}</li>
            ))}
          </ul>
          <button type="button" onClick={() => onDelete(word.id)}>
            Delete
          </button>
        </li>
      ))}
    </ul>
  )
}
