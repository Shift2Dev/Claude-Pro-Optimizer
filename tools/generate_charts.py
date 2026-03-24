"""
Generador de Graficos Profesionales - Claude Pro Optimizer

4 graficos con datos reales medidos:
  1. .claudeignore  -> tokens filtrados con breakdown de archivos
  2. global.md      -> reglas de comportamiento + cobertura por conversacion
  3. smart-init     -> discovery files vs CLAUDE.md compacto
  4. summary        -> impacto combinado de los 3 configs

Requiere: pip install matplotlib numpy
Uso:
  python tools/generate_charts.py --project /tu/repo [--output-dir ./charts]
"""
import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from token_analyzer import (
    analyze_claudeignore, analyze_global_md, analyze_smart_init,
    find_ignore_file, TOKEN_METHOD, count_tokens,
    ClaudeIgnoreResult, GlobalMdResult, SmartInitResult,
)

CONVS_PER_MONTH = 20

# ---------------------------------------------------------------------------
# Design System
# ---------------------------------------------------------------------------

P = {
    'bg':          '#FFFFFF',
    'panel':       '#F8F9FA',
    'bad':         '#C92A2A',
    'bad_mid':     '#E03131',
    'bad_light':   '#FFF5F5',
    'good':        '#2B8A3E',
    'good_mid':    '#40C057',
    'good_light':  '#EBFBEE',
    'blue':        '#1864AB',
    'blue_mid':    '#339AF0',
    'blue_light':  '#E7F5FF',
    'orange':      '#D9480F',
    'orange_mid':  '#FF922B',
    'orange_light':'#FFF4E6',
    'purple':      '#5F3DC4',
    'text':        '#212529',
    'sub':         '#868E96',
    'muted':       '#ADB5BD',
    'border':      '#DEE2E6',
    'grid':        '#F1F3F5',
}

FONT_TITLE    = {'fontsize': 22, 'fontweight': 'bold', 'color': P['text']}
FONT_SUBTITLE = {'fontsize': 11, 'color': P['sub']}

plt.rcParams.update({
    'font.family':        'Segoe UI',
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.spines.left':   True,
    'axes.spines.bottom': True,
    'axes.edgecolor':     P['border'],
    'axes.linewidth':     0.7,
    'axes.labelsize':     10,
    'axes.labelcolor':    P['sub'],
    'grid.alpha':         0.6,
    'grid.linestyle':     '-',
    'grid.linewidth':     0.5,
    'grid.color':         P['grid'],
    'xtick.color':        P['sub'],
    'ytick.color':        P['sub'],
    'figure.facecolor':   P['bg'],
    'axes.facecolor':     P['bg'],
    'legend.framealpha':  0.95,
    'legend.edgecolor':   P['border'],
    'legend.fontsize':    9.5,
})


def _pct(value: float) -> str:
    return f'\u2212{value:.0f}\u202f%'


def _save(fig, name: str, output_dir: Path) -> None:
    path = output_dir / name
    fig.savefig(path, dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    print(f'  [ok] {name}')
    plt.close(fig)


def _parse_global_sections(file_path: Path) -> list:
    """Parse global.md into (section_name, rule_count, token_count) tuples."""
    sections = []
    current = None
    rules = 0
    tokens = 0
    text = file_path.read_text(encoding='utf-8')
    for line in text.splitlines():
        if line.startswith('## '):
            if current:
                sections.append((current, rules, tokens))
            current = line[3:].strip()
            rules = 0
            tokens = count_tokens(line)
        elif line.startswith('- ') and current:
            rules += 1
            tokens += count_tokens(line)
        elif current and line.strip():
            tokens += count_tokens(line)
    if current:
        sections.append((current, rules, tokens))
    return sections


def _rounded_card(ax, x, y, w, h, facecolor, edgecolor, lw=1.8, **kw):
    """Add a rounded rectangle card to axes (data coords or transform)."""
    patch = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=0.03', facecolor=facecolor,
        edgecolor=edgecolor, linewidth=lw, **kw)
    ax.add_patch(patch)
    return patch


# ===========================================================================
# Chart 1: .claudeignore
# ===========================================================================

