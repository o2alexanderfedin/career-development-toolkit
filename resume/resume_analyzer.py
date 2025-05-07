#!/usr/bin/env python3
"""
Resume Analyzer - Analyzes resume content and provides suggestions for improvement
"""

import os
import re
import sys
from pathlib import Path

# Set paths
RESUME_DIR = "/Users/alexanderfedin/Library/CloudStorage/OneDrive-Personal/Jobs/AI/resume"
SECTIONS_DIR = f"{RESUME_DIR}/sections"
REPORTS_DIR = f"{RESUME_DIR}/reports"

# Ensure reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)

# Keywords for different roles
KEYWORDS = {
    "engineering_manager": [
        "leadership", "team", "manage", "strategy", "agile", "scrum", "mentoring", 
        "architecture", "roadmap", "planning", "hiring", "cross-functional"
    ],
    "technical_director": [
        "director", "vision", "strategy", "leadership", "architecture", "enterprise", 
        "governance", "innovation", "transformation", "stakeholder", "executive"
    ],
    "cto": [
        "strategy", "executive", "vision", "innovation", "transformation", 
        "leadership", "architecture", "enterprise", "roadmap", "board", "c-level"
    ]
}

# Action verbs by category
ACTION_VERBS = {
    "leadership": [
        "led", "directed", "managed", "guided", "mentored", "spearheaded", "orchestrated",
        "oversaw", "championed", "established", "influenced", "transformed"
    ],
    "achievement": [
        "achieved", "delivered", "increased", "reduced", "improved", "accelerated", 
        "generated", "exceeded", "optimized", "maximized", "streamlined"
    ],
    "technical": [
        "developed", "implemented", "architected", "engineered", "designed", "built",
        "coded", "programmed", "integrated", "deployed", "migrated", "automated"
    ]
}

def read_section(section_name):
    """Read content from a section file"""
    file_path = f"{SECTIONS_DIR}/{section_name}.md"
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Warning: {section_name}.md not found")
        return ""

def analyze_keyword_density(text, role):
    """Analyze keyword density for a specific role"""
    if role not in KEYWORDS:
        print(f"Error: Role '{role}' not found in keyword database")
        return {}
    
    results = {}
    total_words = len(re.findall(r'\b\w+\b', text.lower()))
    
    for keyword in KEYWORDS[role]:
        count = len(re.findall(r'\b' + keyword + r'\b', text.lower()))
        if total_words > 0:
            density = (count / total_words) * 100
        else:
            density = 0
        results[keyword] = {
            'count': count,
            'density': density
        }
    
    return results

def analyze_action_verbs(text):
    """Analyze action verb usage"""
    results = {}
    for category, verbs in ACTION_VERBS.items():
        category_count = 0
        for verb in verbs:
            category_count += len(re.findall(r'\b' + verb + r'\b', text.lower()))
        results[category] = category_count
    
    return results

def calculate_metrics(text):
    """Calculate various resume metrics"""
    metrics = {}
    
    # Count words
    metrics['word_count'] = len(re.findall(r'\b\w+\b', text))
    
    # Count sentences
    metrics['sentence_count'] = len(re.findall(r'[.!?]+', text))
    
    # Count bullet points
    metrics['bullet_points'] = text.count('- ')
    
    # Count numbers/metrics
    metrics['numbers'] = len(re.findall(r'\b\d+%?\b', text))
    
    # Average words per sentence
    if metrics['sentence_count'] > 0:
        metrics['avg_words_per_sentence'] = metrics['word_count'] / metrics['sentence_count']
    else:
        metrics['avg_words_per_sentence'] = 0
    
    return metrics

def generate_report(role):
    """Generate analysis report for a specific role"""
    # Read all sections
    sections = ['summary', 'skills', 'experience', 'education', 'projects', 'certifications']
    content = ""
    for section in sections:
        content += read_section(section)
    
    # Analyze keyword density
    keyword_results = analyze_keyword_density(content, role)
    
    # Analyze action verbs
    verb_results = analyze_action_verbs(content)
    
    # Calculate metrics
    metrics = calculate_metrics(content)
    
    # Generate report
    report = f"# Resume Analysis for {role.replace('_', ' ').title()} Role\n\n"
    
    report += "## Content Metrics\n\n"
    report += f"- **Total Word Count:** {metrics['word_count']}\n"
    report += f"- **Sentence Count:** {metrics['sentence_count']}\n"
    report += f"- **Bullet Points:** {metrics['bullet_points']}\n"
    report += f"- **Numbers/Metrics Used:** {metrics['numbers']}\n"
    report += f"- **Avg Words Per Sentence:** {metrics['avg_words_per_sentence']:.1f}\n\n"
    
    report += "## Key Role-Specific Keywords\n\n"
    report += "| Keyword | Count | Density |\n"
    report += "|---------|-------|--------|\n"
    for keyword, data in keyword_results.items():
        report += f"| {keyword} | {data['count']} | {data['density']:.1f}% |\n"
    report += "\n"
    
    report += "## Action Verb Analysis\n\n"
    for category, count in verb_results.items():
        report += f"- **{category.title()} Verbs:** {count}\n"
    
    report += "\n## Recommendations\n\n"
    
    # Generate recommendations based on findings
    low_keywords = [k for k, v in keyword_results.items() if v['count'] < 2]
    if low_keywords:
        report += f"- **Add More Keywords:** Consider adding these underrepresented keywords: {', '.join(low_keywords)}\n"
    
    low_verbs = [c for c, count in verb_results.items() if count < 5]
    if low_verbs:
        report += f"- **Strengthen Verb Usage:** Add more {', '.join(low_verbs)} verbs to better position your experience\n"
    
    if metrics['numbers'] < 10:
        report += "- **Add More Metrics:** Include more quantifiable achievements and metrics\n"
    
    if metrics['bullet_points'] < 15:
        report += "- **Add More Bullet Points:** Consider using more bullet points for better readability\n"
    
    # Write report
    report_path = f"{REPORTS_DIR}/{role}_analysis.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"Report generated: {report_path}")
    return report_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python resume_analyzer.py <role>")
        print("Available roles: engineering_manager, technical_director, cto")
        return
    
    role = sys.argv[1]
    if role not in KEYWORDS:
        print(f"Error: Role '{role}' not supported")
        print(f"Available roles: {', '.join(KEYWORDS.keys())}")
        return
    
    report_path = generate_report(role)
    print(f"Analysis complete! Report saved to {report_path}")

if __name__ == "__main__":
    main()