"""Module for detecting and extracting resume sections."""
import re


def detect_sections(resume_text: str) -> dict[str, str]:
    """
    Detect common resume sections and extract their content.
    
    Args:
        resume_text: Full resume text
        
    Returns:
        Dictionary mapping section names to their content
    """
    # Define common section headers (case-insensitive)
    section_patterns = {
        'contact': r'(?:contact|phone|email|location|address)',
        'summary': r'(?:professional summary|executive summary|objective|summary|profile)',
        'experience': r'(?:work experience|professional experience|employment|experience)',
        'education': r'(?:education|degree|university|college|academic)',
        'skills': r'(?:skills|technical skills|competencies|core competencies|expertise)',
        'certifications': r'(?:certifications|licenses|credentials|awards)',
        'projects': r'(?:projects|portfolio|notable projects)',
        'languages': r'(?:languages|language proficiency)',
    }
    
    sections = {key: "" for key in section_patterns.keys()}
    
    # Split text into lines for processing
    lines = resume_text.split('\n')
    
    # Find section boundaries
    section_indices = {}
    for i, line in enumerate(lines):
        line_lower = line.strip().lower()
        
        # Skip very short lines
        if len(line_lower) < 3:
            continue
        
        # Check if line matches any section header
        for section_name, pattern in section_patterns.items():
            if re.search(pattern, line_lower) and len(line_lower) < 50:
                # This looks like a section header
                if section_name not in section_indices:
                    section_indices[section_name] = i
    
    # Extract content for each section
    sorted_sections = sorted(section_indices.items(), key=lambda x: x[1])
    
    for idx, (section_name, start_line) in enumerate(sorted_sections):
        # Find the end line (start of next section or end of document)
        if idx + 1 < len(sorted_sections):
            end_line = sorted_sections[idx + 1][1]
        else:
            end_line = len(lines)
        
        # Combine lines in this section (skip the header line)
        section_content = '\n'.join(lines[start_line + 1:end_line])
        sections[section_name] = section_content.strip()
    
    return sections


def extract_section_content(resume_text: str, section_name: str) -> str:
    """
    Extract content for a specific section.
    
    Args:
        resume_text: Full resume text
        section_name: Name of section to extract (e.g., 'skills', 'experience')
        
    Returns:
        Content of the requested section
    """
    sections = detect_sections(resume_text)
    return sections.get(section_name, "")