def chart_claudeignore(r: ClaudeIgnoreResult, output_dir: Path) -> None:
    fig = plt.figure(figsize=(16, 9))

    # -- Title block (generous top margin) --
    fig.text(0.50, 0.96, '.claudeignore', **FONT_TITLE, ha='center')
    fig.text(0.50, 0.93,
             f'Filtra automaticamente archivos de ruido antes de que Claude los lea',
             **FONT_SUBTITLE, ha='center')

    # Two panels: bar chart (left 55%) + donut (right 45%)
    ax_bar = fig.add_axes([0.06, 0.10, 0.48, 0.76])    # [left, bottom, width, height]
    ax_pie = fig.add_axes([0.60, 0.08, 0.38, 0.78])

    # -- LEFT: Horizontal bar chart --
    files  = r.top_ignored[:6]
    # Show parent/file for disambiguation (e.g. "fastapi/__init__.py")
    def _short_label(path: str) -> str:
        parts = path.replace('\\', '/').split('/')
        return '/'.join(parts[-2:])[:32] if len(parts) >= 2 else parts[-1][:32]
    labels = [_short_label(f.path) for f in files]
    values = [f.tokens for f in files]
    n = len(files)
    bar_colors = plt.cm.Reds(np.linspace(0.25, 0.70, n))

    bars = ax_bar.barh(labels[::-1], values[::-1], color=bar_colors[::-1],
                       edgecolor='white', linewidth=0.8, height=0.62)

    max_val = max(values) if values else 1
    for bar in bars:
        w = bar.get_width()
        # Place label inside bar (right-aligned) to avoid overlaps between rows
        ax_bar.text(w - max_val * 0.02,
                    bar.get_y() + bar.get_height() / 2,
                    f'{int(w):,}',
                    va='center', ha='right',
                    fontsize=9, fontweight='bold', color='white')

    ax_bar.set_xlim(0, max_val * 1.08)
    ax_bar.set_xlabel('Tokens', labelpad=8)
    ax_bar.tick_params(axis='y', labelsize=10)
    ax_bar.set_axisbelow(True)
    ax_bar.grid(axis='x')
    ax_bar.set_title('Top archivos filtrados por .claudeignore',
                     fontsize=13, fontweight='bold', color=P['text'],
                     loc='left', pad=12)

    # Stats line below title
    ax_bar.text(0.0, 1.02,
                f'{r.ignored_files} archivos  \u00b7  {r.ignored_tokens:,} tokens eliminados',
                fontsize=9, color=P['sub'], transform=ax_bar.transAxes)

    # -- RIGHT: Donut chart --
    sizes  = [r.ignored_tokens, r.kept_tokens]
    colors_d = [P['bad_mid'], P['good_mid']]
    wedges, _ = ax_pie.pie(
        sizes, colors=colors_d, startangle=90,
        wedgeprops={'linewidth': 3.5, 'edgecolor': 'white', 'width': 0.48})

    # Center text
    ax_pie.text(0, 0.10, _pct(r.savings_pct),
                ha='center', va='center', fontsize=36,
                fontweight='bold', color=P['bad'])
    ax_pie.text(0, -0.18, 'tokens filtrados',
                ha='center', va='center', fontsize=11, color=P['sub'])

    # Legend below donut
    kept_pct = 100 - r.savings_pct
    legend_labels = [
        f'Filtrado   {r.ignored_tokens:,} tk  ({r.savings_pct:.0f}%)',
        f'Util          {r.kept_tokens:,} tk  ({kept_pct:.0f}%)',
    ]
    legend_handles = [
        mpatches.Patch(color=P['bad_mid'],  label=legend_labels[0]),
        mpatches.Patch(color=P['good_mid'], label=legend_labels[1]),
    ]
    ax_pie.legend(handles=legend_handles, loc='lower center',
                  bbox_to_anchor=(0.5, -0.08), ncol=1, frameon=True,
                  fontsize=10, handlelength=1.5)

    # Total scanned label
    ax_pie.text(0.5, 1.06, f'Total escaneado: {r.total_tokens:,} tokens',
                fontsize=9, color=P['sub'], ha='center',
                transform=ax_pie.transAxes)

    # Project info bottom-left
    fig.text(0.06, 0.02,
             f'Proyecto: {r.project_name}   |   Metodo: {r.token_method}',
             fontsize=8.5, color=P['muted'])

    _save(fig, 'chart_claudeignore.png', output_dir)


# ===========================================================================
# Chart 2: global.md
# ===========================================================================

