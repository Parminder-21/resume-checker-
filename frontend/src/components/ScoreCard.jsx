import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { getScoreColor, scoreDelta } from '../utils/helpers.js'

const SCORE_ROWS = [
  { key: 'skills_match',     label: 'Skills Match',       icon: '🎯' },
  { key: 'experience_match', label: 'Experience Match',   icon: '💼' },
  { key: 'keyword_coverage', label: 'Keyword Coverage',   icon: '🔑' },
]

function AnimatedScore({ target, delay = 0 }) {
  const [display, setDisplay] = useState(0)

  useEffect(() => {
    let start = null
    const duration = 1000
    const step = (timestamp) => {
      if (!start) start = timestamp
      const progress = Math.min((timestamp - start) / duration, 1)
      setDisplay(Math.round(progress * target))
      if (progress < 1) requestAnimationFrame(step)
    }
    const timer = setTimeout(() => requestAnimationFrame(step), delay)
    return () => clearTimeout(timer)
  }, [target, delay])

  return <span>{display}</span>
}

function ScoreBar({ value, delay = 0, colorClass }) {
  return (
    <div className="score-bar-track flex-1">
      <motion.div
        className={`h-full rounded-full ${colorClass}`}
        initial={{ width: '0%' }}
        animate={{ width: `${value}%` }}
        transition={{ duration: 1.0, delay: delay / 1000, ease: 'easeOut' }}
      />
    </div>
  )
}

export default function ScoreCard({ initial, optimized }) {
  const initColor = getScoreColor(initial.overall)
  const optColor  = getScoreColor(optimized.overall)
  const delta     = scoreDelta(initial.overall, optimized.overall)

  return (
    <div className="glass-card p-6">
      <p className="section-title">ATS Score Analysis</p>

      {/* Big score comparison */}
      <div className="flex items-center justify-between mb-8">
        {/* Initial score */}
        <div className="text-center">
          <p className="text-xs text-slate-500 mb-1 uppercase tracking-wider">Before</p>
          <motion.p
            className={`text-5xl font-bold ${initColor.text}`}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <AnimatedScore target={Math.round(initial.overall)} delay={0} />
            <span className="text-2xl">%</span>
          </motion.p>
        </div>

        {/* Arrow + delta */}
        <div className="flex flex-col items-center gap-1">
          <motion.div
            className="text-2xl"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
          >
            →
          </motion.div>
          <motion.span
            className="text-green-400 font-bold text-sm bg-green-400/10 px-2 py-0.5 rounded-full"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.9 }}
          >
            {delta}%
          </motion.span>
        </div>

        {/* Optimized score */}
        <div className="text-center">
          <p className="text-xs text-slate-500 mb-1 uppercase tracking-wider">After</p>
          <motion.p
            className={`text-5xl font-bold ${optColor.text}`}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <AnimatedScore target={Math.round(optimized.overall)} delay={400} />
            <span className="text-2xl">%</span>
          </motion.p>
        </div>
      </div>

      {/* Breakdown rows */}
      <div className="space-y-4">
        {SCORE_ROWS.map(({ key, label, icon }, idx) => {
          const initVal = Math.round(initial[key])
          const optVal  = Math.round(optimized[key])
          const oc      = getScoreColor(optVal)

          return (
            <motion.div
              key={key}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 + idx * 0.15 }}
            >
              <div className="flex justify-between items-center mb-1.5">
                <span className="text-sm text-slate-300 flex items-center gap-2">
                  <span>{icon}</span> {label}
                </span>
                <span className="text-sm font-mono">
                  <span className="text-slate-500">{initVal}%</span>
                  <span className="text-slate-600 mx-1">→</span>
                  <span className={`font-semibold ${oc.text}`}>{optVal}%</span>
                </span>
              </div>
              <ScoreBar value={optVal} delay={500 + idx * 150} colorClass={oc.bar} />
            </motion.div>
          )
        })}

        {/* Formatting status */}
        <motion.div
          className="flex items-center justify-between pt-2 border-t border-white/10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.0 }}
        >
          <span className="text-sm text-slate-300 flex items-center gap-2">
            <span>📄</span> Formatting
          </span>
          <span className="text-sm text-green-400 font-medium">{optimized.formatting}</span>
        </motion.div>
      </div>
    </div>
  )
}