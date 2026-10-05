import { useCallback, useEffect, useState } from 'react'
import { api } from './api/client.js'
import FeedbackForm from './components/FeedbackForm.jsx'
import FeedbackTable from './components/FeedbackTable.jsx'
import RecentFeedback from './components/RecentFeedback.jsx'
import SentimentChart from './components/SentimentChart.jsx'
import StatCards from './components/StatCards.jsx'
import TimelineChart from './components/TimelineChart.jsx'
import TopicsChart from './components/TopicsChart.jsx'

const REFRESH_MS = 30_000

export default function App() {
  const [analytics, setAnalytics] = useState(null)
  const [feedback, setFeedback] = useState([])
  const [health, setHealth] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [updatedAt, setUpdatedAt] = useState(null)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const [analyticsData, feedbackData, healthData] = await Promise.all([
        api.analytics(),
        api.listFeedback(200),
        api.health(),
      ])
      setAnalytics(analyticsData)
      setFeedback(feedbackData.items)
      setHealth(healthData)
      setError(null)
      setUpdatedAt(new Date())
    } catch (err) {
      setError(err.message)
      setHealth(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
    const timer = setInterval(load, REFRESH_MS)
    return () => clearInterval(timer)
  }, [load])

  const apiOk = health?.status === 'ok'

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>AI Student Feedback System</h1>
          <p>Sentiment and topic analysis of anonymous student feedback · Google Cloud</p>
        </div>
        <div className="header-actions">
          <span className={`status-dot ${health ? (apiOk ? 'ok' : 'down') : error ? 'down' : ''}`}>
            {health ? (apiOk ? 'API online' : 'API degraded') : error ? 'API offline' : 'Connecting…'}
          </span>
          {updatedAt && <span>Updated {updatedAt.toLocaleTimeString('en-GB')}</span>}
          <button className="button" onClick={load} disabled={loading}>
            {loading ? 'Refreshing…' : 'Refresh'}
          </button>
        </div>
      </header>

      {error && !analytics && (
        <div className="card message error" role="alert">
          Could not load data from the API: {error}
        </div>
      )}

      {analytics && (
        <>
          <StatCards analytics={analytics} />

          <section className="grid two">
            <SentimentChart analytics={analytics} />
            <TopicsChart analytics={analytics} />
          </section>

          <section className="grid">
            <TimelineChart analytics={analytics} />
          </section>

          <section className="grid halves">
            <FeedbackForm onSubmitted={load} />
            <RecentFeedback items={feedback} />
          </section>

          <section className="grid">
            <FeedbackTable items={feedback} />
          </section>
        </>
      )}

      <footer className="footer">
        FastAPI · Firestore · Cloud Natural Language API · Vertex AI Gemini · React
      </footer>
    </div>
  )
}