def chart_global_md(r: GlobalMdResult, output_dir: Path) -> None:
    fig = plt.figure(figsize=(16, 9))

    fig.text(0.50, 0.96, 'global.md', **FONT_TITLE, ha='center')
    fig.text(0.50, 0.93,
             'Tus preferencias y reglas, inyectadas automaticamente en cada conversacion',
             **FONT_SUBTITLE, ha='center')

    if not r.found:
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.75])
        ax.text(0.5, 0.5,
                'global.md no encontrado\n\n'
                'Instala: cp configs/global.md ~/.claude/',
                ha='center', va='center', fontsize=14, color=P['sub'],
                transform=ax.transAxes)
        ax.axis('off')
        _save(fig, 'chart_global_md.png', output_dir)
        return

    sections = _parse_global_sections(r.file_path)
    total_rules = sum(s[1] for s in sections)

    # Layout: left = bar chart (55%), right = coverage cards (45%)
    ax_bar = fig.add_axes([0.06, 0.10, 0.46, 0.76])
    ax_cards = fig.add_axes([0.58, 0.10, 0.40, 0.76])
    ax_cards.set_xlim(0, 10)
    ax_cards.set_ylim(0, 10)
    ax_cards.axis('off')

    # -- LEFT: Section breakdown --
    cat_colors = [P['blue_mid'], P['good_mid'], P['orange_mid'],
                  P['purple'], P['bad_mid'], P['muted']]
    while len(cat_colors) < len(sections):
        cat_colors.append(P['muted'])

    names         = [s[0] for s in sections]
    tok_per_cat   = [s[2] for s in sections]
    rules_per_cat = [s[1] for s in sections]

    bars = ax_bar.barh(
        names[::-1], tok_per_cat[::-1],
        color=[cat_colors[i] for i in range(len(names))][::-1],
        height=0.55, edgecolor='white', linewidth=1.2)

    max_tok = max(tok_per_cat) if tok_per_cat else 1
    for bar, rcount in zip(bars, rules_per_cat[::-1]):
        w = bar.get_width()
        ax_bar.text(w + max_tok * 0.035,
                    bar.get_y() + bar.get_height() / 2,
                    f'{rcount} reglas  \u00b7  {int(w)} tk',
                    va='center', fontsize=9.5, fontweight='bold', color=P['text'])

    ax_bar.set_xlim(0, max_tok * 1.70)
    ax_bar.set_xlabel('Tokens', labelpad=6)
    ax_bar.tick_params(axis='y', labelsize=10)
    ax_bar.set_axisbelow(True)
    ax_bar.grid(axis='x')
    ax_bar.set_title('Contenido de tu global.md',
                     fontsize=13, fontweight='bold', color=P['text'],
                     loc='left', pad=12)
    ax_bar.text(0.0, 1.02,
                f'{total_rules} reglas  \u00b7  {r.tokens:,} tokens  \u00b7  inyeccion automatica',
                fontsize=9, color=P['sub'], transform=ax_bar.transAxes)

    # -- RIGHT: Coverage comparison cards --
    cw, ch = 8.6, 3.2   # card dimensions in data coords (axes is 0-10 x 0-10)
    cx = 0.7             # card left x

    # Card 1: "Con global.md" (top)
    _rounded_card(ax_cards, cx, 5.8, cw, ch,
                  facecolor=P['good_light'], edgecolor=P['good'], lw=2.5)
    ax_cards.text(cx + cw / 2, 8.35, 'Con global.md',
                  ha='center', fontsize=13, fontweight='bold', color=P['good'])
    ax_cards.text(cx + cw / 2, 7.25,
                  f'{CONVS_PER_MONTH} / {CONVS_PER_MONTH}',
                  ha='center', fontsize=38, fontweight='bold', color=P['good'])
    ax_cards.text(cx + cw / 2, 6.30,
                  'conversaciones con tus\npreferencias aplicadas',
                  ha='center', fontsize=9.5, color=P['sub'], linespacing=1.5)

    # Card 2: "Sin global.md" (bottom)
    _rounded_card(ax_cards, cx, 1.5, cw, ch,
                  facecolor=P['bad_light'], edgecolor=P['bad'], lw=2.5)
    ax_cards.text(cx + cw / 2, 4.05, 'Sin global.md',
                  ha='center', fontsize=13, fontweight='bold', color=P['bad'])
    ax_cards.text(cx + cw / 2, 2.95,
                  f'0 / {CONVS_PER_MONTH}',
                  ha='center', fontsize=38, fontweight='bold', color=P['bad'])
    ax_cards.text(cx + cw / 2, 2.00,
                  'debes repetir tus preferencias\nen cada conversacion nueva',
                  ha='center', fontsize=9.5, color=P['sub'], linespacing=1.5)

    # Arrow between cards
    ax_cards.annotate('', xy=(cx + cw / 2, 5.75), xytext=(cx + cw / 2, 4.85),
                      arrowprops=dict(arrowstyle='->', color=P['muted'],
                                      lw=2, mutation_scale=18))

    # Project info
    fig.text(0.06, 0.02,
             f'{r.tokens:,} tokens  |  Metodo: {TOKEN_METHOD}',
             fontsize=8.5, color=P['muted'])

    _save(fig, 'chart_global_md.png', output_dir)


