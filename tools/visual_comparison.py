"""
Visual Comparison - Claude Pro Optimizer

Demuestra el impacto real de los 3 archivos de configuración:
  1. .claudeignore  → tokens filtrados del filesystem (scan real)
  2. global.md      → tokens inyectados automáticamente (lectura real del archivo)
  3. smart-init     → tokens de discovery vs CLAUDE.md (archivos reales del proyecto)

Uso:
  python tools/visual_comparison.py                      # analiza directorio actual
  python tools/visual_comparison.py --project /tu/repo   # analiza otro proyecto
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from token_analyzer import (
    analyze_claudeignore, analyze_global_md, analyze_smart_init,
    find_ignore_file, TOKEN_METHOD,
)


class C:
    RED   = '\033[91m'
    GREEN = '\033[92m'
    CYAN  = '\033[96m'
    BOLD  = '\033[1m'
    DIM   = '\033[2m'
    RESET = '\033[0m'


def _bar(value: int, max_val: int, color: str, width: int = 38) -> str:
    filled = int((value / max_val) * width) if max_val > 0 else 0
    return f"{color}{'█' * filled}{'░' * (width - filled)}{C.RESET}"


def header(text: str) -> None:
    print(f"\n{C.BOLD}{C.CYAN}{'═' * 66}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  {text}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═' * 66}{C.RESET}")


def show_claudeignore(project: Path, ignore_file: Path) -> None:
    header("CONFIG 1 · .claudeignore")
    print(f"\n  Qué hace: filtra archivos de ruido antes de que Claude los lea.")
    print(f"  Proyecto: {project}")
    print(f"  Ignorefile: {ignore_file}")
    print(f"  Método de conteo: {TOKEN_METHOD}\n")

    r = analyze_claudeignore(project, ignore_file)
    max_t = r.total_tokens or 1

    print(f"  {'Sin .claudeignore':26}  {_bar(r.total_tokens, max_t, C.RED)}  {r.total_tokens:>10,} tk")
    print(f"  {'Con .claudeignore':26}  {_bar(r.kept_tokens,  max_t, C.GREEN)}  {r.kept_tokens:>10,} tk")

    print(f"\n  Archivos leídos: {r.total_files} → {r.kept_files}  "
          f"({r.ignored_files} ignorados)")
    print(f"\n  {C.GREEN}{C.BOLD}Ahorro real: {r.ignored_tokens:,} tokens ({r.savings_pct:.1f}%){C.RESET}")

    if r.top_ignored:
        print(f"\n  Archivos más pesados que .claudeignore elimina:")
        for f in r.top_ignored[:6]:
            print(f"    {C.DIM}{f.tokens:>8,} tk  [{f.ignore_reason}]  {f.path}{C.RESET}")

    print()


def show_global_md() -> None:
    header("CONFIG 2 · global.md")
    print(f"\n  Qué hace: inyecta tus preferencias automáticamente en cada conversación.")
    print(f"  Sin él: tienes que repetirlas tú en el primer mensaje (o no las aplica).\n")

    r = analyze_global_md()

    if not r.found:
        print(f"  {C.DIM}global.md no encontrado. Instálalo: cp configs/global.md ~/.claude/{C.RESET}\n")
        return

    print(f"  Archivo: {r.file_path}")
    print(f"  Tokens medidos: {C.BOLD}{r.tokens:,}{C.RESET}\n")

    convs = 20
    monthly = r.monthly_savings(convs)
    max_t = monthly

    print(f"  {'Sin global.md (manual por conv)':32}  {_bar(r.tokens, r.tokens, C.RED, 20)}  {r.tokens:>5,} tk/conv")
    print(f"  {'Con global.md (automático)':32}  {_bar(0, r.tokens, C.GREEN, 20)}  {0:>5,} tk/conv")

    print(f"\n  {C.GREEN}{C.BOLD}Ahorro: {r.tokens:,} tk × {convs} conversaciones/mes = {monthly:,} tokens/mes{C.RESET}")
    print(f"  {C.DIM}(Usando ~{convs} conversaciones con contexto nuevo al mes){C.RESET}\n")


def show_smart_init(project: Path) -> None:
    header("CONFIG 3 · smart-init / CLAUDE.md")
    print(f"\n  Qué hace: genera un CLAUDE.md compacto que reemplaza la exploración")
    print(f"  manual del proyecto en cada conversación nueva.")
    print(f"  Proyecto: {project}\n")

    r = analyze_smart_init(project)

    if not r.discovery_files:
        print(f"  {C.DIM}No se encontraron archivos de discovery en la raíz del proyecto.{C.RESET}\n")
        return

    print(f"  Sin CLAUDE.md — Claude lee estos archivos para entender el proyecto:")
    for f in r.discovery_files:
        print(f"    {C.DIM}{f.tokens:>6,} tk  {f.path}{C.RESET}")

    max_t = r.discovery_tokens or 1
    src_label = r.claude_md_path.name if r.claude_md_path else "template SKILL.md"

    print(f"\n  {'Sin CLAUDE.md (discovery)':32}  {_bar(r.discovery_tokens, max_t, C.RED)}  {r.discovery_tokens:>7,} tk")
    print(f"  {f'Con CLAUDE.md ({src_label})':32}  {_bar(r.claude_md_tokens, max_t, C.GREEN)}  {r.claude_md_tokens:>7,} tk")

    print(f"\n  {C.GREEN}{C.BOLD}Ahorro: {r.savings_tokens:,} tokens ({r.savings_pct:.1f}%) por conversación{C.RESET}")
    if not r.claude_md_path:
        print(f"  {C.DIM}(CLAUDE.md no existe en el proyecto — usando template de referencia){C.RESET}")
    print()


def show_summary(r_ignore, r_global, r_init, convs_per_month: int = 20) -> None:
    header("RESUMEN · Ahorro total real")
    print()

    ignore_monthly  = r_ignore.ignored_tokens  # por cada vez que Claude lee el proyecto
    global_monthly  = r_global.monthly_savings(convs_per_month) if r_global.found else 0
    init_per_conv   = r_init.savings_tokens

    rows = [
        (".claudeignore", r_ignore.ignored_tokens, "tokens por lectura de proyecto",
         f"{r_ignore.savings_pct:.0f}% del contexto eliminado"),
        ("global.md",     global_monthly,           f"tokens/mes (~{convs_per_month} conv)",
         f"{r_global.tokens:,} tk × {convs_per_month} conversaciones"),
        ("smart-init",    init_per_conv,             "tokens/conversación (discovery→CLAUDE.md)",
         f"{r_init.savings_pct:.0f}% de reducción de contexto inicial"),
    ]

    max_val = max(v for _, v, _, _ in rows) or 1

    for label, value, unit, detail in rows:
        print(f"  {C.BOLD}{label:<16}{C.RESET} {_bar(value, max_val, C.GREEN, 24)}  "
              f"{C.GREEN}{value:>8,} tk{C.RESET}  {unit}")
        print(f"  {' ' * 16} {C.DIM}{detail}{C.RESET}\n")

    print(f"  {C.DIM}Método de conteo: {TOKEN_METHOD}{C.RESET}\n")


def main(project: Path, ignore_file: Path) -> None:
    print(f"\n{C.BOLD}")
    print("  ╔════════════════════════════════════════════════════════════╗")
    print("  ║       CLAUDE PRO OPTIMIZER — IMPACTO REAL                 ║")
    print("  ╚════════════════════════════════════════════════════════════╝")
    print(C.RESET)

    r_ignore = analyze_claudeignore(project, ignore_file)
    r_global = analyze_global_md()
    r_init   = analyze_smart_init(project)

    show_claudeignore(project, ignore_file)
    show_global_md()
    show_smart_init(project)
    show_summary(r_ignore, r_global, r_init)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(
        description='Muestra el impacto real de los 3 configs de Claude Pro Optimizer'
    )
    parser.add_argument('--project', default='.', help='Proyecto a analizar (default: .)')
    parser.add_argument('--ignore-file', default=None, help='Ruta al .claudeignore')
    args = parser.parse_args()

    project     = Path(args.project).resolve()
    ignore_file = Path(args.ignore_file).resolve() if args.ignore_file else find_ignore_file(project)

    try:
        main(project, ignore_file)
    except KeyboardInterrupt:
        print(f"\n{C.DIM}Interrumpido{C.RESET}")
        sys.exit(0)
