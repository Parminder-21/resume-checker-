import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const optimizeResume = async (resumeText, jobDescription) => {
  const response = await api.post('/optimize', {
    resume_text: resumeText,
    job_description: jobDescription,
  });
  return response.data;
};

export const downloadPDF = async (optimizedResume) => {
  const response = await api.post(
    '/download',
    { optimized_resume: optimizedResume },
    { responseType: 'blob' }
  );
  
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'optimized_resume.pdf');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

export default api;
