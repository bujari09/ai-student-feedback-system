import { useState } from 'react'
import { api } from '../api/client.js'
import { formatScore, titleCase } from '../format.js'
import SentimentBadge from './SentimentBadge.jsx'

const ID_PATTERN = /^[A-Za-z0-9_-]{3,40}$/

export default function FeedbackForm({ onSubmitted }) {
  const [studentId, setStudentId] = useState('')
  const [text, setText] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const trimmed = text.trim()
  const valid = ID_PATTERN.test(studentId) && trimmed.length >= 10 && trimmed.length <= 2000

  async function handleSubmit(event) {
    event.preventDefault()
    if (!valid) return
    setSubmitting(true)
    setError(null)
    try {
      const created = await api.createFeedback({ anonymous_student_id: studentId, feedback_text: trimmed })
      setResult(created)
      setText('')
      onSubmitted?.()
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="card">
      <h2 className="card-title">Submit Feedback</h2>
      <p className="card-subtitle">Anonymous – use an ID such as student_001, never a real name</p>

      <form className="form" onSubmit={handleSubmit}>
        <div className="field">
          <label htmlFor="student-id">Anonymous student ID</label>
          <input
            id="student-id"
            className="input"
            value={studentId}
            onChange={(e) => setStudentId(e.target.value)}
            placeholder="student_001"
            autoComplete="off"
          />
          <div className="hint">3–40 characters: letters, numbers, _ or -</div>
        </div>
        <div className="field">
          <label htmlFor="feedback-text">Feedback</label>
          <textarea
            id="feedback-text"
            className="textarea"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="The lectures were very useful and practical."
            maxLength={2000}
          />
          <div className="hint">English or Albanian · {trimmed.length}/2000 characters (min 10)</div>
        </div>

        <div className="form-row">
          <span className="hint">Analyzed with Google Cloud Natural Language API / Gemini</span>
          <button className="button primary" type="submit" disabled={!valid || submitting}>
            {submitting ? 'Analyzing…' : 'Submit'}
          </button>
        </div>

        {error && <div className="message error">Could not submit: {error}</div>}

        {result && (
          <div className="result" aria-live="polite">
            <div className="result-row">
              <strong>Result</strong>
              <SentimentBadge sentiment={result.sentiment} status={result.status} />
              <span>Score {formatScore(result.sentiment_score)}</span>
              {result.language && <span className="lang">{result.language}</span>}
            </div>
            {result.topics.length > 0 && (
              <div className="chips">
                {result.topics.map((t) => (
                  <span className="chip" key={t}>
                    {titleCase(t)}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </form>
    </div>
  )
}
