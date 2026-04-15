import axios from 'axios'

const BASE_URL = '/api/v1'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 60000, // 60s — Claude can be slow
})

// ─── Upload ───────────────────────────────────────────────────────────────────

/**
 * Upload a PDF resume and get back extracted text.
 * @param {File} file  - PDF file object
 * @returns {Promise<{ resume_text, char_count, sections_detected }>}
 */
export const uploadResume = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  const res = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

// ─── Optimize ─────────────────────────────────────────────────────────────────

/**
 * Run the full optimization pipeline.
 * @param {string} resumeText      - Extracted or pasted resume text
 * @param {string} jobDescription  - Pasted job description
 * @returns {Promise<OptimizeResponse>}
 *
 * OptimizeResponse shape:
 * {
 *   scores: {
 *     initial:   { overall, skills_match, experience_match, keyword_coverage, formatting },
 *     optimized: { overall, skills_match, experience_match, keyword_coverage, formatting }
 *   },
 *   skill_gaps:       [{ skill, priority }],
 *   optimized_resume: string,
 *   diff:             [{ original, optimized, changed }]
 * }
 */
export const optimizeResume = async (resumeText, jobDescription) => {
  const res = await api.post('/optimize', {
    resume_text:     resumeText,
    job_description: jobDescription,
  })
  return res.data
}

// ─── Download ─────────────────────────────────────────────────────────────────

/**
 * Generate and download the optimized resume as PDF.
 * @param {string} optimizedResume  - Optimized resume text
 * @param {string} candidateName    - Name for the PDF filename
 */
export const downloadPDF = async (optimizedResume, candidateName = 'Candidate') => {
  const res = await api.post(
    '/download',
    { optimized_resume: optimizedResume, candidate_name: candidateName },
    { responseType: 'blob' }
  )

  const url  = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
  const link = document.createElement('a')
  link.href  = url
  link.setAttribute('download', `${candidateName.replace(/\s+/g, '_')}_optimized_resume.pdf`)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

// ─── Health ───────────────────────────────────────────────────────────────────

export const checkHealth = async () => {
  const res = await api.get('/health')
  return res.data
}