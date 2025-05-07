# Solo GitFlow for Resume Management

## Overview

This project uses a modified GitFlow workflow optimized for solo development of resume and job application materials. It maintains the benefits of structured version control while eliminating team-oriented processes like pull requests and code reviews.

## Branch Structure

- **`main`**: Production-ready resume versions
- **`develop`**: Integration branch for work-in-progress resume improvements
- **`feature/*`**: Adding new content (skills, experiences, achievements)
- **`bugfix/*`**: Fixing errors in existing content
- **`release/*`**: Preparing resume for specific job applications
- **`hotfix/*`**: Emergency fixes for sent applications
- **`support/*`**: Long-term maintenance of specific resume versions

## Workflow Rules

### Feature Development (Adding Content)
Use for: Adding new skills, experiences, roles, or sections

```bash
# Start feature
git flow feature start add-cloud-skills

# Work and commit changes
git add resume/sections/skills_structured.md
git commit -m "feat: Add cloud engineering skills section"

# Finish feature (merges to develop)
git flow feature finish add-cloud-skills
```

### Bugfix (Correcting Content)
Use for: Correcting errors, typos, or inaccuracies

```bash
# Start bugfix
git flow bugfix start fix-job-dates

# Work and commit changes
git add resume/sections/experience_structured.md
git commit -m "fix: Correct employment dates for Tesla role"

# Finish bugfix
git flow bugfix finish fix-job-dates
```

### Releases (Job Applications)
Use for: Finalizing resume for specific job application

```bash
# Start release when ready to apply
git flow release start google-pm-role

# Make final adjustments for this application
git add resume/customized/google_product_manager.md
git commit -m "feat: Customize summary for Google PM role"

# Finish release (merges to both develop and main)
git flow release finish google-pm-role
```

### Hotfixes (Post-Submission Corrections)
Use for: Critical fixes to resumes already sent out

```bash
# Start hotfix from main
git flow hotfix start 1.2.1

# Fix the critical issue
git add resume/versions/full_resume.md
git commit -m "fix: Correct email address in contact info"

# Finish hotfix
git flow hotfix finish 1.2.1
```

## Commit Guidelines

- Use descriptive commit messages with prefixes: 
  - `feat:` - New content or significant enhancement
  - `fix:` - Corrections to existing content
  - `docs:` - Documentation changes
  - `style:` - Formatting changes
  - `refactor:` - Reorganizing content without changing substance

## Version Tagging

- Use semantic versioning for resume versions: MAJOR.MINOR.PATCH
- MAJOR: Complete resume redesign
- MINOR: Adding significant new content (new jobs, skills)
- PATCH: Small fixes and improvements

## Workflow Examples for Resume Management

### Updating Skills for Technical Roles
```bash
git flow feature start update-tech-skills
# Edit skills section
git add resume/sections/skills_structured.md
git commit -m "feat: Add AI and ML engineering skills"
git flow feature finish update-tech-skills
```

### Preparing for Specific Job Application
```bash
git flow release start amazon-sde-role
# Customize resume sections
git add resume/customized/amazon_sde.md
git commit -m "feat: Highlight AWS experience for Amazon role"
git flow release finish amazon-sde-role
```

### Recording Application Details
```bash
git tag -a "amazon-sde-may2023" -m "Resume version sent to Amazon for SDE role"
```

This customized workflow allows for structured, version-controlled resume development while keeping the process streamlined for solo use.