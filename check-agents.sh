#!/bin/bash
# Agent & Skills Verification Script
# Run this anytime to check your Claude Code agents

echo "🤖 CLAUDE CODE AGENTS & SKILLS CHECKER"
echo "======================================"
echo ""

# Check Agents
echo "📍 AGENTS (.claude/agents/):"
echo "----------------------------"
agent_count=0
for file in .claude/agents/*.md; do
    if [[ "$(basename $file)" != "README.md" ]]; then
        agent_name=$(basename "$file" .md)
        size=$(ls -lh "$file" | awk '{print $5}')
        echo "  ✅ $agent_name ($size)"
        ((agent_count++))
    fi
done
echo "  Total: $agent_count agents"
echo ""

# Check Skills
echo "🛠️  SKILLS (.claude/skills/):"
echo "----------------------------"
skill_count=0
for file in .claude/skills/*.md; do
    if [[ "$(basename $file)" != "README.md" ]]; then
        skill_name=$(basename "$file" .md)
        size=$(ls -lh "$file" | awk '{print $5}')
        echo "  ✅ $skill_name ($size)"
        ((skill_count++))
    fi
done
echo "  Total: $skill_count skills"
echo ""

# Check Commands
echo "⚡ SLASH COMMANDS (.claude/commands/):"
echo "--------------------------------------"
command_count=0
for cmd in backend frontend auth; do
    if [[ -f ".claude/commands/$cmd.md" ]]; then
        size=$(ls -lh ".claude/commands/$cmd.md" | awk '{print $5}')
        echo "  ✅ /$cmd ($size)"
        ((command_count++))
    fi
done
echo "  Total: $command_count agent commands"
echo ""

# Summary
echo "📊 SUMMARY:"
echo "----------"
echo "  Agents: $agent_count"
echo "  Skills: $skill_count"
echo "  Commands: $command_count"
echo ""

if [[ $agent_count -ge 3 ]] && [[ $skill_count -ge 5 ]] && [[ $command_count -ge 3 ]]; then
    echo "✅ All agents and skills are properly installed!"
    echo ""
    echo "🚀 How to use:"
    echo "  /backend  - Database and API development"
    echo "  /frontend - UI component development"
    echo "  /auth     - Authentication setup"
else
    echo "⚠️  Warning: Some components may be missing!"
    echo "   Expected: 3 agents, 5 skills, 3 commands"
fi
echo ""
