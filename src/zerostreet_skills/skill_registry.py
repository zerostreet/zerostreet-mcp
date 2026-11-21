"""Agent Skills Progressive Disclosure 레지스트리 및 규제/무결성 검증 유틸리티."""

import re
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

DEFAULT_SKILLS_DIR = Path(__file__).resolve().parents[2] / "skills"

EXPECTED_SKILL_NAMES: tuple[str, ...] = (
    "macro-crisis-sim",
    "portfolio-risk-audit",
    "pre-trade-risk-gate",
    "rebalance-math-solver",
    "sovereign-system-architect",
)

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_FORBIDDEN_WEIGHT_SUFFIXES: tuple[str, ...] = (".pt", ".pth", ".safetensors", ".onnx", ".ckpt")


class SkillCatalogEntry(BaseModel):
    """Progressive Disclosure Level 1 메타데이터 항목."""

    name: str
    description: str
    license: str = "MIT"
    path: str
    allowed_tools: list[str] = Field(default_factory=list)


def _parse_frontmatter(content: str, skill_path: Path, dir_name: str) -> SkillCatalogEntry:
    match = _FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError(f"Missing YAML frontmatter in {skill_path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"Frontmatter must be a YAML mapping in {skill_path}")

    name = str(data.get("name", "")).strip()
    description = str(data.get("description", "")).strip()
    license_name = str(data.get("license", "")).strip() or "MIT"
    if not name or not description:
        raise ValueError(f"Both 'name' and 'description' are required in {skill_path}")
    if name != dir_name:
        raise ValueError(f"Skill name '{name}' must match directory name '{dir_name}'")

    raw_allowed = data.get("allowed-tools")
    allowed: list[str] = []
    if isinstance(raw_allowed, str):
        allowed = [tok for tok in re.split(r"[\s,]+", raw_allowed) if tok]
    elif isinstance(raw_allowed, list):
        allowed = [str(item).strip() for item in raw_allowed if str(item).strip()]

    return SkillCatalogEntry(
        name=name,
        description=description,
        license=license_name,
        path=str(skill_path),
        allowed_tools=allowed,
    )


def discover_skills(skills_dir: Path = DEFAULT_SKILLS_DIR) -> list[SkillCatalogEntry]:
    """디렉터리 내 모든 SKILL.md Level 1 메타데이터를 정렬하여 반환합니다."""
    root = Path(skills_dir)
    if not root.exists():
        return []

    entries: list[SkillCatalogEntry] = []
    for subdir in sorted(root.iterdir()):
        if not subdir.is_dir():
            continue
        skill_md = subdir / "SKILL.md"
        if not skill_md.is_file():
            continue
        content = skill_md.read_text(encoding="utf-8")
        entries.append(_parse_frontmatter(content, skill_md, subdir.name))
    return entries


def load_skill_markdown(skill_name: str, skills_dir: Path = DEFAULT_SKILLS_DIR) -> str:
    """Progressive Disclosure Level 2: 지정 스킬의 SKILL.md 본문을 로드합니다."""
    cleaned = skill_name.strip()
    if not cleaned or "/" in cleaned or "\\" in cleaned or ".." in cleaned:
        raise ValueError(f"Invalid skill name: {skill_name!r}")

    target = (Path(skills_dir) / cleaned / "SKILL.md").resolve()
    root_resolved = Path(skills_dir).resolve()
    if root_resolved not in target.parents:
        raise ValueError(f"Skill path escapes skills directory: {skill_name!r}")
    if not target.is_file():
        raise FileNotFoundError(f"SKILL.md not found for skill '{cleaned}'")
    return target.read_text(encoding="utf-8")


def validate_skills_compliance(skills_dir: Path = DEFAULT_SKILLS_DIR) -> list[str]:
    """5종 MIT 스킬 규격 및 비투자자문/0바이트 가중치 컴플라이언스를 검증합니다."""
    root = Path(skills_dir)
    errors: list[str] = []

    if not root.exists():
        return [f"Skills directory does not exist: {root}"]

    for file_path in root.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in _FORBIDDEN_WEIGHT_SUFFIXES:
            errors.append(f"Forbidden binary model weight artifact in MIT skills: {file_path}")

    try:
        entries = discover_skills(root)
    except Exception as exc:
        return [f"Skill discovery failed: {exc}"]

    found_names = {entry.name for entry in entries}
    for expected in EXPECTED_SKILL_NAMES:
        if expected not in found_names:
            errors.append(f"Missing expected Agent Skill: {expected}")

    for entry in entries:
        if len(entry.name) > 64:
            errors.append(f"Skill '{entry.name}' name exceeds 64 characters")
        if len(entry.description) > 1024:
            errors.append(f"Skill '{entry.name}' description exceeds 1024 characters")
        if entry.license != "MIT":
            errors.append(f"Skill '{entry.name}' must use MIT license, found {entry.license!r}")

    return errors
