# LLM Instructions for Content Weaver Execution

## 1. Virtual Environment Check
**Before running any commands, verify virtual environment is active:**
- Check if `VIRTUAL_ENV` environment variable is set
- If not active, prompt user to activate with: `source venv/bin/activate`
- Verify Python and pip are available within venv

## 2. Command Execution Protocol
**Always check with user before running commands:**
- Display the exact command to be executed
- Explain what the command does
- Wait for explicit user confirmation (y/n)
- Never execute commands without user approval

## 3. Project Context Files
**Review these files for complete project understanding:**
- `content-weaver-README.md` - Project overview and getting started
- `design.md` - System architecture and component descriptions
- `implementation.md` - Development roadmap and PR structure
- `journal.md` - Development notes and integration details

## 4. Execution Checklist
Before running Content Weaver:
1. ✅ Check venv activation
2. ✅ Verify dependencies installed (`pip install -r requirements.txt`)
3. ✅ Confirm API keys in `.env` file
4. ✅ Get user approval for execution command
5. ✅ Review current topic in `main.py` (currently: "The future of AI")

## 5. Testing Options
- **Full run**: `python3 main.py` (uses real APIs)
- **Simulated run**: Check if `simulate_llm_calls` flag available in OrchestratorAgent
- **Individual agent tests**: Run specific test files in `tests/` directory