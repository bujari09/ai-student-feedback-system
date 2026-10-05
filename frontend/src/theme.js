import { useEffect, useState } from 'react'

// Sentiment is a polarity, so it uses a diverging pair (blue = positive,
// red = negative) with a gray midpoint for neutral. Steps per mode were checked
// with a colour-vision-deficiency validator; neutral's low contrast is offset by
// always showing the label and value next to the mark.
const PALETTES = {
  light: {
    positive: '#2a78d6',
    neutral: '#a8a79f',
    negative: '#e34948',
    surface: '#fcfcfb',
    grid: '#e1e0d9',
    axis: '#c3c2b7',
    muted: '#898781',
  },
  dark: {
    positive: '#3987e5',
    neutral: '#5f5e59',
    negative: '#e66767',
    surface: '#1a1a19',
    grid: '#2c2c2a',
    axis: '#383835',
    muted: '#898781',
  },
}

export const SENTIMENTS = ['positive', 'neutral', 'negative']

export const SENTIMENT_LABELS = {
  positive: 'Positive',
  neutral: 'Neutral',
  negative: 'Negative',
}

const query = '(prefers-color-scheme: dark)'

export function useChartColors() {
  const [dark, setDark] = useState(() => window.matchMedia(query).matches)

  useEffect(() => {
    const media = window.matchMedia(query)
    const onChange = (event) => setDark(event.matches)
    media.addEventListener('change', onChange)
    return () => media.removeEventListener('change', onChange)
  }, [])

  return PALETTES[dark ? 'dark' : 'light']
}
