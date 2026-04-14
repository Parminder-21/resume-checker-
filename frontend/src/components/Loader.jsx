import React from 'react';
import { motion } from 'framer-motion';

export const Loader = () => {
  const steps = [
    'Parsing resume...',
    'Analyzing job description...',
    'Computing semantic match...',
    'Optimizing with AI...',
    'Generating your results...',
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-white rounded-lg p-8 w-96 shadow-2xl"
      >
        <h2 className="text-2xl font-bold text-center mb-8 text-slate-800">
          Optimizing Your Resume
        </h2>

        <div className="space-y-4">
          {steps.map((step, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.3 }}
              className="flex items-center gap-3"
            >
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-5 h-5 border-2 border-blue-400 border-t-blue-600 rounded-full"
              />
              <span className="text-slate-600">{step}</span>
            </motion.div>
          ))}
        </div>

        <motion.div
          animate={{ width: ['0%', '100%'] }}
          transition={{ duration: 8, ease: 'easeInOut' }}
          className="mt-8 h-1 bg-blue-500 rounded-full"
        />

        <p className="text-center text-sm text-slate-500 mt-4">
          This usually takes 5-10 seconds...
        </p>
      </motion.div>
    </div>
  );
};
