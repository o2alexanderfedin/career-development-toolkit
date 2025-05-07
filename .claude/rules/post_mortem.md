# Post-Mortem Analysis Framework

## Overview

This framework provides a structured approach to documenting problems encountered, solutions implemented, and lessons learned throughout the development process. By capturing this information systematically, we create a valuable knowledge base for addressing similar issues in the future.

## Post-Mortem Structure

Each post-mortem document should follow this structure:

1. **Problem Statement**
   - Clear, concise description of the issue
   - Generic enough to be recognizable in different contexts
   - Include relevant error messages or symptoms

2. **Context**
   - Environment in which the problem occurred
   - Relevant system state or conditions
   - Related components or dependencies

3. **Investigation Process**
   - Steps taken to understand the problem
   - Diagnostic approaches and tools used
   - Dead ends or false starts (to prevent future investigators from repeating them)

4. **Root Cause**
   - Underlying issue(s) that led to the problem
   - Technical explanation of why it occurred
   - Contributing factors or patterns

5. **Solution Implemented**
   - Detailed description of the fix
   - Code changes or configuration adjustments made
   - Testing and validation approach

6. **Alternative Solutions Considered**
   - Other potential approaches that were not chosen
   - Pros and cons of each alternative
   - Reasons for selecting the implemented solution

7. **Lessons Learned**
   - Key takeaways from the experience
   - Process improvements to prevent similar issues
   - Knowledge gained about the system

8. **Prevention Strategies**
   - How to detect this issue earlier in the future
   - Monitoring or testing approaches
   - Design patterns to avoid or embrace

9. **References**
   - Links to relevant documentation, code, or discussions
   - Similar problems in other contexts
   - Tools or resources that were helpful

## Storage and Organization

Post-mortem documents are stored in:

```
/.claude/post_mortems/
  ├── infrastructure/        # Environment, build, deployment issues
  ├── code/                  # Programming problems and solutions
  ├── process/               # Workflow, methodology challenges
  ├── tools/                 # Issues with tools and utilities
  └── content/               # Content creation and management problems
```

## File Naming Convention

Post-mortem files follow this naming pattern:
`YYYY-MM-DD_brief-problem-description.md`

Example: `2023-05-07_git-flow-release-spaces-issue.md`

## Tagging and Classification

Each post-mortem includes a YAML frontmatter section with tags for easy searching:

```yaml
---
title: Git Flow Release Command Failed with Spaces in Message
date: 2023-05-07
tags: [git, gitflow, release, error, command-line]
severity: medium
resolution_time: 30min
categories: [infrastructure, process]
related_files: [scripts/version.py, .husky/post-flow-release-start]
---
```

## Referencing System

To ensure post-mortems are easily discoverable:

1. **Central Index**
   - A master index file (`.claude/post_mortems/INDEX.md`) categorizes all post-mortems
   - Updated automatically via Git hooks when new post-mortems are added

2. **Cross-Referencing**
   - In code comments: `// See post-mortem: 2023-05-07_git-flow-release-spaces-issue.md`
   - In Git commits: `fix: Resolve release message issue (see PM:2023-05-07)`
   - In documentation: `For more details, see [PM:2023-05-07](/.claude/post_mortems/infrastructure/2023-05-07_git-flow-release-spaces-issue.md)`

3. **Search Integration**
   - Custom script `scripts/search_pm.py` to search post-mortems by keywords, tags, or categories

## Review Process

After creating a post-mortem:

1. Self-review using the checklist in `.claude/templates/post_mortem_review.md`
2. Update the central index
3. Add references in relevant code, commit messages, or documentation
4. Consider adding preventative measures to relevant workflows

## Example Post-Mortem

See [PM:2023-05-07](/.claude/post_mortems/infrastructure/2023-05-07_git-flow-release-spaces-issue.md) for a complete example.

## Integration with Development Workflow

- When encountering a new issue, first check the post-mortem index for similar problems
- After resolving a significant issue, determine if it warrants a post-mortem document:
  - Significant learning opportunity that could benefit future work
  - Complex problem with non-obvious solution
  - Issue that took substantial time to diagnose or fix
  - Problem that might recur in different contexts
- Skip post-mortem creation for routine issues with straightforward solutions
- Reference post-mortems in release notes when relevant
- Periodically review post-mortems to identify patterns or systemic issues

## Automated Post-Mortem Prompts

The system includes Git hooks that prompt for potential post-mortem documentation at key points:

- After completing a release or hotfix
- When resolving complex merge conflicts
- After significant feature implementation
- Following a complex rebase operation
- When fixing critical issues

Each prompt includes an option to skip post-mortem creation when not warranted, ensuring that only meaningful events are documented.