import React from 'react';
import { motion } from 'framer-motion';
import { Diff } from 'lucide-react';

export const ResumeDiff = ({ diffs }) => {
  const changedDiffs = diffs.filter(d => d.changed && d.original !== d.optimized).slice(0, 8);

  if (!changedDiffs || changedDiffs.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-lg shadow-lg p-8 text-center"
      >
        <p className="text-slate-500">No significant changes made.</p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-lg p-8"
    >
      <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
        <Diff size={24} /> Resume Improvements
      </h3>

      <div className="space-y-4">
        {changedDiffs.map((diff, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: idx * 0.1 }}
            className="border border-slate-200 rounded-lg overflow-hidden"
          >
            <div className="grid grid-cols-2 gap-0">
              {/* Original */}
              <div className="bg-red-50 p-4 border-r border-slate-200">
                <p className="text-xs font-semibold text-red-700 uppercase mb-2">
                  Original
                </p>
                <p className="text-sm text-slate-700 line-through">
                  {diff.original}
                </p>
              </div>

              {/* Optimized */}
              <div className="bg-green-50 p-4">
                <p className="text-xs font-semibold text-green-700 uppercase mb-2">
                  Optimized
                </p>
                <p className="text-sm text-slate-700 font-medium">
                  {highlightChanges(diff.original, diff.optimized)}
                </p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <p className="text-xs text-slate-500 mt-6 text-center">
        Showing top {changedDiffs.length} improvements out of {diffs.length} total changes
      </p>
    </motion.div>
  );
};

// Helper function to highlight what changed
const highlightChanges = (original, optimized) => {
  // Simple highlighting - in a real app, use a diffing library
  const origWords = original.split(' ');
  const optWords = optimized.split(' ');

  return (
    <span>
      {optWords.map((word, idx) => {
        const isNew = !origWords.includes(word);
        return (
          <span
            key={idx}
            className={isNew ? 'font-semibold text-green-700' : ''}
          >
            {word}{' '}
          </span>
        );
      })}
    </span>
  );
};
