# GitFlow Process Rules

## Branch Structure

- **`main`**: Production-ready code only
- **`develop`**: Integration branch for features
- **`feature/*`**: New features or enhancements
- **`release/*`**: Preparing for a new release
- **`hotfix/*`**: Emergency fixes for production issues
- **`support/*`**: Long-term maintenance branches

## Workflow Rules

### Feature Development
1. Create feature branches from `develop`:
   ```bash
   git flow feature start feature-name
   ```
2. Work on the feature, committing changes regularly
3. When complete, finish the feature:
   ```bash
   git flow feature finish feature-name
   ```
   - If no changes were made, you'll be prompted to cancel or continue
4. This merges back to `develop` and deletes the feature branch

### Releases
1. Create release branch from `develop`:
   ```bash
   git flow release start X.Y.Z
   ```
2. Make only bug fixes, documentation, and release-oriented changes
3. Finish the release:
   ```bash
   git flow release finish X.Y.Z
   ```
   - If no changes were made, you'll be prompted to cancel or continue
4. This merges to both `main` and `develop`, creates a tag, and deletes the release branch

### Hotfixes
1. Create hotfix branch from `main`:
   ```bash
   git flow hotfix start X.Y.Z
   ```
2. Fix the critical issue
3. Finish the hotfix:
   ```bash
   git flow hotfix finish X.Y.Z
   ```
   - If no changes were made, you'll be prompted to cancel or continue
4. This merges to both `main` and `develop`, creates a tag, and deletes the hotfix branch

### Empty Branch Handling
The workflow includes smart detection of branches with no changes:

1. When finishing a branch with no changes:
   - Option to cancel the operation and delete the branch
   - Option to continue anyway (for documentation-only changes)
   
2. Benefits:
   - Prevents empty merge commits that clutter history
   - Saves time by avoiding unnecessary merges
   - Keeps repository history clean and meaningful

## Commit Guidelines

- Use descriptive commit messages with a clear subject line
- Format: `[type]: Brief description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Example: `feat: Add LinkedIn post template generator`
- Include issue/ticket references when applicable
- Keep commits focused on a single concern

## Solo Workflow Process

1. Merge directly from feature branch to `develop` when complete
   ```bash
   git flow feature finish feature-name
   ```
2. Ensure all tests pass and code meets standards before finishing
3. Keep commits clean and focused 
4. Use meaningful commit messages with proper types
5. For larger changes, consider self-review before finishing

## Tagging

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Tag all production releases on the `main` branch
- Include release notes in tag annotations
- Format: `vX.Y.Z` (e.g., `v1.0.0`)

## Project-Specific Conventions

- **Resume Updates**: Use `feat(resume): description` format
- **LinkedIn Content**: Use `content(linkedin): description` format
- **Documentation**: Use `docs: description` format
- **Tool Development**: Use `tool: description` format

## Example Workflows

### Adding a New Resume Section
```bash
git flow feature start resume-skills-update
# Work on files
git add resume/sections/skills_enhanced.md
git commit -m "feat(resume): Add cloud engineering skills section"
git flow feature finish resume-skills-update
```

### Preparing for Job Application Release
```bash
git flow release start v1.2.0
# Final polishing
git commit -m "docs: Update README with new skills section"
git flow release finish v1.2.0
```

### Emergency Fix for LinkedIn Post
```bash
git flow hotfix start v1.2.1
# Fix the issue
git commit -m "fix(linkedin): Correct metrics in leadership post"
git flow hotfix finish v1.2.1
```