import { formatDateTime, titleCase } from '../format.js'
import SentimentBadge from './SentimentBadge.jsx'

export default function RecentFeedback({ items }) {
  const recent = items.slice(0, 5)

  return (
    <div className="card">
      <h2 className="card-title">Recent Feedback</h2>
      <p className="card-subtitle">The latest {recent.length} comments</p>

      {recent.length === 0 ? (
        <div className="empty">No feedback yet</div>
      ) : (
        <ul className="recent">
          {recent.map((f) => (
            <li key={f.id}>
              <p className="recent-text">{f.feedback_text}</p>
              <div className="recent-meta">
                <SentimentBadge sentiment={f.sentiment} status={f.status} />
                {f.topics.map((t) => (
                  <span className="chip" key={t}>
                    {titleCase(t)}
                  </span>
                ))}
                <span>
                  {f.anonymous_student_id} · {formatDateTime(f.created_at)}
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
