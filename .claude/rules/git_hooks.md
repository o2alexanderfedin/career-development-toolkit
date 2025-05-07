# Git Hooks & Automated Reminders

## Overview

This project uses Git hooks to provide contextual reminders about GitFlow operations at key points in the development workflow. These hooks help ensure consistent use of GitFlow practices by providing just-in-time guidance.

## Implemented Hooks

### post-checkout
- Triggered after checking out a branch
- Provides context-specific reminders based on the branch type
- Suggests next steps appropriate for the current branch
- Example: When checking out a feature branch, reminds about how to finish the feature

### post-commit
- Triggered after making a commit
- Reminds about next steps after committing changes
- Only shows reminders for feature/release/hotfix branches with multiple commits
- Example: After committing to a feature branch, suggests pushing or finishing the feature

### pre-push
- Triggered before pushing changes to remote
- Provides warnings when pushing directly to protected branches (main)
- Reminds about appropriate GitFlow operations after pushing
- Example: When pushing a release branch, reminds about the release finish process

## Hook Installation

The hooks are managed using Husky, which is set up in package.json:

1. Install dependencies: `npm install`
2. Husky will automatically install the hooks via the prepare script

## Customizing Reminders

To modify the reminders:

1. Edit the appropriate hook file in the `.husky/` directory
2. Ensure executable permissions: `chmod +x .husky/<hook-name>`
3. Commit the changes

## Convenience Scripts

The package.json includes convenience scripts for common GitFlow operations:

```bash
# Start a new feature
npm run gitflow:feature:start feature-name

# Finish a feature
npm run gitflow:feature:finish feature-name

# Start a new release
npm run gitflow:release:start version

# Finish a release
npm run gitflow:release:finish version

# Start a hotfix
npm run gitflow:hotfix:start version

# Finish a hotfix
npm run gitflow:hotfix:finish version
```

## Best Practices

1. **Pay attention to reminders**: The hook messages are designed to guide you through the GitFlow process
2. **Use the suggested commands**: Copy-paste the suggested commands when appropriate
3. **Follow branch naming conventions**: Keep feature/release/hotfix names consistent
4. **Don't ignore warnings**: Especially warnings about pushing directly to protected branches

## Troubleshooting

If hooks aren't executing:
1. Check permissions: Ensure hooks are executable (`chmod +x .husky/*`)
2. Verify Husky installation: Reinstall with `npm run prepare`
3. Check Git version: Git >= 2.9.0 is required for these hooks