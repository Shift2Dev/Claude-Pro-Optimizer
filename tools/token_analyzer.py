"""
Token Analyzer - Motor de medición real para Claude Pro Optimizer

Mide el impacto concreto de cada uno de los 3 archivos de configuración:
  1. .claudeignore  → tokens filtrados del filesystem
  2. global.md      → tokens inyectados automáticamente por conversación
  3. CLAUDE.md      → tokens de "discovery" reemplazados por un archivo compacto

No hay números inventados: todo viene de leer archivos reales.
"""
import fnmatch
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

# Token counting: tiktoken si está instalado, si no chars/4
try:
    import tiktoken
    _enc = tiktoken.get_encoding("cl100k_base")
    def count_tokens(text: str) -> int:
        return len(_enc.encode(text))
    TOKEN_METHOD = "tiktoken (cl100k_base)"
except ImportError:
    def count_tokens(text: str) -> int:
        return max(1, len(text) // 4)
    TOKEN_METHOD = "estimado (chars ÷ 4)"

TEXT_EXTENSIONS = frozenset({
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs',
    '.rb', '.php', '.cs', '.cpp', '.c', '.h', '.swift', '.kt',
    '.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.ini',
    '.env', '.sh', '.bash', '.html', '.css', '.scss', '.sql',
    '.xml', '.gradle', '.properties', '.lock', '.cfg', '.conf',
})

# Archivos que Claude lee para entender un proyecto cuando no hay CLAUDE.md
DISCOVERY_PATTERNS = [
    'README*', 'readme*',
    'package.json', 'pyproject.toml', 'setup.py', 'setup.cfg',
    'requirements*.txt', 'Pipfile',
    'Cargo.toml', 'pom.xml', 'build.gradle', 'go.mod', 'go.sum',
    'Makefile', 'makefile',
    'docker-compose*.yml', 'docker-compose*.yaml', 'Dockerfile*',
    '.env.example', '.env.sample',
    'tsconfig.json', 'jsconfig.json',
    'vite.config.*', 'webpack.config.*', 'next.config.*',
    '*.gemspec', 'Gemfile',
]

MAX_FILE_BYTES = 512_000


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class FileStats:
    path: str
    tokens: int
    ignored: bool
    ignore_reason: str


@dataclass
class ClaudeIgnoreResult:
    """Resultado del escenario 1: .claudeignore"""
    project_name: str
    total_files: int
    total_tokens: int
    kept_files: int
    kept_tokens: int
    ignored_files: int
    ignored_tokens: int
    top_ignored: List[FileStats]
    token_method: str

    @property
    def savings_pct(self) -> float:
        return (self.ignored_tokens / self.total_tokens * 100) if self.total_tokens else 0.0


@dataclass
class GlobalMdResult:
    """Resultado del escenario 2: global.md"""
    file_path: Path
    tokens: int
    token_method: str
    found: bool = True

    def monthly_savings(self, conversations: int = 20) -> int:
        return self.tokens * conversations


@dataclass
class SmartInitResult:
    """Resultado del escenario 3: smart-init / CLAUDE.md"""
    project_name: str
    discovery_files: List[FileStats]
    claude_md_path: Optional[Path]
    claude_md_tokens: int
    token_method: str

    @property
    def discovery_tokens(self) -> int:
        return sum(f.tokens for f in self.discovery_files)

    @property
    def savings_tokens(self) -> int:
        return self.discovery_tokens - self.claude_md_tokens

    @property
    def savings_pct(self) -> float:
        return (self.savings_tokens / self.discovery_tokens * 100) if self.discovery_tokens else 0.0


# ── Helpers internos ──────────────────────────────────────────────────────────

def _read_tokens(path: Path) -> int:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return 0
        return count_tokens(path.read_text(encoding='utf-8', errors='ignore'))
    except (OSError, PermissionError):
        return 0


def load_patterns(ignore_file: Path) -> List[str]:
    if not ignore_file.exists():
        return []
    return [
        line.strip()
        for line in ignore_file.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.strip().startswith('#')
    ]


def _is_ignored(file_path: Path, base: Path, patterns: List[str]) -> Tuple[bool, str]:
    rel   = str(file_path.relative_to(base)).replace('\\', '/')
    name  = file_path.name
    parts = rel.split('/')
    for pat in patterns:
        clean = pat.rstrip('/')
        if fnmatch.fnmatch(name, clean):
            return True, pat
        for part in parts:
            if fnmatch.fnmatch(part, clean):
                return True, pat
        if fnmatch.fnmatch(rel, clean) or fnmatch.fnmatch(rel, f'{clean}/*'):
            return True, pat
    return False, ''


def find_ignore_file(project: Path) -> Path:
    candidates = [
        project / '.claudeignore',
        Path(__file__).parent.parent / 'configs' / '.claudeignore',
        Path.home() / '.claude' / '.claudeignore',
    ]
    return next((p for p in candidates if p.exists()), candidates[1])


def find_global_md() -> Optional[Path]:
    candidates = [
        Path(__file__).parent.parent / 'configs' / 'global.md',
        Path.home() / '.claude' / 'global.md',
    ]
    return next((p for p in candidates if p.exists()), None)


def find_claude_md(project: Path) -> Optional[Path]:
    candidates = [
        project / 'CLAUDE.md',
        project / '.claude' / 'CLAUDE.md',
    ]
    return next((p for p in candidates if p.exists()), None)


# ── Escenario 1: .claudeignore ────────────────────────────────────────────────

def analyze_claudeignore(project: Path, ignore_file: Path) -> ClaudeIgnoreResult:
    """Escanea el proyecto y mide cuántos tokens filtra .claudeignore."""
    patterns = load_patterns(ignore_file)
    files: List[FileStats] = []

    for path in sorted(project.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        ignored, reason = _is_ignored(path, project, patterns)
        tokens = _read_tokens(path)
        if tokens:
            files.append(FileStats(
                path=str(path.relative_to(project)).replace('\\', '/'),
                tokens=tokens,
                ignored=ignored,
                ignore_reason=reason,
            ))

    ignored = [f for f in files if f.ignored]
    kept    = [f for f in files if not f.ignored]
    return ClaudeIgnoreResult(
        project_name=project.name,
        total_files=len(files),
        total_tokens=sum(f.tokens for f in files),
        kept_files=len(kept),
        kept_tokens=sum(f.tokens for f in kept),
        ignored_files=len(ignored),
        ignored_tokens=sum(f.tokens for f in ignored),
        top_ignored=sorted(ignored, key=lambda x: x.tokens, reverse=True)[:8],
        token_method=TOKEN_METHOD,
    )


# ── Escenario 2: global.md ────────────────────────────────────────────────────

def analyze_global_md() -> GlobalMdResult:
    """Lee el archivo global.md real y cuenta sus tokens."""
    path = find_global_md()
    if not path:
        return GlobalMdResult(file_path=Path('global.md'), tokens=0,
                              token_method=TOKEN_METHOD, found=False)
    tokens = count_tokens(path.read_text(encoding='utf-8'))
    return GlobalMdResult(file_path=path, tokens=tokens, token_method=TOKEN_METHOD)


# ── Escenario 3: smart-init / CLAUDE.md ──────────────────────────────────────

def analyze_smart_init(project: Path) -> SmartInitResult:
    """
    Mide los tokens de los archivos que Claude leeforiosamente sin CLAUDE.md
    (README, package.json, pyproject.toml, etc.) vs. los de un CLAUDE.md compacto.
    """
    # Archivos de discovery: solo raíz del proyecto
    discovery: List[FileStats] = []
    for path in sorted(project.iterdir()):
        if not path.is_file():
            continue
        for pattern in DISCOVERY_PATTERNS:
            if fnmatch.fnmatch(path.name, pattern):
                tokens = _read_tokens(path)
                if tokens:
                    discovery.append(FileStats(
                        path=path.name,
                        tokens=tokens,
                        ignored=False,
                        ignore_reason='',
                    ))
                break  # no duplicar si matchea varios patrones

    # CLAUDE.md existente en el proyecto
    claude_md = find_claude_md(project)
    if claude_md:
        claude_tokens = count_tokens(claude_md.read_text(encoding='utf-8'))
    else:
        # Si no existe, usa el template del skill como referencia del output esperado
        template = Path(__file__).parent.parent / 'configs' / 'skills' / 'smart-init' / 'SKILL.md'
        claude_tokens = count_tokens(template.read_text(encoding='utf-8')) if template.exists() else 0

    return SmartInitResult(
        project_name=project.name,
        discovery_files=sorted(discovery, key=lambda x: x.tokens, reverse=True),
        claude_md_path=claude_md,
        claude_md_tokens=claude_tokens,
        token_method=TOKEN_METHOD,
    )


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(
        description='Mide el impacto real de cada config de Claude Pro Optimizer'
    )
    parser.add_argument('project', nargs='?', default='.', help='Proyecto a analizar')
    parser.add_argument('--ignore-file', default=None)
    args = parser.parse_args()

    project = Path(args.project).resolve()
    if not project.exists():
        print(f"Error: no existe '{project}'"); sys.exit(1)

    ignore_file = Path(args.ignore_file).resolve() if args.ignore_file else find_ignore_file(project)

    sep = '─' * 60

    # 1. .claudeignore
    r1 = analyze_claudeignore(project, ignore_file)
    print(f"\n{sep}\n  .claudeignore — {r1.project_name}\n{sep}")
    print(f"  Sin filtro: {r1.total_files} archivos → {r1.total_tokens:,} tokens")
    print(f"  Con filtro: {r1.kept_files} archivos → {r1.kept_tokens:,} tokens")
    print(f"  Ahorro: {r1.ignored_tokens:,} tokens ({r1.savings_pct:.1f}%)")
    for f in r1.top_ignored[:5]:
        print(f"    {f.tokens:>8,} tk  [{f.ignore_reason}]  {f.path}")

    # 2. global.md
    r2 = analyze_global_md()
    print(f"\n{sep}\n  global.md\n{sep}")
    if r2.found:
        print(f"  Archivo: {r2.file_path}")
        print(f"  Tokens: {r2.tokens:,} inyectados automáticamente por conversación")
        print(f"  Ahorro mensual (~20 conv): {r2.monthly_savings():,} tokens")
    else:
        print("  No encontrado. Instala: cp configs/global.md ~/.claude/")

    # 3. smart-init
    r3 = analyze_smart_init(project)
    print(f"\n{sep}\n  smart-init / CLAUDE.md — {r3.project_name}\n{sep}")
    print(f"  Sin CLAUDE.md, Claude lee estos archivos para entender el proyecto:")
    for f in r3.discovery_files:
        print(f"    {f.tokens:>6,} tk  {f.path}")
    print(f"  Total discovery: {r3.discovery_tokens:,} tokens por conversación")
    src = r3.claude_md_path or "template SKILL.md"
    print(f"  Con CLAUDE.md ({src}): {r3.claude_md_tokens:,} tokens")
    print(f"  Ahorro: {r3.savings_tokens:,} tokens ({r3.savings_pct:.1f}%) por conversación")
    print(f"\n{sep}\n")
