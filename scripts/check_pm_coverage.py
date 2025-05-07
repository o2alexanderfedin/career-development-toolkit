#!/usr/bin/env python3
"""
Post-Mortem Coverage Checker

Analyzes commit history to identify significant events that might warrant
post-mortem documentation but don't have one yet.
"""

import os
import sys
import re
import subprocess
import datetime
from typing import List, Dict, Tuple, Optional

# Configuration
PM_ROOT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".claude", "post_mortems")
DAYS_TO_CHECK = 30  # How far back to look in the commit history

def get_recent_significant_commits() -> List[Dict]:
    """Get commits from the last N days that might indicate significant issues"""
    since_date = (datetime.datetime.now() - datetime.timedelta(days=DAYS_TO_CHECK)).strftime("%Y-%m-%d")
    
    try:
        # Get commits with keywords indicating significant issues
        cmd = [
            "git", "log", f"--since={since_date}", "--format=%h|%ad|%an|%s", "--date=short",
            "--grep=fix\\|hotfix\\|emergency\\|critical\\|urgent\\|workaround\\|resolve"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
                
            parts = line.split('|', 3)
            if len(parts) < 4:
                continue
                
            hash_id, date, author, subject = parts
            commits.append({
                'hash': hash_id,
                'date': date,
                'author': author,
                'subject': subject,
                'severity': estimate_severity(subject)
            })
        
        return commits
    except subprocess.CalledProcessError as e:
        print(f"Error getting commits: {e}", file=sys.stderr)
        return []

def estimate_severity(commit_subject: str) -> str:
    """Estimate the severity of an issue based on commit message keywords"""
    subject_lower = commit_subject.lower()
    
    if any(term in subject_lower for term in ['critical', 'emergency', 'security', 'vulnerability', 'data loss', 'crash']):
        return 'high'
    elif any(term in subject_lower for term in ['important', 'major', 'significant', 'broken']):
        return 'medium'
    else:
        return 'low'

def get_existing_post_mortems() -> List[Tuple[str, str]]:
    """Get list of existing post-mortem documents with their date and title"""
    post_mortems = []
    
    for category in ['infrastructure', 'code', 'process', 'tools', 'content']:
        category_dir = os.path.join(PM_ROOT_DIR, category)
        if not os.path.exists(category_dir):
            continue
            
        for filename in os.listdir(category_dir):
            if not filename.endswith('.md') or filename == 'README.md':
                continue
                
            match = re.match(r'(\d{4}-\d{2}-\d{2})_(.*?)\.md', filename)
            if match:
                date, title = match.groups()
                title = title.replace('-', ' ').replace('_', ' ')
                post_mortems.append((date, title))
    
    return post_mortems

def check_post_mortem_coverage() -> List[Dict]:
    """Check if significant commits have corresponding post-mortem documents"""
    commits = get_recent_significant_commits()
    post_mortems = get_existing_post_mortems()
    
    # Convert post-mortem dates to datetime for comparison
    pm_dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date, _ in post_mortems]
    
    # Get unique keywords from post-mortem titles
    pm_keywords = set()
    for _, title in post_mortems:
        keywords = re.findall(r'\b[a-z]{4,}\b', title.lower())
        pm_keywords.update(keywords)
    
    needs_documentation = []
    
    for commit in commits:
        commit_date = datetime.datetime.strptime(commit['date'], '%Y-%m-%d')
        
        # Check if there's a post-mortem within 3 days of the commit
        has_date_match = any(abs((pm_date - commit_date).days) <= 3 for pm_date in pm_dates)
        
        # Check if commit subject contains keywords from existing post-mortems
        commit_keywords = set(re.findall(r'\b[a-z]{4,}\b', commit['subject'].lower()))
        keyword_matches = commit_keywords.intersection(pm_keywords)
        
        # If neither date nor keyword match, this might need documentation
        if not has_date_match and len(keyword_matches) < 2:
            # Don't suggest documentation for minor fixes
            if commit['severity'] != 'low' or 'fix' not in commit['subject'].lower():
                needs_documentation.append(commit)
    
    return needs_documentation

def main():
    """Main function"""
    print("Checking for significant events that might need post-mortem documentation...\n")
    
    needs_documentation = check_post_mortem_coverage()
    
    if not needs_documentation:
        print("✅ All significant events appear to be documented!")
        return
    
    print(f"Found {len(needs_documentation)} events that might need documentation:\n")
    
    for i, commit in enumerate(needs_documentation, 1):
        severity_marker = {
            'high': '🔴',
            'medium': '🟠',
            'low': '🟡'
        }.get(commit['severity'], '⚪')
        
        print(f"{severity_marker} {i}. [{commit['date']}] {commit['subject']} ({commit['hash']})")
        
        # Suggest post-mortem filename
        words = re.findall(r'\b[a-z]{3,}\b', commit['subject'].lower())
        if words:
            if 'fix' in words:
                words.remove('fix')
            if len(words) > 3:
                words = words[:3]
            suggested_name = '-'.join(words)
            print(f"   Suggested post-mortem: {commit['date']}_{suggested_name}.md")
        
        print()
    
    print("To create a post-mortem:")
    print("1. Copy the template: cp .claude/templates/post_mortem_template.md .claude/post_mortems/[category]/YYYY-MM-DD_name.md")
    print("2. Edit the file with details of the issue and solution")
    print("3. Update the index: .claude/post_mortems/INDEX.md")

if __name__ == "__main__":
    main()