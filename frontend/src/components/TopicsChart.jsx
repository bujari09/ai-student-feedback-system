import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { titleCase } from '../format.js'
import { SENTIMENTS, SENTIMENT_LABELS, useChartColors } from '../theme.js'
import ChartTooltip from './ChartTooltip.jsx'

export default function TopicsChart({ analytics }) {
  const colors = useChartColors()
  const data = analytics.top_topics.map((t) => ({ topic: t.topic, count: t.count, ...t.sentiment }))
  const height = Math.max(200, data.length * 36 + 40)

  return (
    <div className="card">
      <h2 className="card-title">Top Topics</h2>
      <p className="card-subtitle">Most mentioned topics, split by sentiment</p>

      <ul className="legend">
        {SENTIMENTS.map((s) => (
          <li key={s}>
            <span className="swatch" style={{ background: colors[s] }} />
            {SENTIMENT_LABELS[s]}
          </li>
        ))}
      </ul>

      {data.length === 0 ? (
        <div className="empty">No topics identified yet</div>
      ) : (
        <div style={{ height }}>
          <ResponsiveContainer>
            <BarChart data={data} layout="vertical" margin={{ top: 0, right: 16, bottom: 0, left: 0 }} barCategoryGap={8}>
              <CartesianGrid horizontal={false} stroke={colors.grid} />
              <XAxis
                type="number"
                allowDecimals={false}
                tick={{ fill: colors.muted, fontSize: 12 }}
                axisLine={{ stroke: colors.axis }}
                tickLine={false}
              />
              <YAxis
                type="category"
                dataKey="topic"
                width={130}
                tickFormatter={titleCase}
                tick={{ fill: 'currentColor', fontSize: 13 }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                cursor={{ fill: colors.grid, opacity: 0.5 }}
                content={<ChartTooltip colors={colors} formatLabel={titleCase} />}
              />
              {SENTIMENTS.map((s, i) => (
                <Bar
                  key={s}
                  dataKey={s}
                  stackId="sentiment"
                  fill={colors[s]}
                  stroke={colors.surface}
                  strokeWidth={2}
                  maxBarSize={22}
                  radius={i === SENTIMENTS.length - 1 ? [0, 4, 4, 0] : 0}
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
