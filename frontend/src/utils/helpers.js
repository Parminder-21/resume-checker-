// Utility functions for the frontend

export const getScoreColor = (score) => {
  if (score >= 80) return 'text-green-600 bg-green-50';
  if (score >= 60) return 'text-blue-600 bg-blue-50';
  if (score >= 40) return 'text-yellow-600 bg-yellow-50';
  return 'text-red-600 bg-red-50';
};

export const getPriorityColor = (priority) => {
  switch (priority) {
    case 'High':
      return 'bg-red-100 text-red-800';
    case 'Medium':
      return 'bg-yellow-100 text-yellow-800';
    case 'Low':
      return 'bg-green-100 text-green-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export const getPriorityIcon = (priority) => {
  switch (priority) {
    case 'High':
      return '🔴';
    case 'Medium':
      return '🟡';
    case 'Low':
      return '🟢';
    default:
      return '⚫';
  }
};

export const formatScore = (score) => {
  return Math.round(score) + '%';
};

export const highlightDifferences = (original, optimized) => {
  // Simple implementation - can be enhanced
  return {
    added: optimized.split(' ').filter(word => !original.includes(word)),
    removed: original.split(' ').filter(word => !optimized.includes(word)),
  };
};
