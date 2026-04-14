import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Loader } from '../components/Loader';
import { Upload } from '../components/Upload';
import { Result } from './Result';
import { optimizeResume, uploadResume } from '../services/api';

const STEPS = {
  UPLOAD: 'upload',
  PROCESSING: 'processing',
  RESULTS: 'results',
};

function App() {
  const [step, setStep] = useState(STEPS.UPLOAD);
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);

  const handleResumeUpload = async (file) => {
    try {
      setError('');
      setUploadedFile(file);
      const response = await uploadResume(file);
      setResumeText(response.resume_text);
    } catch (err) {
      setError('Failed to upload resume. Please try again.');
      console.error(err);
    }
  };

  const handleJobDescriptionChange = (text) => {
    setJobDescription(text);
  };

  const handleOptimize = async () => {
    if (!resumeText.trim()) {
      setError('Please upload a resume first');
      return;
    }
    if (!jobDescription.trim()) {
      setError('Please paste a job description');
      return;
    }

    try {
      setError('');
      setStep(STEPS.PROCESSING);
      
      const response = await optimizeResume(resumeText, jobDescription);
      
      setResults(response);
      setStep(STEPS.RESULTS);
    } catch (err) {
      setError('Failed to optimize resume. Please try again.');
      setStep(STEPS.UPLOAD);
      console.error(err);
    }
  };

  const handleReset = () => {
    setStep(STEPS.UPLOAD);
    setResumeText('');
    setJobDescription('');
    setResults(null);
    setError('');
    setUploadedFile(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
          <motion.h1
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-3xl sm:text-4xl font-bold text-slate-800"
          >
            🎯 OptiResume AI
          </motion.h1>
          <p className="text-slate-600 mt-1">
            Real-time ATS Simulator & Resume Optimizer with Measurable Improvement
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        {step === STEPS.PROCESSING && <Loader />}

        {step === STEPS.UPLOAD && (
          <motion.div
            key="upload"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-8"
          >
            <Upload
              onUpload={handleResumeUpload}
              onJobDescriptionChange={handleJobDescriptionChange}
            />

            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700"
              >
                ❌ {error}
              </motion.div>
            )}

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleOptimize}
              disabled={!resumeText || !jobDescription}
              className="w-full py-4 px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold rounded-lg text-lg transition-all shadow-lg"
            >
              {resumeText && jobDescription
                ? '🚀 Optimize My Resume'
                : '⏳ Complete the form above'}
            </motion.button>
          </motion.div>
        )}

        {step === STEPS.RESULTS && results && (
          <Result results={results} onReset={handleReset} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-12 py-6">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-slate-600">
            🏆 OptiResume AI v1.0.0 | Hackathon Edition | Built for job seekers
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