# ===========================================================================
# Chart 3: smart-init
# ===========================================================================

def chart_smart_init(r: SmartInitResult, output_dir: Path) -> None:
    fig = plt.figure(figsize=(16, 9))

    fig.text(0.50, 0.96, 'smart-init / CLAUDE.md', **FONT_TITLE, ha='center')
    fig.text(0.50, 0.93,
             'Genera un CLAUDE.md compacto que reemplaza multiples archivos de discovery',
             **FONT_SUBTITLE, ha='center')

    if not r.discovery_files:
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.75])
        ax.text(0.5, 0.5, 'No se encontraron archivos de discovery',
                ha='center', va='center', fontsize=14, color=P['sub'],
                transform=ax.transAxes)
        ax.axis('off')
        _save(fig, 'chart_smart_init.png', output_dir)
        return

    # Layout: left = before/after bars (55%), right = file breakdown (45%)
    ax_bars = fig.add_axes([0.06, 0.10, 0.44, 0.76])
    ax_info = fig.add_axes([0.56, 0.10, 0.42, 0.76])
    ax_info.set_xlim(0, 10)
    ax_info.set_ylim(0, 10)
    ax_info.axis('off')

    # -- LEFT: Before / After horizontal bars --
    n_files = len(r.discovery_files)
    file_colors = plt.cm.Oranges(np.linspace(0.30, 0.75, n_files))

    # Order: "Con" at bottom (index 0), "Sin" at top (index 1) → before on top
    bar_labels = ['Con\nCLAUDE.md', 'Sin\nCLAUDE.md']
    bar_values = [r.claude_md_tokens, r.discovery_tokens]
    bar_colors_main = [P['good_mid'], P['orange_mid']]

    bars = ax_bars.barh(bar_labels, bar_values, color=bar_colors_main,
                        height=0.50, edgecolor='white', linewidth=1.5)

    max_v = r.discovery_tokens
    for bar in bars:
        w = bar.get_width()
        ax_bars.text(w + max_v * 0.025,
                     bar.get_y() + bar.get_height() / 2,
                     f'{int(w):,} tokens',
                     va='center', fontsize=12, fontweight='bold', color=P['text'])

    ax_bars.set_xlim(0, max_v * 1.40)
    ax_bars.set_xlabel('Tokens por conversacion nueva', labelpad=8)
    ax_bars.tick_params(axis='y', labelsize=11)
    ax_bars.set_axisbelow(True)
    ax_bars.grid(axis='x')
    ax_bars.set_title(
        f'Antes vs Despues: {n_files} archivos \u2192 1 CLAUDE.md',
        fontsize=13, fontweight='bold', color=P['text'], loc='left', pad=12)

    # Savings badge between bars
    mid_y = 0.5
    mid_x = (r.discovery_tokens + r.claude_md_tokens) / 2
    ax_bars.annotate(
        f'{_pct(r.savings_pct)}',
        xy=(mid_x, mid_y), fontsize=22, fontweight='bold',
        color=P['good'], ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=P['good_light'],
                  edgecolor=P['good'], linewidth=2.5, alpha=0.97))

    # -- RIGHT: File breakdown table --
    ax_info.set_title('Desglose de archivos',
                      fontsize=13, fontweight='bold', color=P['text'],
                      loc='left', pad=12)

    # Header
    y_pos = 9.0
    ax_info.text(0.4, y_pos, 'Sin CLAUDE.md, Claude lee:',
                 fontsize=10.5, color=P['sub'], fontweight='bold')
    y_pos -= 0.55

    # File list
    for i, f in enumerate(r.discovery_files):
        color = file_colors[i] if i < len(file_colors) else P['sub']
        # Color dot
        ax_info.add_patch(mpatches.Circle(
            (0.7, y_pos), 0.22, facecolor=color,
            edgecolor='white', linewidth=1, transform=ax_info.transData))
        # File name
        ax_info.text(1.3, y_pos, f.path,
                     fontsize=10, color=P['text'], va='center')
        # Token count
        ax_info.text(9.2, y_pos, f'{f.tokens:,} tk',
                     fontsize=10, color=P['sub'], va='center', ha='right',
                     fontweight='bold')
        y_pos -= 0.70

    # Separator
    y_pos -= 0.15
    ax_info.plot([0.4, 9.2], [y_pos, y_pos], color=P['border'],
                 linewidth=1, linestyle='-')
    y_pos -= 0.45

    # Total discovery
    ax_info.text(1.3, y_pos, 'Total discovery:',
                 fontsize=10.5, color=P['orange'], fontweight='bold', va='center')
    ax_info.text(9.2, y_pos, f'{r.discovery_tokens:,} tk',
                 fontsize=10.5, color=P['orange'], fontweight='bold',
                 va='center', ha='right')
    y_pos -= 0.90

    # CLAUDE.md result
    ax_info.add_patch(mpatches.Circle(
        (0.7, y_pos), 0.22, facecolor=P['good_mid'],
        edgecolor='white', linewidth=1, transform=ax_info.transData))
    src = r.claude_md_path.name if r.claude_md_path else 'SKILL.md'
    ax_info.text(1.3, y_pos, f'CLAUDE.md ({src})',
                 fontsize=10, color=P['good'], fontweight='bold', va='center')
    ax_info.text(9.2, y_pos, f'{r.claude_md_tokens:,} tk',
                 fontsize=10, color=P['good'], fontweight='bold',
                 va='center', ha='right')
    y_pos -= 1.10

    # Explanation card
    card_h = 1.8
    _rounded_card(ax_info, 0.2, y_pos - card_h, 9.2, card_h,
                  facecolor=P['good_light'], edgecolor=P['good'], lw=1.5)
    ax_info.text(4.8, y_pos - card_h / 2,
                 f'smart-init genera 1 archivo compacto que reemplaza\n'
                 f'{n_files} archivos de discovery \u2192 '
                 f'Ahorro: {r.savings_tokens:,} tk ({r.savings_pct:.0f}%)',
                 ha='center', va='center', fontsize=9.5,
                 color=P['good'], fontweight='bold', linespacing=1.6)

    # Project info
    fig.text(0.06, 0.02,
             f'Proyecto: {r.project_name}   |   Metodo: {r.token_method}',
             fontsize=8.5, color=P['muted'])

    _save(fig, 'chart_smart_init.png', output_dir)


