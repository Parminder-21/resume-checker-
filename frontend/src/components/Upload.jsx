import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileUp, Copy, Check } from 'lucide-react';

export const Upload = ({ onUpload, onJobDescriptionChange }) => {
  const [dragActive, setDragActive] = useState(false);
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [copiedID, setCopiedID] = useState(null);
  const [error, setError] = useState('');

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    setError('');

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const file = files[0];
      if (file.type === 'application/pdf') {
        setResumeFile(file);
        onUpload(file);
      } else {
        setError('Please upload a PDF file');
      }
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
      setError('');
      onUpload(file);
    } else if (file) {
      setError('Please upload a PDF file');
    }
  };

  const handleCopy = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedID(id);
    setTimeout(() => setCopiedID(null), 2000);
  };

  const handleJobDescriptionChange = (e) => {
    const text = e.target.value;
    setJobDescription(text);
    onJobDescriptionChange(text);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8"
    >
      {/* Resume Upload */}
      <div>
        <label className="block text-lg font-semibold text-slate-800 mb-4">
          📄 Upload Your Resume (PDF)
        </label>

        <motion.div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          animate={{
            borderColor: dragActive ? '#3B82F6' : '#e2e8f0',
            backgroundColor: dragActive ? '#f0f4ff' : 'white',
          }}
          className="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all"
        >
          <FileUp size={48} className="mx-auto mb-4 text-blue-500" />
          <p className="text-lg font-medium text-slate-700 mb-2">
            Drag and drop your resume here
          </p>
          <p className="text-sm text-slate-500 mb-4">or click to select a file</p>

          <input
            type="file"
            accept=".pdf"
            onChange={handleFileInput}
            className="hidden"
            id="pdf-upload"
          />
          <label
            htmlFor="pdf-upload"
            className="inline-block px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors cursor-pointer"
          >
            Select PDF
          </label>

          {resumeFile && (
            <p className="text-sm text-green-600 mt-4 flex items-center justify-center gap-2">
              ✓ {resumeFile.name}
            </p>
          )}
        </motion.div>

        {error && (
          <p className="text-sm text-red-600 mt-2">{error}</p>
        )}
      </div>

      {/* Job Description Input */}
      <div>
        <label className="block text-lg font-semibold text-slate-800 mb-4">
          💼 Paste the Job Description
        </label>

        <textarea
          value={jobDescription}
          onChange={handleJobDescriptionChange}
          placeholder="Paste the complete job description here... The more details, the better our optimization!"
          rows={8}
          className="w-full p-4 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        />

        <p className="text-sm text-slate-500 mt-2">
          💡 Include required skills, responsibilities, and qualifications
        </p>
      </div>

      {/* Sample Data Section */}
      <details className="bg-slate-50 p-4 rounded-lg">
        <summary className="cursor-pointer font-medium text-slate-700">
          📋 Click here to see sample data (for testing)
        </summary>
        <div className="mt-4 space-y-4">
          <div>
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-slate-700">Sample Resume</h4>
              <button
                onClick={() => handleCopy(SAMPLE_RESUME, 'resume')}
                className="flex items-center gap-2 px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                {copiedID === 'resume' ? (
                  <><Check size={16} /> Copied</>
                ) : (
                  <><Copy size={16} /> Copy</>
                )}
              </button>
            </div>
            <pre className="mt-2 p-2 bg-white text-sm overflow-auto max-h-40 text-slate-700">
              {SAMPLE_RESUME}
            </pre>
          </div>

          <div>
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-slate-700">Sample Job Description</h4>
              <button
                onClick={() => handleCopy(SAMPLE_JD, 'jd')}
                className="flex items-center gap-2 px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                {copiedID === 'jd' ? (
                  <><Check size={16} /> Copied</>
                ) : (
                  <><Copy size={16} /> Copy</>
                )}
              </button>
            </div>
            <pre className="mt-2 p-2 bg-white text-sm overflow-auto max-h-40 text-slate-700">
              {SAMPLE_JD}
            </pre>
          </div>
        </div>
      </details>
    </motion.div>
  );
};

const SAMPLE_RESUME = `John Doe
john.doe@email.com | LinkedIn.com/in/johndoe

EXPERIENCE
Backend Developer at Tech Corp (Jan 2022 - Present)
Built REST APIs for microservices
Worked with Python and FastAPI
Managed database migrations
Deployed to AWS using Docker

Junior Developer at StartupXYZ (Jun 2021 - Dec 2021)
Built simple web features
Used JavaScript and React
Fixed bugs in the codebase

EDUCATION
B.S. Computer Science
Tech University (2021)

SKILLS
Python, JavaScript, React, FastAPI, SQL, AWS, Docker, Git`;

const SAMPLE_JD = `We are looking for a Senior Backend Engineer to join our team!

RESPONSIBILITIES:
- Design and develop scalable REST APIs
- Architect microservices using Python and FastAPI
- Implement CI/CD pipelines
- Optimize database queries and performance
- Lead code reviews and mentor junior developers
- Deploy and manage applications on AWS

REQUIRED SKILLS:
- 3+ years of backend development experience
- Strong Python knowledge (FastAPI/Django proficiency)
- Experience with AWS services (EC2, RDS, S3, Lambda)
- Docker and Kubernetes expertise
- SQL and NoSQL databases
- CI/CD pipeline setup (Jenkins, GitLab CI)
- GraphQL experience
- Microservices architecture knowledge

PREFERRED:
- Experience with monitoring and logging tools
- Knowledge of design patterns
- API documentation experience
- TDD and unit testing`;
