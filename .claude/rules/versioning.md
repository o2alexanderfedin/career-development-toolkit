# Versioning Policy

## Semantic Versioning for Career Materials

This project follows semantic versioning (SemVer) principles adapted for career materials. Version numbers follow the format: `MAJOR.MINOR.PATCH`.

### Version Components

- **MAJOR**: Significant career milestones or complete resume redesigns
  - Increment when: 
    - Changing careers or industries
    - Complete portfolio/resume redesign
    - Major professional advancement (e.g., senior → executive)

- **MINOR**: New experiences, skills, or significant enhancements
  - Increment when:
    - Adding a new job position
    - Adding significant new skills or certifications
    - Creating new types of content (e.g., cover letter templates)
    - Making substantial improvements to existing materials

- **PATCH**: Corrections, refinements, and small updates
  - Increment when:
    - Fixing typos or errors
    - Refining language in existing entries
    - Making minor formatting improvements
    - Small updates to existing content

### Special Versions

- **Pre-release**: For content being prepared but not ready for applications
  - Format: `1.2.0-alpha.1`, `1.2.0-beta.1`
  - Use for early drafts of new content

- **Application-specific**: For tracking materials sent to specific companies
  - Format: `1.2.0+google`, `1.2.0+amazon`
  - Use build metadata to track company-specific variations

## Release Branches and Tags

### Branch Naming

- Release branches follow the format: `release/vX.Y.Z`
  - Example: `release/v1.2.0`

### Tag Naming

- Release tags follow the format: `vX.Y.Z`
  - Example: `v1.2.0`

- Application-specific tags may include company information:
  - Example: `v1.2.0-amazon-sde`

## Version Files

The repository maintains version information in:

1. `/VERSION` - Contains the current version number
2. `/CHANGELOG.md` - Documents changes in each version

## Automated Tools

Use the provided scripts to manage versions:

- `bump-version.sh [major|minor|patch]` - Increment version number
- `get-next-version.sh` - Calculate the next version based on changes
- `start-release.sh` - Create a properly named release branch

## Practical Examples

1. **Initial Resume Setup**
   - Version: `v1.0.0`

2. **Adding a New Job Position**
   - Previous: `v1.0.0` → New: `v1.1.0`

3. **Fixing Typos**
   - Previous: `v1.1.0` → New: `v1.1.1`

4. **Career Change**
   - Previous: `v1.1.1` → New: `v2.0.0`

5. **Company-Specific Application**
   - Tag: `v1.1.1-microsoft-pm`

## Validation

Before finalizing a release, ensure:

1. The version increment follows these guidelines
2. `VERSION` file is updated
3. `CHANGELOG.md` documents all relevant changes
4. Release tag matches the version number