# ===========================================================================
# Chart 4: Summary - Impacto combinado
# ===========================================================================
#
# Clean infographic: 3 config cards + 1 total card, vertically stacked.
# All positions computed from a uniform grid so nothing overlaps.

# Layout constants (axes fraction coords, y=0 bottom, y=1 top)
_CH  = 0.150   # config card height
_TH  = 0.205   # total card height
_GAP = 0.035   # gap between config cards
_BH  = 0.016   # progress bar height
_BADGE_X = 0.87


def _draw_config_card(ax, yc: float,
                      title: str, color: str, light: str,
                      pct_text: str, before_val: str, after_val: str,
                      detail: str, bar_pct: float) -> None:
    """Draw one config-savings card. yc = vertical center in axes coords."""
    # Card background
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.04, yc - _CH / 2), 0.92, _CH,
        boxstyle='round,pad=0.016', facecolor=light,
        edgecolor=color, linewidth=2.0,
        transform=ax.transAxes, clip_on=False))

    row_top = yc + _CH * 0.30    # title + before/after
    row_mid = yc - _CH * 0.02    # detail
    row_bot = yc - _CH * 0.32    # bar

    # Title (left)
    ax.text(0.07, row_top, title,
            fontsize=13, fontweight='bold', color=color,
            transform=ax.transAxes, va='center')

    # Before -> After (center-right of title row)
    ax.text(0.54, row_top, f'{before_val}  \u2192  {after_val}',
            fontsize=10, fontweight='bold', color=P['text'],
            transform=ax.transAxes, va='center', ha='center')

    # Detail
    ax.text(0.07, row_mid, detail,
            fontsize=8.5, color=P['sub'],
            transform=ax.transAxes, va='center')

    # Progress bar
    bar_x, bar_w = 0.07, 0.62
    ax.add_patch(mpatches.FancyBboxPatch(
        (bar_x, row_bot - _BH / 2), bar_w, _BH,
        boxstyle='round,pad=0.002', facecolor=P['grid'],
        edgecolor=P['border'], linewidth=0.5,
        transform=ax.transAxes, clip_on=False))
    filled = bar_w * min(bar_pct / 100.0, 1.0)
    if filled > 0.003:
        ax.add_patch(mpatches.FancyBboxPatch(
            (bar_x, row_bot - _BH / 2), filled, _BH,
            boxstyle='round,pad=0.002', facecolor=color,
            edgecolor='none', linewidth=0,
            transform=ax.transAxes, clip_on=False))
    ax.text(bar_x + bar_w + 0.012, row_bot, f'{bar_pct:.0f}%',
            fontsize=8, color=color, fontweight='bold',
            transform=ax.transAxes, va='center')

    # Big badge (right)
    ax.text(_BADGE_X, yc, pct_text,
            fontsize=18, fontweight='bold', color=color,
            transform=ax.transAxes, va='center', ha='center',
            bbox=dict(boxstyle='round,pad=0.28', facecolor='white',
                      edgecolor=color, linewidth=2, alpha=0.95))


