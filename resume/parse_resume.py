#!/usr/bin/env python3
"""
Resume Parser - Extracts text from PDF resume and parses it into sections
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# Get the absolute path of the resume
RESUME_PATH = "/Users/alexanderfedin/Library/CloudStorage/OneDrive-Personal/Jobs/AI/resume/versions/AlexanderFedin_2025-01-21.pdf"
OUTPUT_DIR = "/Users/alexanderfedin/Library/CloudStorage/OneDrive-Personal/Jobs/AI/resume/sections"

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using macOS built-in tools"""
    try:
        # Try using textutil (macOS)
        result = subprocess.run(
            ["textutil", "-convert", "txt", "-stdout", pdf_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except (subprocess.SubprocessError, FileNotFoundError):
        try:
            # Fallback to pdftotext if available
            result = subprocess.run(
                ["pdftotext", pdf_path, "-"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Error: Could not extract text from PDF")
            print("Neither textutil nor pdftotext are available")
            return None

def identify_sections(text):
    """Identify sections in the resume text"""
    # Common resume section headers
    sections = {
        "summary": r"(?:SUMMARY|PROFESSIONAL\s+SUMMARY|PROFILE)",
        "skills": r"(?:SKILLS|TECHNICAL\s+SKILLS|EXPERTISE|TECHNOLOGIES)",
        "experience": r"(?:EXPERIENCE|WORK\s+EXPERIENCE|PROFESSIONAL\s+EXPERIENCE|EMPLOYMENT)",
        "education": r"(?:EDUCATION|ACADEMIC|DEGREES)",
        "projects": r"(?:PROJECTS|KEY\s+PROJECTS|NOTABLE\s+PROJECTS)",
        "certifications": r"(?:CERTIFICATIONS|CERTIFICATES|PROFESSIONAL\s+DEVELOPMENT)"
    }
    
    # Find potential section boundaries
    section_positions = {}
    for section_name, pattern in sections.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            section_positions[section_name] = matches[0].start()
    
    # Sort sections by position
    sorted_sections = sorted(section_positions.items(), key=lambda x: x[1])
    
    # Extract content for each section
    section_content = {}
    for i, (section_name, pos) in enumerate(sorted_sections):
        start = pos
        # End is either the next section or the end of text
        end = sorted_sections[i+1][1] if i < len(sorted_sections) - 1 else len(text)
        section_content[section_name] = text[start:end].strip()
    
    return section_content

def save_sections(sections):
    """Save each section to a markdown file"""
    for section_name, content in sections.items():
        # Format the content as markdown
        if content:
            # Add heading
            markdown_content = f"# {section_name.title()}\n\n{content}"
            
            # Save to file
            file_path = os.path.join(OUTPUT_DIR, f"{section_name}.md")
            with open(file_path, 'w') as f:
                f.write(markdown_content)
            print(f"Saved {section_name} to {file_path}")

def main():
    # Extract text from PDF
    print(f"Extracting text from {RESUME_PATH}")
    resume_text = extract_text_from_pdf(RESUME_PATH)
    
    if not resume_text:
        print("Failed to extract text from PDF")
        sys.exit(1)
    
    # Save full text for reference
    with open(os.path.join(OUTPUT_DIR, "full_text.md"), 'w') as f:
        f.write(f"# Full Resume Text\n\n```\n{resume_text}\n```")
    
    # Identify and extract sections
    print("Parsing resume sections")
    sections = identify_sections(resume_text)
    
    # Save sections to files
    save_sections(sections)
    print("Done!")

if __name__ == "__main__":
    main()