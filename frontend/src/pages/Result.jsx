import React from 'react';
import { motion } from 'framer-motion';
import { Download, ArrowLeft } from 'lucide-react';
import { ScoreCard } from './ScoreCard';
import { SkillGap } from './SkillGap';
import { ResumeDiff } from './ResumeDiff';
import { downloadPDF } from '../services/api';

export const Result = ({ results, onReset }) => {
  const handleDownload = async () => {
    try {
      await downloadPDF(results.optimized_resume);
    } catch (error) {
      alert('Error downloading PDF. Please try again.');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8"
    >
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-slate-800 mb-2">
          ✨ Your Resume is Ready!
        </h1>
        <p className="text-lg text-slate-600">
          See your improvements below and download your optimized resume.
        </p>
      </div>

      {/* Main Results Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <ScoreCard scores={results.scores} />
        <SkillGap gaps={results.skill_gaps} />
      </div>

      {/* Resume Diff */}
      <ResumeDiff diffs={results.diff} />

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleDownload}
          className="flex items-center justify-center gap-2 px-8 py-4 bg-green-500 hover:bg-green-600 text-white font-bold rounded-lg transition-all shadow-lg"
        >
          <Download size={20} />
          Download Optimized PDF
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onReset}
          className="flex items-center justify-center gap-2 px-8 py-4 bg-slate-500 hover:bg-slate-600 text-white font-bold rounded-lg transition-all shadow-lg"
        >
          <ArrowLeft size={20} />
          Try Another Resume
        </motion.button>
      </div>

      {/* Results Summary */}
      <div className="bg-blue-50 p-6 rounded-lg text-center">
        <p className="text-sm text-slate-600">
          💡 Pro tip: You can copy the optimized resume and use it for all job applications. Every resume is tailored to the specific job!
        </p>
      </div>
    </motion.div>
  );
};
