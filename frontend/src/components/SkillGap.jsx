import React from 'react';
import { motion } from 'framer-motion';
import { getPriorityColor, getPriorityIcon } from '../utils/helpers';
import { AlertCircle } from 'lucide-react';

export const SkillGap = ({ gaps }) => {
  if (!gaps || gaps.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-lg p-8 text-center"
      >
        <AlertCircle size={48} className="mx-auto text-green-500 mb-4" />
        <p className="text-lg font-semibold text-slate-700">
          🎉 No major skill gaps detected!
        </p>
        <p className="text-sm text-slate-500 mt-2">
          Your resume aligns well with the job description.
        </p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-lg p-8"
    >
      <h3 className="text-xl font-bold text-slate-800 mb-6">
        🎯 Missing Skills & Experience
      </h3>

      <div className="space-y-3">
        {gaps.slice(0, 10).map((gap, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.05 }}
            className={`p-3 rounded-lg flex items-center justify-between ${getPriorityColor(gap.priority)}`}
          >
            <div className="flex items-center gap-2">
              <span className="text-xl">{getPriorityIcon(gap.priority)}</span>
              <span className="font-medium">{gap.skill}</span>
            </div>
            <span className="text-xs font-semibold px-2 py-1 rounded bg-white bg-opacity-50">
              {gap.priority}
            </span>
          </motion.div>
        ))}
      </div>

      <p className="text-xs text-slate-500 mt-6 text-center">
        💡 Focus on high-priority skills first to maximize your match score
      </p>
    </motion.div>
  );
};
