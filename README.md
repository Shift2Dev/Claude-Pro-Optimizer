# Claude Pro Optimizer

> Setup profesional para maximizar eficiencia en Claude Desktop y Claude Pro

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 El Problema

Claude Pro tiene límites de mensajes diarios. Cada token cuenta.

**Prompts ineficientes = menos conversaciones útiles por día.**

## 💡 La Solución

Sistema de configuración optimizado para Claude Desktop que:

- ✅ **Reduce tokens por prompt** mediante configuración global
- ✅ **Auto-genera project configs** con el skill `smart-init`
- ✅ **Optimiza lectura de archivos** con `.claudeignore` balanceado
- ✅ **Maximiza mensajes útiles** de tu plan Pro

## 📊 Resultados

**Antes:**
- Setup manual de proyectos: ~15 minutos
- Prompts largos e ineficientes
- Claude lee archivos innecesarios
- Llegas al límite rápido

**Después:**
- Setup automático: <30 segundos (smart-init)
- Prompts concisos y claros
- Solo lee archivos relevantes
- Más conversaciones útiles por día

## 🚀 Quick Start

### 1. Instalar Configuraciones

```bash
# Copiar configs a tu directorio .claude
cp configs/global.md ~/.claude/
cp configs/.claudeignore ~/.claude/
cp -r configs/skills/smart-init ~/.claude/skills/
```

### 2. Usar Smart-Init

En cualquier proyecto, escribe en Claude Desktop:

```
/init
```

El skill analizará tu codebase y generará automáticamente `.claude/CLAUDE.md` optimizado.

### 3. Verificar

```bash
# Ver tu nueva configuración
cat .claude/CLAUDE.md
```

## 📊 Demos Visuales

Todos los números son medidos en tiempo real leyendo los archivos reales de configuración y el filesystem. Sin estimaciones.

![Resumen de impacto total — proyecto FastAPI real](examples/demo-fastapi/charts/chart_summary.png)

Cada tool demuestra el impacto de uno de los 3 configs:

| Config | Qué mide |
|---|---|
| `.claudeignore` | Tokens filtrados del filesystem (scan real del proyecto) |
| `global.md` | Tokens inyectados automáticamente × conversaciones/mes |
| `smart-init` | Tokens de "discovery" reemplazados por un CLAUDE.md compacto |

### Vista previa por config

![.claudeignore — tokens filtrados](examples/demo-fastapi/charts/chart_claudeignore.png)
![global.md — ahorro mensual acumulado](examples/demo-fastapi/charts/chart_global_md.png)
![smart-init — discovery vs CLAUDE.md](examples/demo-fastapi/charts/chart_smart_init.png)

> Proyecto de ejemplo: [demo-fastapi](examples/demo-fastapi/) — FastAPI + SQLAlchemy + pytest

### Medir savings en terminal

```bash
# Analiza directorio actual
python tools/token_analyzer.py

# Analiza cualquier proyecto
python tools/token_analyzer.py /ruta/a/tu/proyecto
```

### Ver comparativa interactiva

```bash
python tools/visual_comparison.py --project /ruta/a/tu/proyecto
```

### Generar gráficos PNG

```bash
pip install matplotlib numpy
python tools/generate_charts.py --project /ruta/a/tu/proyecto
```

Crea 3 gráficos, uno por config:
- `chart_claudeignore.png` - tokens filtrados y distribución del contexto
- `chart_global_md.png` - ahorro mensual acumulado por conversación
- `chart_smart_init.png` - discovery files vs CLAUDE.md por conversación

## 📂 Qué Incluye

### Configs Principales

- **`global.md`** - Preferencias personales y optimización de tokens
  - Español/inglés según contexto
  - Principios de código funcional
  - Token efficiency rules
  - Workflow optimizado

- **`.claudeignore`** - Gitignore balanceado
  - Bloquea ruido (node_modules, logs, cache)
  - Permite archivos build cuando son necesarios
  - Optimizado para reducir contexto innecesario

- **`smart-init/`** - Skill de auto-setup
  - Detecta stack automáticamente
  - Genera CLAUDE.md completo
  - Extrae comandos de package.json/pyproject.toml
  - Zero placeholders, 100% funcional

### Tools Opcionales

- **`prompt_optimizer.py`** - Script Python para analizar y comprimir prompts
- **`context_manager.py`** - Gestión de contexto en conversaciones largas

## 🎓 Guías

- [Setup Guide](docs/setup-guide.md) - Cómo instalar paso a paso
- [Token Optimization](docs/token-optimization-theory.md) - Principios de eficiencia
- [Creating Skills](docs/creating-skills.md) - Guía para crear tus propios skills
- [Workflow Demo](examples/workflow-demo.md) - Ejemplos de uso real

## 💪 Casos de Uso

### Para Developers

- Setup instantáneo de proyectos nuevos
- Configuración consistente entre proyectos
- Menos tiempo configurando, más tiempo desarrollando

### Para Usuarios de Claude Pro

- Maximizar mensajes diarios
- Prompts más eficientes
- Mejor aprovechamiento del plan

### Para Equipos

- Configuración estándar compartida
- Onboarding más rápido
- Best practices automáticas

## 🛠️ Tech Stack

- **Config**: Markdown, Custom Skills
- **Tools**: Python 3.8+ (opcional)
- **Platform**: Claude Desktop / Claude.ai

## 📝 Filosofía

### Principios de Diseño

1. **Token Efficiency First**
   - Cada token cuenta en Claude Pro
   - Optimizar sin perder claridad
   - Batching de operaciones relacionadas

2. **Automation Over Manual**
   - Auto-detectar en vez de preguntar
   - Generar en vez de plantillas vacías
   - Smart defaults sobre configuración manual

3. **Balanced Ignorance**
   - Ignorar ruido (logs, cache, node_modules)
   - Leer lo necesario (build/, dist/ cuando relevante)
   - Contextual, no absoluto

## 🤝 Contribuir

¿Tienes un skill útil? ¿Mejoras al gitignore? ¿Nuevas estrategias de optimización?

1. Fork el repo
2. Crea tu feature branch (`git checkout -b feat/amazing-skill`)
3. Commit con convención (`git commit -m 'feat: add amazing skill'`)
4. Push y abre PR

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## ⚠️ Disclaimer

Este es mi setup personal que uso diariamente y comparto con la comunidad. 

Las optimizaciones están basadas en:
- Uso real en proyectos Python/TypeScript
- Experiencia con Claude Desktop/Pro
- Principios de token efficiency

**Recomendación:** Prueba y ajusta según tu stack y preferencias.

## 📜 License

MIT © 2026 Iván Díaz

---

**¿Útil?** Dale ⭐ y comparte con otros usuarios de Claude

**¿Preguntas?** Abre un [issue](../../issues)

**¿Mejoras?** Los PRs son bienvenidos 🚀
