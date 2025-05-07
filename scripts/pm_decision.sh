#!/bin/sh
# pm_decision.sh - Helper script to prompt for post-mortem decision

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

TITLE="$1"
EVENT_TYPE="$2"
TEMPLATE_CMD="$3"

echo "${BLUE}----------------------------------------${NC}"
echo "${BLUE}🔄 ${TITLE}${NC}"
echo "${BLUE}----------------------------------------${NC}"

# Ask if this event needs a post-mortem
echo "${YELLOW}Question:${NC} Did you encounter any issues or learn anything significant during this ${EVENT_TYPE}?"
echo "1) Yes - I should document this in a post-mortem"
echo "2) No - Nothing significant to document"

read -p "Enter your choice (1/2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "Great! Create a post-mortem to document the insights and solutions:"
    echo "  - Create from template: ${GREEN}${TEMPLATE_CMD}${NC}"
    echo "  - Edit the post-mortem file based on the template"
    echo "  - Update the index: ${GREEN}[editor] .claude/post_mortems/INDEX.md${NC}"
else
    echo ""
    echo "${GREEN}✅ No post-mortem needed for this event. Continuing...${NC}"
fi

echo "${BLUE}----------------------------------------${NC}"