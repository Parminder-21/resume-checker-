import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp } from 'lucide-react';
import { getScoreColor, formatScore } from '../utils/helpers';

export const ScoreCard = ({ scores }) => {
  const { initial, optimized } = scores || { initial: {}, optimized: {} };

  const metrics = [
    { label: 'Skills Match', key: 'skills_match' },
    { label: 'Experience Match', key: 'experience_match' },
    { label: 'Keyword Coverage', key: 'keyword_coverage' },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-lg p-8 space-y-6"
    >
      {/* Main Score */}
      <div className="text-center">
        <p className="text-sm font-medium text-slate-500 mb-2">OVERALL ATS MATCH</p>
        <div className="flex items-center justify-center gap-4">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className={`text-4xl font-bold ${getScoreColor(initial.overall || 0)}`}
          >
            {formatScore(initial.overall || 0)}
          </motion.div>
          <TrendingUp size={32} className="text-green-500" />
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2 }}
            className={`text-4xl font-bold ${getScoreColor(optimized.overall || 0)}`}
          >
            {formatScore(optimized.overall || 0)}
          </motion.div>
        </div>
        <p className="text-sm text-slate-500 mt-4">
          ✨ Improvement: +{Math.round((optimized.overall || 0) - (initial.overall || 0))}%
        </p>
      </div>

      <hr className="border-slate-200" />

      {/* Detailed Metrics */}
      <div className="space-y-3">
        {metrics.map((metric, idx) => (
          <motion.div
            key={metric.key}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="space-y-1"
          >
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-slate-700">
                ✅ {metric.label}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex-grow bg-slate-200 h-2 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${initial[metric.key] || 0}%` }}
                  transition={{ duration: 0.5, delay: 0.3 }}
                  className="h-full bg-blue-400"
                />
              </div>
              <span className="text-xs font-medium text-slate-600 w-8">
                {formatScore(initial[metric.key] || 0)}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex-grow bg-slate-200 h-2 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${optimized[metric.key] || 0}%` }}
                  transition={{ duration: 0.5, delay: 0.5 }}
                  className="h-full bg-green-400"
                />
              </div>
              <span className="text-xs font-medium text-green-600 w-8">
                {formatScore(optimized[metric.key] || 0)}
              </span>
            </div>
          </motion.div>
        ))}
      </div>

      <hr className="border-slate-200" />

      {/* Formatting Status */}
      <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
        <span className="text-sm font-medium text-slate-700">Formatting</span>
        <span className="text-sm font-semibold text-green-700">✔ ATS Safe</span>
      </div>
    </motion.div>
  );
};
