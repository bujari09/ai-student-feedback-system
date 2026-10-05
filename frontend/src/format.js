const dateTime = new Intl.DateTimeFormat('en-GB', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
})

const shortDate = new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short' })

export const formatDateTime = (iso) => dateTime.format(new Date(iso))

// Backend dates are plain "YYYY-MM-DD"; parse as local date to avoid a timezone shift.
export const formatDay = (isoDate) => {
  const [y, m, d] = isoDate.split('-').map(Number)
  return shortDate.format(new Date(y, m - 1, d))
}

export const formatScore = (score) =>
  score === null || score === undefined ? '–' : `${score > 0 ? '+' : ''}${score.toFixed(2)}`

export const titleCase = (text) => text.replace(/\b\w/g, (c) => c.toUpperCase())
