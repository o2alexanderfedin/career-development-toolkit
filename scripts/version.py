#!/usr/bin/env python3
"""
Versioning tool for career development materials

Provides functionality to:
- Get current version
- Calculate next version based on changes
- Bump version (major, minor, patch)
- Generate appropriate GitFlow release branch names and tags
"""

import os
import sys
import re
import subprocess
import argparse
from datetime import datetime
from typing import Tuple, List, Optional

# File paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(ROOT_DIR, 'VERSION')
CHANGELOG_FILE = os.path.join(ROOT_DIR, 'CHANGELOG.md')


def get_current_version() -> str:
    """Get the current version from the VERSION file"""
    if not os.path.exists(VERSION_FILE):
        return "0.1.0"  # Default initial version
    
    with open(VERSION_FILE, 'r') as f:
        version = f.read().strip()
        
    return version


def parse_version(version: str) -> Tuple[int, int, int, str, str]:
    """Parse a version string into its components"""
    # Match SemVer with optional pre-release and metadata
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$', version)
    
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))
    prerelease = match.group(4) or ""
    metadata = match.group(5) or ""
    
    return major, minor, patch, prerelease, metadata


def bump_version(current_version: str, part: str, prerelease: str = None, metadata: str = None) -> str:
    """Increment the specified part of the version number"""
    major, minor, patch, _, _ = parse_version(current_version)
    
    if part == 'major':
        major += 1
        minor = 0
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    elif part == 'patch':
        patch += 1
    else:
        raise ValueError(f"Invalid version part: {part}")
    
    # Construct the new version
    new_version = f"{major}.{minor}.{patch}"
    
    # Add pre-release if specified
    if prerelease:
        new_version += f"-{prerelease}"
    
    # Add metadata if specified
    if metadata:
        new_version += f"+{metadata}"
    
    return new_version


def save_version(version: str) -> None:
    """Save version to the VERSION file"""
    with open(VERSION_FILE, 'w') as f:
        f.write(version)


def update_changelog(version: str) -> None:
    """Update the CHANGELOG.md file with a new version section"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # If CHANGELOG.md doesn't exist, create it
    if not os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, 'w') as f:
            f.write(f"""# Changelog

All notable changes to career materials will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [{version}] - {today}
### Added
- Initial version

