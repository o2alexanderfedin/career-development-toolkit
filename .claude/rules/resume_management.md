# Resume Management Best Practices

## Document Organization

- **Modularity**: Structure resume content into discrete, maintainable modules (summary, skills, experience, education)
- **Single Source of Truth**: Maintain each section in a dedicated file and reference these in the complete resume
- **Version Control**: Track changes to resume components individually for better change management
- **Linking Strategy**: Use relative paths when linking between documents to maintain portability

## Content Enhancement

- **Quantification**: Always include metrics when describing achievements (%, time saved, improvement ratios)
- **Technology Tagging**: Tag each role with relevant technologies to improve keyword matching
- **Hierarchy**: Organize skills into logical categories to improve readability and ATS optimization
- **Recency Focus**: Place most recent and relevant experiences first, with more detail for recent roles

## Technical Implementation

- **Markdown Format**: Use markdown for ease of editing, conversion, and version control
- **Consistent Formatting**: Use consistent headers, bullet styles, and emphasis throughout
- **File Naming**: Use descriptive, consistent file names with version indicators when appropriate
- **Relative Paths**: Always use relative paths in references between files for portability

## Workflow Patterns

- **TDD for Content**: Define expected outcomes before creating content (e.g., target role requirements)
- **Incremental Updates**: Make small, focused changes to individual sections rather than complete rewrites
- **Multi-format Output**: Generate multiple formats (PDF, Word, text) from a single markdown source
- **Analysis-Driven Editing**: Analyze resume against target job requirements before making changes

## Directory Structure Standards

- **/versions**: Complete assembled resumes in various formats
- **/sections**: Individual component files
- **/reports**: Analysis and recommendations
- **/customized**: Role or company-specific variations
- **/.claude**: AI assistance rules and learned patterns