def chart_summary(r1: ClaudeIgnoreResult, r2: GlobalMdResult,
                  r3: SmartInitResult, output_dir: Path) -> None:
    # -- Numbers --
    pref_tokens   = r2.tokens if r2.found else 0
    total_without = r1.kept_tokens + r1.ignored_tokens + r3.discovery_tokens + pref_tokens
    total_with    = r1.kept_tokens + r3.claude_md_tokens
    total_saved   = total_without - total_with
    saving_pct    = total_saved / total_without * 100 if total_without else 0
    monthly_saved = total_saved * CONVS_PER_MONTH

    sections    = _parse_global_sections(r2.file_path) if r2.found else []
    total_rules = sum(s[1] for s in sections)

    # -- Card vertical centres --
    # First card top edge at y=0.895 (below subtitle at 0.93)
    _GAP_TOTAL = 0.062   # larger gap before the total card for visual separation
    yc1 = 0.895 - _CH / 2
    yc2 = yc1 - _CH - _GAP
    yc3 = yc2 - _CH - _GAP
    yc4 = yc3 - _CH / 2 - _GAP_TOTAL - _TH / 2

    # -- Figure --
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.50, 0.97, 'Claude Pro Optimizer', **FONT_TITLE,
            ha='center', transform=ax.transAxes)
    ax.text(0.50, 0.94, 'Impacto real medido sobre tu proyecto',
            **FONT_SUBTITLE, ha='center', transform=ax.transAxes)

    # -- Three config cards --
    _draw_config_card(
        ax, yc=yc1,
        title='.claudeignore',
        color=P['bad'], light=P['bad_light'],
        pct_text=_pct(r1.savings_pct),
        before_val=f'{r1.total_tokens:,} tk',
        after_val=f'{r1.kept_tokens:,} tk',
        detail=f'Filtra {r1.ignored_files} archivos de ruido (.venv, __pycache__, lockfiles...)',
        bar_pct=r1.savings_pct)

    _draw_config_card(
        ax, yc=yc2,
        title='global.md',
        color=P['blue'], light=P['blue_light'],
        pct_text=f'{total_rules}\nreglas',
        before_val=f'{pref_tokens:,} tk/conv manual',
        after_val='0 tk (auto)',
        detail=f'{pref_tokens} tokens de preferencias inyectados en cada nueva conversacion',
        bar_pct=100)

    _draw_config_card(
        ax, yc=yc3,
        title='smart-init / CLAUDE.md',
        color=P['orange'], light=P['orange_light'],
        pct_text=_pct(r3.savings_pct),
        before_val=f'{r3.discovery_tokens:,} tk discovery',
        after_val=f'{r3.claude_md_tokens:,} tk CLAUDE.md',
        detail=f'Reemplaza {len(r3.discovery_files)} archivos de discovery por 1 CLAUDE.md compacto',
        bar_pct=r3.savings_pct)

    # -- Total card --
    row_t1 = yc4 + _TH * 0.32    # header
    row_t2 = yc4 + _TH * 0.08    # before -> after
    row_t3 = yc4 - _TH * 0.12    # bar
    row_t4 = yc4 - _TH * 0.34    # monthly

    ax.add_patch(mpatches.FancyBboxPatch(
        (0.04, yc4 - _TH / 2), 0.92, _TH,
        boxstyle='round,pad=0.018', facecolor=P['good_light'],
        edgecolor=P['good'], linewidth=3,
        transform=ax.transAxes, clip_on=False))

    ax.text(0.07, row_t1, 'AHORRO TOTAL POR SESION',
            fontsize=11, fontweight='bold', color=P['good'],
            transform=ax.transAxes, va='center')

    ax.text(0.07, row_t2,
            f'{total_without:,} tk  \u2192  {total_with:,} tk   '
            f'({total_saved:,} tokens ahorrados)',
            fontsize=12, fontweight='bold', color=P['text'],
            transform=ax.transAxes, va='center')

    # Wide bar
    total_bx, total_bw, total_bh = 0.07, 0.62, 0.020
    ax.add_patch(mpatches.FancyBboxPatch(
        (total_bx, row_t3 - total_bh / 2), total_bw, total_bh,
        boxstyle='round,pad=0.002', facecolor='white',
        edgecolor=P['border'], linewidth=0.7,
        transform=ax.transAxes, clip_on=False))
    filled = total_bw * min(saving_pct / 100.0, 1.0)
    ax.add_patch(mpatches.FancyBboxPatch(
        (total_bx, row_t3 - total_bh / 2), filled, total_bh,
        boxstyle='round,pad=0.002', facecolor=P['good_mid'],
        edgecolor='none', linewidth=0,
        transform=ax.transAxes, clip_on=False))
    ax.text(total_bx + total_bw + 0.012, row_t3,
            f'{saving_pct:.0f}% optimizado',
            fontsize=9, color=P['good'], fontweight='bold',
            transform=ax.transAxes, va='center')

    ax.text(0.07, row_t4,
            f'~{CONVS_PER_MONTH} conv/mes  \u2192  {monthly_saved:,} tokens ahorrados al mes',
            fontsize=9.5, color=P['sub'],
            transform=ax.transAxes, va='center')

    # Big badge
    ax.text(_BADGE_X, yc4, _pct(saving_pct),
            fontsize=28, fontweight='bold', color=P['good'],
            transform=ax.transAxes, va='center', ha='center',
            bbox=dict(boxstyle='round,pad=0.32', facecolor='white',
                      edgecolor=P['good'], linewidth=2.5, alpha=0.97))

    # Project info
    ax.text(0.07, 0.02,
            f'Proyecto: {r1.project_name}   |   Metodo: {r1.token_method}',
            fontsize=8.5, color=P['muted'],
            transform=ax.transAxes)

    _save(fig, 'chart_summary.png', output_dir)


