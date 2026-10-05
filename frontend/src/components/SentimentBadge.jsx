import { SENTIMENT_LABELS } from '../theme.js'

const ICONS = { positive: '▲', neutral: '●', negative: '▼' }

// Sentiment is shown as icon + text + colour, never colour alone.
export default function SentimentBadge({ sentiment, status }) {
  if (status === 'pending') return <span className="badge pending">Pending</span>
  if (status === 'failed' || !sentiment) return <span className="badge failed">Not analyzed</span>
  return (
    <span className={`badge ${sentiment}`}>
      <span aria-hidden="true">{ICONS[sentiment]}</span>
      {SENTIMENT_LABELS[sentiment]}
    </span>
  )
}
