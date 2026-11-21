"""ZeroStreet MIT Agent Skills, Foundry MCP Server, and DeepAgents Architect."""

from zerostreet_skills.architect_agent import (
    ARCHITECT_SYSTEM_PROMPT,
    create_zerostreet_architect_agent,
)
from zerostreet_skills.foundry_mcp import (
    AlphaSmithFoundryClient,
    build_validated_policy_config,
    generate_sovereign_scaffold_manifest,
    mcp_server,
)
from zerostreet_skills.skill_registry import (
    DEFAULT_SKILLS_DIR,
    EXPECTED_SKILL_NAMES,
    SkillCatalogEntry,
    discover_skills,
    load_skill_markdown,
    validate_skills_compliance,
)

__version__ = "0.1.0"

__all__ = [
    "ARCHITECT_SYSTEM_PROMPT",
    "AlphaSmithFoundryClient",
    "DEFAULT_SKILLS_DIR",
    "EXPECTED_SKILL_NAMES",
    "SkillCatalogEntry",
    "__version__",
    "build_validated_policy_config",
    "create_zerostreet_architect_agent",
    "discover_skills",
    "generate_sovereign_scaffold_manifest",
    "load_skill_markdown",
    "mcp_server",
    "validate_skills_compliance",
]
