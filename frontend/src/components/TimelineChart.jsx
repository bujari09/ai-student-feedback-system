import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { formatDay } from '../format.js'
import { SENTIMENTS, SENTIMENT_LABELS, useChartColors } from '../theme.js'
import ChartTooltip from './ChartTooltip.jsx'

export default function TimelineChart({ analytics }) {
  const colors = useChartColors()
  const data = analytics.feedback_over_time.map((d) => ({ date: d.date, ...d.sentiment }))

  return (
    <div className="card">
      <h2 className="card-title">Feedback Over Time</h2>
      <p className="card-subtitle">Analyzed feedback per day, split by sentiment</p>

      <ul className="legend">
        {SENTIMENTS.map((s) => (
          <li key={s}>
            <span className="swatch" style={{ background: colors[s] }} />
            {SENTIMENT_LABELS[s]}
          </li>
        ))}
      </ul>

      {data.length === 0 ? (
        <div className="empty">No feedback yet</div>
      ) : (
        <div style={{ height: 240 }}>
          <ResponsiveContainer>
            <BarChart data={data} margin={{ top: 4, right: 8, bottom: 0, left: -16 }}>
              <CartesianGrid vertical={false} stroke={colors.grid} />
              <XAxis
                dataKey="date"
                tickFormatter={formatDay}
                tick={{ fill: colors.muted, fontSize: 12 }}
                axisLine={{ stroke: colors.axis }}
                tickLine={false}
              />
              <YAxis allowDecimals={false} tick={{ fill: colors.muted, fontSize: 12 }} axisLine={false} tickLine={false} />
              <Tooltip
                cursor={{ fill: colors.grid, opacity: 0.5 }}
                content={<ChartTooltip colors={colors} formatLabel={formatDay} />}
              />
              {SENTIMENTS.map((s, i) => (
                <Bar
                  key={s}
                  dataKey={s}
                  stackId="sentiment"
                  fill={colors[s]}
                  stroke={colors.surface}
                  strokeWidth={2}
                  maxBarSize={40}
                  radius={i === SENTIMENTS.length - 1 ? [4, 4, 0, 0] : 0}
                  isAnimationActive={false}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
