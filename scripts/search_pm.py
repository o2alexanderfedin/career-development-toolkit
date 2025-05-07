#!/usr/bin/env python3
"""
Post-Mortem Search Tool

Searches through post-mortem analysis documents by keywords, tags, categories, 
or other criteria to help quickly find relevant information for troubleshooting.
"""

import os
import re
import sys
import argparse
import yaml
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configuration
PM_ROOT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".claude", "post_mortems")
CATEGORIES = ["infrastructure", "code", "process", "tools", "content"]

def load_frontmatter(file_path: str) -> Optional[Dict[str, Any]]:
    """Extract and parse YAML frontmatter from a markdown file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract frontmatter between --- markers
        frontmatter_match = re.search(r'^---\s(.*?)\s---', content, re.DOTALL)
        if not frontmatter_match:
            return None
        
        frontmatter_text = frontmatter_match.group(1)
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter
    except Exception as e:
        print(f"Error loading frontmatter from {file_path}: {e}", file=sys.stderr)
        return None

def search_file_content(file_path: str, search_term: str) -> bool:
    """Search for a term in the content of a file (excluding frontmatter)"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Remove frontmatter
        content = re.sub(r'^---\s.*?\s---', '', content, flags=re.DOTALL)
        
        # Case-insensitive search
        return search_term.lower() in content.lower()
    except Exception as e:
        print(f"Error searching file {file_path}: {e}", file=sys.stderr)
        return False

def find_post_mortems(
    keyword: Optional[str] = None,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    severity: Optional[str] = None,
    since_date: Optional[str] = None,
    until_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Find post-mortems matching the specified criteria"""
    results = []
    
    # Process date filters
    since_dt = None
    until_dt = None
    
    if since_date:
        try:
            since_dt = datetime.strptime(since_date, "%Y-%m-%d")
        except ValueError:
            print(f"Invalid date format for 'since': {since_date}. Use YYYY-MM-DD.", file=sys.stderr)
    
    if until_date:
        try:
            until_dt = datetime.strptime(until_date, "%Y-%m-%d")
        except ValueError:
            print(f"Invalid date format for 'until': {until_date}. Use YYYY-MM-DD.", file=sys.stderr)
    
    # Determine which directories to search
    dirs_to_search = []
    if category:
        if category not in CATEGORIES:
            print(f"Warning: Unknown category '{category}'. Available categories: {', '.join(CATEGORIES)}", file=sys.stderr)
            return []
        dirs_to_search.append(os.path.join(PM_ROOT_DIR, category))
    else:
        for cat in CATEGORIES:
            dirs_to_search.append(os.path.join(PM_ROOT_DIR, cat))
    
    # Search through directories
    for dir_path in dirs_to_search:
        if not os.path.exists(dir_path):
            continue
        
        for filename in os.listdir(dir_path):
            if not filename.endswith('.md') or filename == 'README.md':
                continue
            
            file_path = os.path.join(dir_path, filename)
            frontmatter = load_frontmatter(file_path)
            
            if not frontmatter:
                continue
            
            # Check date criteria
            if frontmatter.get('date'):
                try:
                    file_date = frontmatter['date']
                    if isinstance(file_date, str):
                        file_dt = datetime.strptime(file_date, "%Y-%m-%d")
                    else:
                        file_dt = file_date  # Already a date object
                    
                    if since_dt and file_dt < since_dt:
                        continue
                    if until_dt and file_dt > until_dt:
                        continue
                except (ValueError, TypeError):
                    # Skip date check if format is invalid
                    pass
            
            # Check severity
            if severity and frontmatter.get('severity', '').lower() != severity.lower():
                continue
            
            # Check tags
            if tags:
                file_tags = [t.lower() for t in frontmatter.get('tags', [])]
                if not all(tag.lower() in file_tags for tag in tags):
                    continue
            
            # Check content keyword
            if keyword and not search_file_content(file_path, keyword):
                continue
            
            # All criteria passed, add to results
            result = {
                'file_path': file_path,
                'relative_path': os.path.relpath(file_path, PM_ROOT_DIR),
                'title': frontmatter.get('title', filename),
                'date': frontmatter.get('date', 'Unknown'),
                'severity': frontmatter.get('severity', 'Unknown'),
                'tags': frontmatter.get('tags', []),
                'categories': frontmatter.get('categories', [])
            }
            results.append(result)
    
    # Sort by date, newest first
    results.sort(key=lambda x: x['date'] if isinstance(x['date'], datetime) else datetime.strptime(str(x['date']), "%Y-%m-%d") if isinstance(x['date'], str) else datetime.min, reverse=True)
    
    return results

def format_results(results: List[Dict[str, Any]], verbose: bool = False) -> str:
    """Format search results for display"""
    if not results:
        return "No matching post-mortems found."
    
    output = f"Found {len(results)} matching post-mortem document(s):\n\n"
    
    for i, result in enumerate(results, 1):
        output += f"{i}. [{result['title']}]({result['relative_path']})\n"
        output += f"   Date: {result['date']}, Severity: {result['severity']}\n"
        
        if verbose:
            output += f"   Tags: {', '.join(result['tags'])}\n"
            output += f"   Categories: {', '.join(result['categories'])}\n"
            output += f"   Path: {result['file_path']}\n"
        
        output += "\n"
    
    return output

def main() -> None:
    """Main function for the post-mortem search tool"""
    parser = argparse.ArgumentParser(description="Search post-mortem documents")
    parser.add_argument("-k", "--keyword", help="Search for keyword in document content")
    parser.add_argument("-t", "--tags", help="Filter by tags (comma-separated)")
    parser.add_argument("-c", "--category", help="Filter by category")
    parser.add_argument("-s", "--severity", help="Filter by severity (low, medium, high, critical)")
    parser.add_argument("--since", help="Filter documents since date (YYYY-MM-DD)")
    parser.add_argument("--until", help="Filter documents until date (YYYY-MM-DD)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    tags_list = args.tags.split(',') if args.tags else None
    
    results = find_post_mortems(
        keyword=args.keyword,
        tags=tags_list,
        category=args.category,
        severity=args.severity,
        since_date=args.since,
        until_date=args.until
    )
    
    print(format_results(results, args.verbose))

if __name__ == "__main__":
    main()