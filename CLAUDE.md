# Working Rules for Claude

## LinkedIn Post Enhancement
- Save all versions of post text to files for comparison
- Review from multiple perspectives (hiring manager, recruiter, general audience)
- Include specific metrics with before/after values
- Balance technical credibility with accessibility
- Use concrete timeframes and measures

## Format Guidelines
- Use bullet points and emojis for readability
- Structure content into clear sections
- Keep statements concise and impactful
- Include specific numerical improvements
- Add context to metrics when possible

## Workflow
- Save drafts to files for review
- Create separate files for different aspects (reviews, recommendations)
- Use Task tool for complex analysis
- Use Edit tool for targeted modifications
- Review final content from multiple perspectives

## Position/Job Search
- Focus on senior engineering leadership roles
- Emphasize process improvement capabilities
- Highlight AI integration experience
- Showcase measurable team performance improvements
- Target roles with organizational transformation opportunities

## TDD Principles for Content Development
- Define expected outcomes before creating content (equivalent to writing tests first)
- Create small, focused content chunks and validate each before proceeding
- Test content against multiple perspectives (hiring manager, recruiter, peer) before finalizing
- Refactor content after validation without changing its core meaning
- When identifying issues, create a test case first that would catch similar issues
- Apply red-green-refactor cycle: identify problems, fix them, then improve quality
- Maintain a test suite of criteria that all content must satisfy

## Documentation of Patterns and Best Practices
- Document discovered best practices in dedicated files under `.claude/rules/`
- Each domain (resume, LinkedIn, job search, etc.) should have its own best practices file
- Update rules files whenever new patterns are discovered or proven effective
- Reference these rules files in relevant commands and workflows
- Review and refine rules periodically based on outcomes
- Format rules files with clear categories, bullet points, and examples