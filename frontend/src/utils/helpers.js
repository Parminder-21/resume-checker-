/**
 * Returns Tailwind color classes based on ATS score value.
 */
export const getScoreColor = (score) => {
  if (score >= 75) return { text: 'text-green-400',  bar: 'bg-green-500',  glow: 'shadow-green-500/30'  }
  if (score >= 50) return { text: 'text-yellow-400', bar: 'bg-yellow-500', glow: 'shadow-yellow-500/30' }
  return              { text: 'text-red-400',    bar: 'bg-red-500',    glow: 'shadow-red-500/30'    }
}

/**
 * Returns Tailwind classes for skill priority badge.
 */
export const getPriorityStyle = (priority) => {
  const map = {
    High:   'tag-high',
    Medium: 'tag-medium',
    Low:    'tag-low',
  }
  return map[priority] || 'tag-low'
}

/**
 * Returns priority dot color.
 */
export const getPriorityDot = (priority) => {
  const map = {
    High:   'bg-red-400',
    Medium: 'bg-yellow-400',
    Low:    'bg-green-400',
  }
  return map[priority] || 'bg-slate-400'
}

/**
 * Format score delta for display.
 * e.g. 42 → 78 returns "+36"
 */
export const scoreDelta = (initial, optimized) => {
  const delta = Math.round(optimized - initial)
  return delta >= 0 ? `+${delta}` : `${delta}`
}

/**
 * Truncate long text for display.
 */
export const truncate = (text, maxLen = 120) => {
  if (!text) return ''
  return text.length > maxLen ? text.slice(0, maxLen) + '…' : text
}

/**
 * Count changed bullets in diff.
 */
export const countChanges = (diff) => {
  if (!diff) return 0
  return diff.filter(item => item.changed).length
}

/**
 * Processing step messages shown during loading animation.
 */
export const PROCESSING_STEPS = [
  { label: 'Parsing resume structure...',        duration: 1200 },
  { label: 'Analyzing job description...',       duration: 1400 },
  { label: 'Computing semantic match...',        duration: 1600 },
  { label: 'Detecting skill gaps...',            duration: 1200 },
  { label: 'Rewriting bullets with AI...',       duration: 2200 },
  { label: 'Scoring optimized resume...',        duration: 1200 },
  { label: 'Generating results...',              duration: 800  },
]