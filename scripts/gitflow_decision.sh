#!/bin/sh
# gitflow_decision.sh - Helper script to check if a gitflow operation should proceed

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

FLOW_TYPE="$1"  # feature, bugfix, hotfix, release
BRANCH_NAME="$2"

echo "${BLUE}----------------------------------------${NC}"
echo "${BLUE}🔄 GitFlow ${FLOW_TYPE^} Decision${NC}"
echo "${BLUE}----------------------------------------${NC}"

# Check if there are any changes to commit
if [ -z "$(git status --porcelain)" ]; then
    # No changes found
    echo "${YELLOW}No changes were detected on this ${FLOW_TYPE} branch (${BRANCH_NAME}).${NC}"
    echo ""
    echo "Options:"
    echo "1) Cancel the ${FLOW_TYPE} (no changes to commit)"
    echo "2) Continue anyway (e.g., for documentation only changes)"
    
    read -p "Enter your choice (1/2): " choice
    
    if [ "$choice" = "1" ]; then
        echo ""
        echo "${GREEN}✅ Canceling the ${FLOW_TYPE}. No changes will be committed.${NC}"
        # Determine which branch to checkout based on flow type
        TARGET_BRANCH="develop"
        if [ "$FLOW_TYPE" = "hotfix" ]; then
            TARGET_BRANCH="main"
        fi
        
        echo "Switching back to ${TARGET_BRANCH}..."
        git checkout "$TARGET_BRANCH"
        
        # Delete the feature branch
        echo "Deleting the ${FLOW_TYPE} branch ${BRANCH_NAME}..."
        git branch -D "$BRANCH_NAME"
        
        echo "${BLUE}----------------------------------------${NC}"
        exit 1  # Return non-zero to abort any further gitflow operations
    else
        echo ""
        echo "${GREEN}✅ Continuing with the ${FLOW_TYPE} finish process...${NC}"
    fi
else
    # Changes found, just report them
    FILES_CHANGED=$(git status --porcelain | wc -l | tr -d ' ')
    echo "${GREEN}✅ Found ${FILES_CHANGED} file(s) with changes.${NC}"
    echo "Continuing with the ${FLOW_TYPE} finish process..."
fi

echo "${BLUE}----------------------------------------${NC}"
exit 0  # Return success to continue with gitflow operations