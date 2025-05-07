# Directory Structure Standards

## Core Principles

- **Separation of Concerns**: Organize files by their purpose and target audience
- **Consistent Naming**: Use clear, consistent naming conventions across all directories
- **Logical Grouping**: Group related files together in dedicated directories
- **Progressive Disclosure**: Structure directories to reveal complexity progressively
- **README First**: Include README.md files in each directory explaining its purpose

## Top-Level Organization

- **`/resume`**: All resume-related content
- **`/job_search`**: Job search strategies and materials
- **`/linkedin`**: LinkedIn profile and content
- **`/requirements`**: All requirement specifications
- **`/tests`**: Content validation tools and reports
- **`/.claude`**: AI assistance rules and configuration
- **`/scripts`**: Automation scripts and utilities

## Detailed Structure Standards

### Resume Organization

- **`/resume/versions`**: Complete assembled resumes
- **`/resume/sections`**: Modular resume components
  - **`/common`**: Shared elements (education, certifications)
  - **`/individual_contributor`**: IC-focused versions of sections
  - **`/director`**: Leadership-focused versions of sections
- **`/resume/reports`**: Analysis and recommendations
- **`/resume/customized`**: Role or company-specific variations

### Requirements Organization

- **`/requirements`**: All requirements documentation
  - Store separate files for different requirement types
  - Include README.md explaining purpose of each file
  - Prefix filenames with category (e.g., `job_`, `system_`)

### Job Search Materials

- **`/job_search`**: Job search materials and strategies
  - **`/target_roles`**: Role recommendations and analysis
  - **`/cover_letters`**: Cover letter templates
  - **`/interview_prep`**: Interview preparation materials

### Content Management Rules

1. **Never store files at repository root** except:
   - README.md
   - CHANGELOG.md
   - Other standard top-level documentation

2. **Maintain parallel structures** across different file types:
   - If creating a director-level resume, ensure all components exist
   - Keep naming conventions consistent across parallel files

3. **Link via relative paths** to ensure portability:
   - Use `../` notation for cross-directory references
   - Prefer relative links over absolute paths

4. **Update all dependent files** when moving content:
   - When relocating files, update all references
   - Document structure changes in CHANGELOG.md

## File Conventions

- **Markdown filenames**: Use `snake_case` for general files (e.g., `job_search_requirements.md`)
- **Component names**: Use descriptive names without version numbers in filenames
- **README files**: Include in every directory to explain purpose and contents
- **Structure changes**: Must be documented in CHANGELOG.md under "Changed" section