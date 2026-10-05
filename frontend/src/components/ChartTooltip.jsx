import { SENTIMENT_LABELS } from '../theme.js'

// Shared tooltip for the sentiment-split bar charts.
export default function ChartTooltip({ active, payload, label, colors, formatLabel = (l) => l }) {
  if (!active || !payload?.length) return null
  const total = payload.reduce((sum, item) => sum + (item.value ?? 0), 0)

  return (
    <div className="tooltip">
      <div className="tooltip-title">{formatLabel(label)}</div>
      {payload.map((item) => (
        <div className="tooltip-row" key={item.dataKey}>
          <span className="swatch" style={{ background: colors[item.dataKey] }} />
          {SENTIMENT_LABELS[item.dataKey]}
          <span className="value">{item.value}</span>
        </div>
      ))}
      <div className="tooltip-row">
        Total
        <span className="value">{total}</span>
      </div>
    </div>
  )
}
