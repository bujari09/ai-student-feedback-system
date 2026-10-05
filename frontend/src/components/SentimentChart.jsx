import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import { SENTIMENTS, SENTIMENT_LABELS, useChartColors } from '../theme.js'

function DonutTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const { name, value, percent } = payload[0].payload
  return (
    <div className="tooltip">
      <div className="tooltip-title">{SENTIMENT_LABELS[name]}</div>
      <div className="tooltip-row">
        Feedback <span className="value">{value}</span>
      </div>
      <div className="tooltip-row">
        Share <span className="value">{percent}%</span>
      </div>
    </div>
  )
}

export default function SentimentChart({ analytics }) {
  const colors = useChartColors()
  const { analyzed, sentiment_counts, sentiment_distribution } = analytics
  const data = SENTIMENTS.map((s) => ({
    name: s,
    value: sentiment_counts[s],
    percent: sentiment_distribution[s],
  }))

  return (
    <div className="card">
      <h2 className="card-title">Sentiment Distribution</h2>
      <p className="card-subtitle">Share of analyzed feedback by sentiment</p>

      <ul className="legend">
        {data.map((d) => (
          <li key={d.name}>
            <span className="swatch" style={{ background: colors[d.name] }} />
            {SENTIMENT_LABELS[d.name]} <span className="value">{d.percent}%</span>
          </li>
        ))}
      </ul>

      {analyzed === 0 ? (
        <div className="empty">No analyzed feedback yet</div>
      ) : (
        <div className="chart-wrap" style={{ height: 240 }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={data.filter((d) => d.value > 0)}
                dataKey="value"
                nameKey="name"
                innerRadius="62%"
                outerRadius="92%"
                startAngle={90}
                endAngle={-270}
                stroke={colors.surface}
                strokeWidth={2}
                isAnimationActive={false}
              >
                {data
                  .filter((d) => d.value > 0)
                  .map((d) => (
                    <Cell key={d.name} fill={colors[d.name]} />
                  ))}
              </Pie>
              <Tooltip content={<DonutTooltip />} />
            </PieChart>
          </ResponsiveContainer>
          <div className="donut-center">
            <strong>{analyzed}</strong>
            <span>analyzed</span>
          </div>
        </div>
      )}
    </div>
  )
}
