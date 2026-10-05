import { useMemo, useState } from 'react'
import { formatDateTime, formatScore, titleCase } from '../format.js'
import { SENTIMENTS, SENTIMENT_LABELS } from '../theme.js'
import SentimentBadge from './SentimentBadge.jsx'

export default function FeedbackTable({ items }) {
  const [search, setSearch] = useState('')
  const [sentiment, setSentiment] = useState('all')

  const filtered = useMemo(() => {
    const term = search.trim().toLowerCase()
    return items.filter(
      (f) =>
        (sentiment === 'all' || f.sentiment === sentiment) &&
        (!term ||
          f.feedback_text.toLowerCase().includes(term) ||
          f.anonymous_student_id.toLowerCase().includes(term) ||
          f.topics.some((t) => t.includes(term))),
    )
  }, [items, search, sentiment])

  return (
    <div className="card">
      <h2 className="card-title">All Feedback</h2>
      <p className="card-subtitle">
        Showing {filtered.length} of {items.length}
      </p>

      <div className="table-tools">
        <input
          className="input"
          type="search"
          placeholder="Search text, student ID or topic…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="Search feedback"
        />
        <select
          className="select"
          value={sentiment}
          onChange={(e) => setSentiment(e.target.value)}
          aria-label="Filter by sentiment"
        >
          <option value="all">All sentiments</option>
          {SENTIMENTS.map((s) => (
            <option key={s} value={s}>
              {SENTIMENT_LABELS[s]}
            </option>
          ))}
        </select>
      </div>

      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Student</th>
              <th>Feedback</th>
              <th>Sentiment</th>
              <th>Score</th>
              <th>Topics</th>
              <th>Lang</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((f) => (
              <tr key={f.id}>
                <td className="date">{formatDateTime(f.created_at)}</td>
                <td>{f.anonymous_student_id}</td>
                <td className="text">{f.feedback_text}</td>
                <td>
                  <SentimentBadge sentiment={f.sentiment} status={f.status} />
                </td>
                <td className="num">{formatScore(f.sentiment_score)}</td>
                <td>
                  <div className="chips">
                    {f.topics.map((t) => (
                      <span className="chip" key={t}>
                        {titleCase(t)}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="lang">{f.language ?? '–'}</td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={7} className="empty" style={{ minHeight: 80 }}>
                  No feedback matches the filters
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
