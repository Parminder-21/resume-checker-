"""Module for extracting skills from resume and job descriptions."""
import re
import json
import os


# Common technical and soft skills database
COMMON_SKILLS = {
    # Programming languages
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust', 'Ruby',
    'PHP', 'Swift', 'Kotlin', 'R', 'MATLAB', 'Scala', 'Perl', 'Lua', 'Haskell',
    
    # Web technologies
    'React', 'Vue', 'Angular', 'Node.js', 'Express', 'Django', 'Flask', 'FastAPI',
    'Spring', 'ASP.NET', 'HTML', 'CSS', 'SQL', 'GraphQL', 'REST', 'WebSocket',
    
    # Databases
    'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'DynamoDB', 'Cassandra', 'ElasticSearch',
    'Oracle', 'SQLite', 'MariaDB', 'Firebase', 'Firestore',
    
    # Cloud & DevOps
    'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes', 'CI/CD',
    'Jenkins', 'GitHub Actions', 'GitLab CI', 'Terraform', 'CloudFormation',
    'Lambda', 'EC2', 'RDS', 'S3', 'ECS', 'EKS', 'AppEngine', 'Cloud Functions',
    
    # Data & ML
    'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn',
    'Pandas', 'NumPy', 'Data Analysis', 'Statistics', 'Big Data', 'Spark',
    'Hadoop', 'Kafka', 'Data Visualization', 'Analytics',
    
    # Soft skills
    'Leadership', 'Communication', 'Project Management', 'Agile', 'Scrum',
    'Problem Solving', 'Team Collaboration', 'Critical Thinking', 'Attention to Detail',
    'Time Management', 'Adaptability', 'Creativity', 'Documentation',
    
    # Other tools
    'Git', 'Linux', 'Windows', 'macOS', 'Bash', 'Shell', 'Vim', 'VS Code',
    'JetBrains', 'Postman', 'Jira', 'Confluence', 'Slack', 'Figma', 'Adobe',
}


def extract_skills(text: str) -> list[dict]:
    """
    Extract skills from text (resume or job description).
    
    Args:
        text: Text to search for skills
        
    Returns:
        List of dicts: [{"skill": "Python", "count": 2, "in_required": False}, ...]
    """
    text_lower = text.lower()
    skill_counts = {}
    skill_sections = {}
    
    # Check for "required" or "must have" section
    required_section = ""
    if re.search(r'(required|must have|mandatory)', text_lower):
        match = re.search(
            r'(required|must have|mandatory)[:\s]+(.*?)(?=\n\s*\n|\Z)',
            text_lower,
            re.DOTALL | re.IGNORECASE
        )
        if match:
            required_section = match.group(2).lower()
    
    # Count skill occurrences
    for skill in COMMON_SKILLS:
        skill_lower = skill.lower()
        
        # Count occurrences in full text
        count = len(re.findall(r'\b' + re.escape(skill_lower) + r'\b', text_lower))
        
        if count > 0:
            in_required = skill_lower in required_section if required_section else False
            skill_counts[skill] = {
                "count": count,
                "in_required": in_required
            }
    
    # Convert to list and sort by count (descending)
    skills_list = [
        {
            "skill": skill,
            "count": data["count"],
            "in_required": data["in_required"]
        }
        for skill, data in skill_counts.items()
    ]
    
    # Sort by: in_required (True first), then count (descending)
    skills_list.sort(
        key=lambda x: (-int(x["in_required"]), -x["count"])
    )
    
    return skills_list


def extract_skill_names(text: str) -> list[str]:
    """
    Extract unique skill names from text.
    
    Args:
        text: Text to search for skills
        
    Returns:
        List of unique skill names found
    """
    skills = extract_skills(text)
    return [s["skill"] for s in skills]


def load_master_skills(json_path: str = None) -> dict:
    """
    Load skill categories from master skills JSON file.
    
    Args:
        json_path: Optional path to master_skills.json
        
    Returns:
        Dictionary of skill categories
    """
    if json_path is None:
        # Try to find master_skills.json in data directory
        json_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', 'data', 'skills', 'master_skills.json'
        )
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    return {}
