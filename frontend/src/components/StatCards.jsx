import { SENTIMENTS, SENTIMENT_LABELS } from '../theme.js'

export default function StatCards({ analytics }) {
  const { total_feedback, analyzed, pending, failed, sentiment_counts, sentiment_distribution } = analytics
  const notAnalyzed = pending + failed

  return (
    <section className="grid stats" aria-label="Summary statistics">
      <div className="card">
        <div className="stat-label">Total Feedback</div>
        <div className="stat-value">{total_feedback}</div>
        <div className="stat-detail">
          {analyzed} analyzed{notAnalyzed > 0 ? ` · ${notAnalyzed} not analyzed` : ''}
        </div>
      </div>
      {SENTIMENTS.map((sentiment) => (
        <div className="card" key={sentiment}>
          <div className="stat-label">
            <span className="swatch" style={{ background: `var(--${sentiment})` }} aria-hidden="true" />
            {SENTIMENT_LABELS[sentiment]}
          </div>
          <div className="stat-value">{sentiment_distribution[sentiment]}%</div>
          <div className="stat-detail">
            {sentiment_counts[sentiment]} of {analyzed} analyzed
          </div>
        </div>
      ))}
    </section>
  )
}