# ===========================================================================
# Main
# ===========================================================================

def main(project: Path, ignore_file: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f'\nMidiendo datos reales de \'{project.name}\'...')

    r1 = analyze_claudeignore(project, ignore_file)
    r2 = analyze_global_md()
    r3 = analyze_smart_init(project)

    print(f'  .claudeignore : {r1.total_tokens:,} -> {r1.kept_tokens:,} tk  (-{r1.savings_pct:.0f}%)')
    print(f'  global.md     : {r2.tokens:,} tk  ({sum(s[1] for s in _parse_global_sections(r2.file_path)) if r2.found else 0} reglas)')
    print(f'  smart-init    : {r3.discovery_tokens:,} -> {r3.claude_md_tokens:,} tk  (-{r3.savings_pct:.0f}%)')
    print(f'\nGenerando graficos en {output_dir} ...\n')

    chart_claudeignore(r1, output_dir)
    chart_global_md(r2, output_dir)
    chart_smart_init(r3, output_dir)
    chart_summary(r1, r2, r3, output_dir)

    print(f'\nListos 4 graficos en {output_dir}')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Genera graficos de impacto')
    parser.add_argument('--project', type=Path, default=Path('examples/demo-fastapi'))
    parser.add_argument('--ignore-file', type=Path, default=None)
    parser.add_argument('--output-dir', type=Path, default=None)
    args = parser.parse_args()

    project = args.project.resolve()
    ignore  = args.ignore_file or find_ignore_file(project)
    out_dir = args.output_dir or (project / 'charts')

    main(project, ignore, out_dir)
