# TODO List

## LinkedIn MCP Server Setup

1. **Configure LinkedIn MCP Server**
   - [ ] Download ChromeDriver matching your Chrome version
   - [ ] Create `.env` file with LinkedIn credentials
   - [ ] Create/update Claude Desktop configuration at `~/Library/Application Support/Claude/claude_desktop_config.json`
   - [ ] Test MCP server connection with Claude

   ```bash
   # Activate virtual environment
   cd ~/Library/CloudStorage/OneDrive-Personal/Jobs/AI/MCPs/linkedin-servers
   source venv/linkedin-mcp-server-env/bin/activate
   
   # Run the server
   cd linkedin-mcp-server
   python main.py --no-headless
   ```

2. **Test Job Search Capabilities**
   - [ ] Search for jobs with specific criteria
   - [ ] View job details and application requirements
   - [ ] Test resume analysis against job descriptions
   - [ ] Try sending connection requests (if desired)

3. **Alternative Setup (If Needed)**
   - [ ] Configure `linkedin-mcp` server as backup option
   - [ ] Test with more basic job search functionality

## Configuration Templates

### Claude Desktop Configuration Example
```json
{
  "mcpServers": {
    "linkedin-mcp-server": {
      "command": "/Users/alexanderfedin/Library/CloudStorage/OneDrive-Personal/Jobs/AI/MCPs/linkedin-servers/venv/linkedin-mcp-server-env/bin/python",
      "args": [
        "/Users/alexanderfedin/Library/CloudStorage/OneDrive-Personal/Jobs/AI/MCPs/linkedin-servers/linkedin-mcp-server/main.py",
        "--no-headless"
      ],
      "env": {
        "LINKEDIN_EMAIL": "your_email@example.com",
        "LINKEDIN_PASSWORD": "your_password"
      }
    }
  }
}
```

### Environment File Template
```
# LinkedIn Credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Server Configuration (if needed)
# CHROMEDRIVER=/path/to/chromedriver
```

## Additional Notes
- LinkedIn MCP servers will not be tracked by git (in `.gitignore`)
- Be mindful of LinkedIn's terms of service when using automation tools
- Consider adding a scheduled task to update ChromeDriver when Chrome updates