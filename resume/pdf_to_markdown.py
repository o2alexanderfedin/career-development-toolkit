#!/usr/bin/env python3
"""
PDF to Markdown Converter
Extracts text from PDF and converts it to markdown format
Uses PyMuPDF (fitz) for PDF processing
"""

import sys
import re
import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page in doc:
            text += page.get_text()
        
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def clean_text(text):
    """Clean and format the extracted text"""
    # Replace multiple newlines with double newline for paragraphs
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Normalize spacing
    text = re.sub(r' +', ' ', text)
    
    return text

def detect_sections(text):
    """Attempt to detect resume sections based on common patterns"""
    # Common section headers in resumes
    section_patterns = [
        (r'(?i)(?:professional\s+)?summary|profile', 'summary'),
        (r'(?i)skills|technical\s+skills|expertise|competencies', 'skills'),
        (r'(?i)experience|work\s+experience|employment|work\s+history', 'experience'),
        (r'(?i)education|academic|qualifications', 'education'),
        (r'(?i)projects|key\s+projects|notable\s+projects', 'projects'),
        (r'(?i)certifications|certificates|professional\s+development', 'certifications'),
    ]
    
    # Find potential section boundaries
    sections = {}
    section_positions = []
    
    for pattern, section_name in section_patterns:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            # Use the first match as the section start
            pos = matches[0].start()
            sections[section_name] = pos
            section_positions.append((pos, section_name))
    
    # Sort sections by position
    section_positions.sort()
    
    # Extract section content
    section_content = {}
    for i, (pos, section_name) in enumerate(section_positions):
        start = pos
        # End is either the next section or the end of text
        if i < len(section_positions) - 1:
            end = section_positions[i+1][0]
        else:
            end = len(text)
        
        content = text[start:end].strip()
        # Remove the section header from the content
        header_match = re.search(r'^.*?\n', content)
        if header_match:
            content = content[header_match.end():].strip()
        
        section_content[section_name] = content
    
    return section_content

def format_as_markdown(section_name, content):
    """Format section content as markdown"""
    # Add section heading
    md = f"# {section_name.title()}\n\n"
    
    # Process content based on section type
    if section_name == "skills":
        # Try to identify skill categories
        categories = re.findall(r'([A-Z][A-Za-z ]+)(?::|•|\n)', content)
        if categories:
            for category in categories:
                md += f"## {category.strip()}\n\n"
                # Find skills associated with this category
                pattern = f"{re.escape(category)}(?::|•|\n)(.*?)(?=(?:[A-Z][A-Za-z ]+:|$))"
                matches = re.search(pattern, content, re.DOTALL)
                if matches:
                    skills_text = matches.group(1).strip()
                    # Convert to bullet points
                    skills = re.split(r'[,•\n]', skills_text)
                    for skill in skills:
                        skill = skill.strip()
                        if skill:
                            md += f"- {skill}\n"
                    md += "\n"
        else:
            # Simple bullet list for skills
            skills = re.split(r'[,•\n]', content)
            for skill in skills:
                skill = skill.strip()
                if skill:
                    md += f"- {skill}\n"
    
    elif section_name == "experience":
        # Try to identify experience entries
        companies = re.findall(r'([A-Z][A-Za-z0-9 .]+)(?:\s+[-–|]\s+|\n)([A-Za-z0-9 ]+)?(?:\s+[-–|]\s+|\n)?([A-Za-z0-9 ]+)?(?:\s+[-–|]\s+|\n)?(\d{4})?(?:\s*[-–]\s*)?(\d{4}|Present)?', content)
        if companies:
            for company_match in companies:
                company = company_match[0].strip()
                title = company_match[1].strip() if len(company_match) > 1 else ""
                location = company_match[2].strip() if len(company_match) > 2 else ""
                start_date = company_match[3].strip() if len(company_match) > 3 else ""
                end_date = company_match[4].strip() if len(company_match) > 4 else ""
                
                md += f"## {company}\n\n"
                if title:
                    md += f"**{title}**"
                    if start_date or end_date:
                        md += f" | {start_date} - {end_date}"
                    md += "\n\n"
                
                if location:
                    md += f"*{location}*\n\n"
                
                # Find bullet points for this position
                company_section = content[content.find(company):]
                next_company = re.search(r'[A-Z][A-Za-z0-9 .]+(?:\s+[-–|]\s+|\n)[A-Za-z0-9 ]+', company_section[len(company):])
                if next_company:
                    company_section = company_section[:next_company.start() + len(company)]
                
                # Extract bullet points (lines starting with • or -)
                bullets = re.findall(r'[•-]\s*(.*?)(?:\n|$)', company_section)
                if bullets:
                    for bullet in bullets:
                        if bullet.strip():
                            md += f"- {bullet.strip()}\n"
                    md += "\n"
        else:
            # Fallback: just add the content as is
            md += content + "\n\n"
    
    elif section_name == "education":
        # Format education entries
        institutions = re.findall(r'([A-Z][A-Za-z0-9 .]+)(?:\s+[-–|]\s+|\n)([A-Za-z0-9 ,]+)?(?:\s+[-–|]\s+|\n)?(\d{4})?(?:\s*[-–]\s*)?(\d{4}|Present)?', content)
        if institutions:
            for inst_match in institutions:
                institution = inst_match[0].strip()
                degree = inst_match[1].strip() if len(inst_match) > 1 else ""
                year = inst_match[2].strip() if len(inst_match) > 2 else ""
                
                md += f"## {institution}\n\n"
                if degree:
                    md += f"**{degree}**"
                    if year:
                        md += f" | {year}"
                    md += "\n\n"
        else:
            # Fallback: just add the content as is
            md += content + "\n\n"
    
    else:
        # Default formatting: preserve paragraphs
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                # Check if it's a bullet point
                if paragraph.startswith('•') or paragraph.startswith('-'):
                    lines = paragraph.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line:
                            if line.startswith('•'):
                                line = '- ' + line[1:].strip()
                            elif not line.startswith('-'):
                                line = '- ' + line
                            md += line + '\n'
                else:
                    md += paragraph + '\n\n'
    
    return md

def save_to_markdown_files(sections, output_dir):
    """Save each section to a separate markdown file"""
    for section_name, content in sections.items():
        md_content = format_as_markdown(section_name, content)
        
        file_path = os.path.join(output_dir, f"{section_name}.md")
        with open(file_path, 'w') as f:
            f.write(md_content)
        print(f"Saved {section_name} to {file_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python pdf_to_markdown.py <pdf_file>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found")
        sys.exit(1)
    
    # Extract text from PDF
    print(f"Extracting text from {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("Failed to extract text from PDF")
        sys.exit(1)
    
    # Clean text
    text = clean_text(text)
    
    # Extract sections
    print("Identifying resume sections")
    sections = detect_sections(text)
    
    if not sections:
        print("No sections detected, saving entire text as markdown")
        sections = {"full_resume": text}
    
    # Determine output directory
    output_dir = os.path.dirname(pdf_path)
    if output_dir.endswith("versions"):
        output_dir = os.path.join(os.path.dirname(output_dir), "sections")
    
    # Save sections to markdown files
    print(f"Saving sections to {output_dir}")
    save_to_markdown_files(sections, output_dir)
    
    print("Conversion complete!")

if __name__ == "__main__":
    main()