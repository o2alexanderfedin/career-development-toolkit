# Resume Management System

This directory contains a modular, version-controlled resume management system designed using software development principles and GitFlow for solo workflow.

## Directory Structure

- `/versions` - Complete resume versions
  - `AlexanderFedin_2025-01-21.pdf` - Original PDF resume
  - `full_resume.md` - Complete resume in markdown format
  - `full_resume_with_references.md` - Resume with references to component files

- `/sections` - Individual resume components in markdown format
  - `summary_enhanced.md` - Professional summary
  - `skills_structured.md` - Technical skills organized by category
  - `experience_structured.md` - Work history with achievements
  - `education_enhanced.md` - Educational background

- `/reports` - Analysis and recommendations
  - `resume_analysis.md` - Detailed review and enhancement suggestions

- `/customized` - Tailored versions for specific job applications

## Tools

- `pdf_to_markdown.py` - Script for extracting content from PDF resumes
  - Usage: `python pdf_to_markdown.py path/to/resume.pdf`

- `resume_analyzer.py` - Script for analyzing resume content for target roles
  - Usage: `python resume_analyzer.py <role>`
  - Available roles: engineering_manager, technical_director, cto

## Usage Instructions

### Viewing the Resume
The complete resume is available in multiple formats:
- Markdown: `/versions/full_resume.md`
- PDF: `/versions/AlexanderFedin_2025-01-21.pdf`

### Updating Content
1. Edit the relevant section file in the `/sections` directory
2. Run the appropriate script to regenerate the complete resume:
   ```
   python update_resume.py
   ```

### Creating Role-Specific Versions
1. Identify target role and company
2. Run the analyzer for specific recommendations:
   ```
   python resume_analyzer.py engineering_manager
   ```
3. Create a customized version in the `/customized` directory
4. Validate against job requirements

### Adding New Experiences
1. Update `/sections/experience_structured.md` with new role details
2. Add relevant skills to `/sections/skills_structured.md`
3. Regenerate the full resume

## Best Practices

1. Always version each new resume with a date (YYYY-MM-DD)
2. Keep achievements quantifiable and result-focused
3. Customize for each significant application
4. Maintain consistent formatting
5. Follow the TDD principles outlined in `CLAUDE.md`
6. Use GitFlow branches for managing resume updates:
   - `feature/` branches for adding new skills or experiences
   - `bugfix/` branches for correcting errors
   - `release/` branches when preparing for specific applications

## Report Generation
For analysis of your resume against specific job targets:
```
python resume_analyzer.py <role>
```

This will provide targeted recommendations for optimizing your resume for specific positions.