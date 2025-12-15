# 🔍 How to Check Your Claude Code Agents

## Quick Verification Methods

### Method 1: Run the Verification Script ⚡ (Easiest)

```bash
./check-agents.sh
```

This will show:
- All installed agents
- All available skills
- All slash commands
- Summary and status

---

### Method 2: Manual File Check 📂

#### Check Agents:
```bash
ls -lh .claude/agents/
```

**Expected output:**
```
auth-specialist.md       (13K)
backend-architect.md     (8.5K)
frontend-builder.md      (12K)
```

#### Check Skills:
```bash
ls -lh .claude/skills/
```

**Expected output:**
```
api-client-generator.md           (13K)
auth-integration-helper.md        (15K)
database-schema-generator.md      (9.8K)
fastapi-generator.md              (6.2K)
nextjs-component-generator.md     (11K)
```

#### Check Slash Commands:
```bash
ls -lh .claude/commands/{backend,frontend,auth}.md
```

**Expected output:**
```
.claude/commands/auth.md      (1.6K)
.claude/commands/backend.md   (1.2K)
.claude/commands/frontend.md  (1.3K)
```

---

### Method 3: View Agent Details 📖

#### Read Backend Agent:
```bash
cat .claude/agents/backend-architect.md | head -30
```

#### Read Frontend Agent:
```bash
cat .claude/agents/frontend-builder.md | head -30
```

#### Read Auth Agent:
```bash
cat .claude/agents/auth-specialist.md | head -30
```

---

### Method 4: Test Slash Commands 🧪

In Claude Code CLI, try these commands:

#### Test Backend Agent:
```
/backend Create a simple Task model with id, title, and completed fields
```

#### Test Frontend Agent:
```
/frontend Create a TaskCard component that displays task information
```

#### Test Auth Agent:
```
/auth Set up JWT authentication with email/password
```

---

## Expected Results ✅

When everything is working, you should see:

### ✅ 3 Agents:
1. **backend-architect** - FastAPI & database development
2. **frontend-builder** - Next.js & React components
3. **auth-specialist** - Authentication & security

### ✅ 5 Skills:
1. **fastapi-generator** - Generate API endpoints
2. **database-schema-generator** - Create database models
3. **nextjs-component-generator** - Build React components
4. **api-client-generator** - Create type-safe API clients
5. **auth-integration-helper** - Setup authentication

### ✅ 3 Slash Commands:
1. **/backend** - Invoke Backend Architect
2. **/frontend** - Invoke Frontend Builder
3. **/auth** - Invoke Auth Specialist

---

## Common Issues 🐛

### "No such file or directory"
→ Make sure you're in the project root directory:
```bash
cd /mnt/c/Users/nehak/OneDrive/Desktop/hackathon\ 2\ todo/hacathon2/
```

### "Agents not showing"
→ They're in `.claude/` (hidden folder), not `/agents`:
```bash
ls -la | grep .claude
```

### "Slash commands don't work"
→ Make sure you're using Claude Code CLI and the commands are properly formatted:
- Correct: `/backend Create a Task model`
- Incorrect: `backend Create a Task model`

---

## Quick Test 🎯

Run this one-liner to verify everything:

```bash
echo "Agents: $(ls -1 .claude/agents/*.md 2>/dev/null | grep -v README | wc -l)/3" && \
echo "Skills: $(ls -1 .claude/skills/*.md 2>/dev/null | grep -v README | wc -l)/5" && \
echo "Commands: $(ls -1 .claude/commands/{backend,frontend,auth}.md 2>/dev/null | wc -l)/3"
```

**Expected output:**
```
Agents: 3/3
Skills: 5/5
Commands: 3/3
```

---

## How to Use Agents in Claude Code 🚀

### Option 1: Slash Commands (Recommended)
```
/backend Create REST API for task management
/frontend Build a task list UI
/auth Set up user authentication
```

### Option 2: Natural Language
Just describe your task:
```
"I need a FastAPI endpoint for creating tasks"
→ Claude will suggest using Backend Architect agent
```

### Option 3: Direct Reference
```
"Use the Backend Architect agent to create database models"
```

---

## Files Created 📄

- `check-agents.sh` - Quick verification script
- `AGENTS_STATUS.md` - Complete status report
- `HOW-TO-CHECK-AGENTS.md` - This guide

---

## Need More Help? 🆘

### View Complete Agent Definition:
```bash
cat .claude/agents/backend-architect.md
```

### View Complete Skill Definition:
```bash
cat .claude/skills/fastapi-generator.md
```

### View All README Files:
```bash
cat .claude/agents/README.md
cat .claude/skills/README.md
```

---

## Success Indicators ✨

Your agents are working if:
- ✅ All files exist in `.claude/` directory
- ✅ Verification script shows 3/3 agents
- ✅ Slash commands are recognized
- ✅ Agents respond to task requests
- ✅ Generated code follows expected patterns

---

**You're all set!** 🎉

Your agents and skills are ready for the hackathon. Time to build something amazing!
