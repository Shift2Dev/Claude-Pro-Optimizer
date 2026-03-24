# Setup Guide

Guía paso a paso para instalar y configurar Claude Pro Optimizer.

## 📋 Requisitos

- Claude Desktop instalado
- Plan Claude Pro (recomendado)
- Terminal (PowerShell en Windows, bash en Mac/Linux)

## 🚀 Instalación

### Windows (PowerShell)

```powershell
# 1. Navegar a tu directorio .claude
cd ~\.claude

# 2. Crear carpeta skills si no existe
New-Item -ItemType Directory -Force -Path skills

# 3. Copiar configuraciones
# Descarga el repo y ejecuta:
Copy-Item -Path C:\ruta\al\repo\configs\global.md -Destination . -Force
Copy-Item -Path C:\ruta\al\repo\configs\.claudeignore -Destination . -Force
Copy-Item -Path C:\ruta\al\repo\configs\skills\smart-init -Destination skills\ -Recurse -Force

# 4. Verificar
ls
```

### Mac/Linux (bash)

```bash
# 1. Navegar a tu directorio .claude
cd ~/.claude

# 2. Crear carpeta skills si no existe
mkdir -p skills

# 3. Copiar configuraciones
cp /ruta/al/repo/configs/global.md .
cp /ruta/al/repo/configs/.claudeignore .
cp -r /ruta/al/repo/configs/skills/smart-init skills/

# 4. Verificar
ls -la
```

## ✅ Verificación

Después de instalar, tu directorio `~/.claude` debería verse así:

```
.claude/
├── global.md
├── .claudeignore
└── skills/
    └── smart-init/
        └── SKILL.md
```

## 🎯 Primer Uso

### 1. Abrir un proyecto

Abre cualquier proyecto en Claude Desktop.

### 2. Ejecutar smart-init

En el chat, escribe:

```
/init
```

### 3. Ver resultado

Claude analizará tu proyecto y generará `.claude/CLAUDE.md` automáticamente.

```powershell
# Ver el archivo generado
cat .claude/CLAUDE.md
```

### 4. Editar si necesario

El archivo está listo para usar, pero puedes personalizarlo:

```powershell
code .claude/CLAUDE.md
```

## 🔧 Personalización

### Modificar global.md

Edita `~/.claude/global.md` para ajustar:

```markdown
## Tools
- OS: [Tu sistema operativo]
- Terminal: [Tu terminal preferida]
- Editor: [Tu editor]

## Code Style
- [Tus preferencias de código]
```

### Modificar .claudeignore

Añade patrones específicos de tu stack:

```
# Ejemplo: Ignorar archivos Next.js
.next/
out/

# Ejemplo: Ignorar archivos de Rust
target/debug/
target/release/
```

### Crear Skills Propios

1. Crea carpeta en `~/.claude/skills/tu-skill/`
2. Crea `SKILL.md` con estructura:

```markdown
---
name: tu-skill
description: Qué hace tu skill
---

# Tu Skill

Instrucciones de tu skill...
```

Ver [Creating Skills](creating-skills.md) para más detalles.

## 🐛 Troubleshooting

### Skill no funciona

**Problema:** `/init` no hace nada

**Solución:**
1. Verifica que el archivo está en `~/.claude/skills/smart-init/SKILL.md`
2. Reinicia Claude Desktop
3. Intenta de nuevo

### Configuración no se aplica

**Problema:** Claude no usa mi global.md

**Solución:**
1. Verifica ruta: `~/.claude/global.md`
2. Chequea formato Markdown válido
3. Reinicia Claude Desktop

### Smart-init genera mal el archivo

**Problema:** CLAUDE.md tiene placeholders

**Solución:**
1. Verifica que tu proyecto tiene `package.json` o `pyproject.toml`
2. Asegúrate que hay archivos de código en `src/` o similar
3. Reporta un issue con ejemplo del proyecto

## 💡 Tips

### Token Efficiency

- Usa `/btw` para preguntas cortas que no necesitan contexto
- Usa `/compact` cuando el contexto se llene
- Revisa periódicamente `.claudeignore` y añade ruido nuevo

### Workflow Óptimo

1. **Nuevo proyecto:** `/init` inmediatamente
2. **Proyecto existente:** Añade `.claudeignore` primero
3. **Equipos:** Comparte tus `.claude/` configs en el repo

### Best Practices

- Commitea `.claude/CLAUDE.md` en tu repo
- NO commitees `global.md` (es personal)
- Ajusta smart-init defaults a tu stack preferido

## 📚 Siguiente Paso

- Lee [Token Optimization Theory](token-optimization-theory.md)
- Ve ejemplos en [Workflow Demo](../examples/workflow-demo.md)
- Aprende a crear skills en [Creating Skills](creating-skills.md)

## 🆘 Soporte

¿Problemas? Abre un [issue](../../issues) con:
- Tu OS y versión de Claude Desktop
- Contenido de tu config que falla
- Pasos para reproducir el problema

---

**Happy optimizing! 🚀**