""")
        return
    
    # Read existing content
    with open(CHANGELOG_FILE, 'r') as f:
        content = f.read()
    
    # Check if Unreleased section exists
    unreleased_match = re.search(r'## \[Unreleased\]\n(.*?)(?=\n## \[|$)', content, re.DOTALL)
    if not unreleased_match:
        # Add unreleased section if it doesn't exist
        new_content = re.sub(r'# Changelog.*?\n\n', f'# Changelog\n\n## [Unreleased]\n\n## [{version}] - {today}\n', content, flags=re.DOTALL)
    else:
        # Insert new version section after unreleased
        unreleased_content = unreleased_match.group(1).strip()
        if unreleased_content:
            # If there are unreleased changes, move them to the new version
            new_version_content = f"## [{version}] - {today}\n{unreleased_content}\n\n"
            new_content = content.replace(unreleased_match.group(0), f"## [Unreleased]\n\n{new_version_content}")
        else:
            # If no unreleased changes, just add an empty new version
            new_content = content.replace(unreleased_match.group(0), f"## [Unreleased]\n\n## [{version}] - {today}\n### Added\n- Version bump\n\n")
    
    # Write updated content
    with open(CHANGELOG_FILE, 'w') as f:
        f.write(new_content)


def get_changed_files(since: str = "develop") -> List[str]:
    """Get list of files changed since the given reference"""
    try:
        result = subprocess.run(["git", "diff", "--name-only", since], 
                               capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        print(f"Error: Failed to get changed files since {since}", file=sys.stderr)
        return []


def guess_version_bump(current_version: str, changed_files: List[str]) -> str:
    """Guess the appropriate version bump based on changed files"""
    # Parse patterns that indicate the significance of changes
    major_patterns = [
        r'career_change\.md',
        r'major_redesign\.md'
    ]
    
    minor_patterns = [
        r'resume/sections/experience_structured\.md',  # New job or role
        r'resume/sections/skills_structured\.md',      # New skills
        r'linkedin/posts/final/.*\.md'                 # New LinkedIn content
    ]
    
    # Check for major changes
    for pattern in major_patterns:
        if any(re.search(pattern, file) for file in changed_files):
            return bump_version(current_version, 'major')
    
    # Check for minor changes
    for pattern in minor_patterns:
        if any(re.search(pattern, file) for file in changed_files):
            return bump_version(current_version, 'minor')
    
    # Default to patch for other changes
    return bump_version(current_version, 'patch')


def get_release_branch_name(version: str) -> str:
    """Generate the GitFlow release branch name for a version"""
    # Strip any metadata
    version_core = version.split('+')[0]
    return f"release/v{version_core}"


def get_release_tag(version: str) -> str:
    """Generate the git tag for a release version"""
    return f"v{version}"


def start_release(version: str) -> None:
    """Start a GitFlow release with the given version"""
    branch_name = get_release_branch_name(version).replace('release/', '')
    
    try:
        subprocess.run(["git", "flow", "release", "start", branch_name], check=True)
        print(f"Started release branch: {branch_name}")
        
        # Update VERSION and CHANGELOG
        save_version(version)
        update_changelog(version)
        
        print(f"Updated VERSION to {version}")
        print(f"Updated CHANGELOG.md")
        
        # Stage the changes
        subprocess.run(["git", "add", "VERSION", "CHANGELOG.md"], check=True)
        subprocess.run(["git", "commit", "-m", f"chore: Bump version to {version}"], check=True)
        
        print(f"Committed version bump to {version}")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to start release: {e}", file=sys.stderr)
        sys.exit(1)


def finish_release(version: str) -> None:
    """Finish a GitFlow release with the given version"""
    branch_name = get_release_branch_name(version).replace('release/', '')
    tag = get_release_tag(version)
    
    try:
        # Ensure we're on the correct branch
        current_branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], 
                                       capture_output=True, text=True, check=True).stdout.strip()
        expected_branch = f"release/{branch_name}"
        
        if current_branch != expected_branch:
            print(f"Error: Not on the expected release branch. Expected {expected_branch}, got {current_branch}", file=sys.stderr)
            sys.exit(1)
        
        # Finish the release
        subprocess.run(["git", "flow", "release", "finish", "-m", f"Release {version}", branch_name], check=True)
        print(f"Finished release: {version}")
        print(f"Created tag: {tag}")
        
        # Push branches and tags
        subprocess.run(["git", "push", "origin", "develop", "main", tag], check=True)
        print(f"Pushed develop, main, and {tag} to remote")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to finish release: {e}", file=sys.stderr)
        sys.exit(1)


def tag_application(version: str, company: str, role: str) -> str:
    """Create a tag for a specific job application"""
    tag = f"v{version}-{company}-{role}"
    tag = tag.lower().replace(' ', '-')
    
    try:
        message = f"Application materials for {company} {role} position"
        subprocess.run(["git", "tag", "-a", tag, "-m", message], check=True)
        subprocess.run(["git", "push", "origin", tag], check=True)
        print(f"Created and pushed application tag: {tag}")
        return tag
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to create application tag: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(description="Versioning tool for career development materials")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # get command
    get_parser = subparsers.add_parser("get", help="Get the current version")
    
    # next command
    next_parser = subparsers.add_parser("next", help="Calculate the next version")
    next_parser.add_argument("--part", choices=["major", "minor", "patch"], 
                            help="Explicitly specify which part to bump")
    
    # bump command
    bump_parser = subparsers.add_parser("bump", help="Bump version and update files")
    bump_parser.add_argument("part", choices=["major", "minor", "patch"], 
                            help="Which part of the version to bump")
    bump_parser.add_argument("--prerelease", help="Add pre-release identifier")
    bump_parser.add_argument("--metadata", help="Add build metadata")
    
    # release commands
    release_parser = subparsers.add_parser("release", help="Manage releases")
    release_subparsers = release_parser.add_subparsers(dest="release_command", help="Release command to run")
    
    start_parser = release_subparsers.add_parser("start", help="Start a new release")
    start_parser.add_argument("--part", choices=["major", "minor", "patch"], 
                             help="Which part of the version to bump")
    
    finish_parser = release_subparsers.add_parser("finish", help="Finish an existing release")
    
    # application tagging
    app_parser = subparsers.add_parser("application", help="Tag an application")
    app_parser.add_argument("company", help="Company name")
    app_parser.add_argument("role", help="Job role or title")
    
    args = parser.parse_args()
    
    # Get current version
    current_version = get_current_version()
    
    if args.command == "get":
        print(current_version)
    
    elif args.command == "next":
        if args.part:
            next_version = bump_version(current_version, args.part)
        else:
            changed_files = get_changed_files()
            next_version = guess_version_bump(current_version, changed_files)
        print(next_version)
    
    elif args.command == "bump":
        new_version = bump_version(current_version, args.part, args.prerelease, args.metadata)
        save_version(new_version)
        update_changelog(new_version)
        print(f"Bumped version from {current_version} to {new_version}")
    
    elif args.command == "release":
        if args.release_command == "start":
            if args.part:
                new_version = bump_version(current_version, args.part)
            else:
                changed_files = get_changed_files()
                new_version = guess_version_bump(current_version, changed_files)
            start_release(new_version)
        
        elif args.release_command == "finish":
            finish_release(current_version)
        
        else:
            release_parser.print_help()
    
    elif args.command == "application":
        tag_application(current_version, args.company, args.role)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()