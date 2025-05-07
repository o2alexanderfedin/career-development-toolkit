# Career Development Toolkit

A structured approach to managing professional content using software development principles.

## Overview

This repository contains a modular, version-controlled system for managing various aspects of professional development, particularly focused on job search and career advancement. It applies software engineering best practices to personal branding materials.

## Repository Structure

- **`/linkedin`** - LinkedIn content management
  - `/posts` - LinkedIn posts in various stages (drafts, final, archive)
  - `/profile` - LinkedIn profile content
  - `/engagement` - Templates for engagement

- **`/resume`** - Resume management system
  - `/versions` - Complete resume versions ([full_resume.md](/resume/versions/full_resume.md))
  - `/sections` - Modular resume components
    - [Professional Summary](/resume/sections/summary_enhanced.md)
    - [Technical Skills](/resume/sections/skills_structured.md) 
    - [Professional Experience](/resume/sections/experience_structured.md)
    - [Education & Certifications](/resume/sections/certifications.md)
  - `/reports` - Analysis and recommendations
    - [Job Position Analysis](/resume/reports/job_position_analysis.md) - Recommended roles
    - [Resume Analysis](/resume/reports/resume_analysis.md) - Enhancement recommendations
  - `/customized` - Role-specific variations

- **`/job_search`** - Job search materials
  - Target roles and companies
  - Cover letter templates
  - Interview preparation

- **`/tests`** - Content validation
  - Testing criteria
  - Reviewer personas
  - Test reports

- **`/.claude`** - AI assistance
  - `/rules` - Best practices and patterns

## Key Features

- **Modular Content**: Break down content into maintainable, reusable components
- **Version Control**: Track changes to professional materials over time
- **Test-Driven Development**: Apply TDD principles to content creation
- **Automation**: Scripts for content analysis and generation
- **Multi-format Output**: Generate various formats from a single source

## Getting Started

1. Clone this repository
2. Navigate to the relevant section for your needs
3. Follow the README in each directory for specific instructions

## Key Reports & Resources

- **Career Strategy**
  - [Job Position Analysis](/resume/reports/job_position_analysis.md) - Recommended roles based on experience
  - [Resume Analysis](/resume/reports/resume_analysis.md) - Resume enhancement recommendations
  - [LinkedIn Post Review](/tests/reports/engineering_leader_post_review.md) - LinkedIn content evaluation

- **Complete Documents**
  - [Full Resume](/resume/versions/full_resume.md) - Current complete resume

## Tools

- Python scripts for PDF parsing and resume analysis
- Markdown files for content storage
- GitHub for version control

## Best Practices

Detailed best practices are documented in `.claude/rules/` directory, including:
- [Resume Management](/.claude/rules/resume_management.md) - Guidelines for resume content and structure
- [GitFlow Process](/.claude/rules/gitflow.md) - Version control workflow
- [Solo GitFlow](/.claude/rules/solo_gitflow.md) - GitFlow adapted for individual work
- [Post-Mortem Analysis](/.claude/rules/post_mortem.md) - System for documenting problems and solutions
- [Versioning](/.claude/rules/versioning.md) - Semantic versioning for career materials

## License

Personal use only - not licensed for redistribution.