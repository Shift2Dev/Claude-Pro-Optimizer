# Contribuir a Claude Pro Optimizer

¡Gracias por tu interés en contribuir! 🎉

## 🤝 Cómo Contribuir

### 1. Fork y Clone

```bash
# Fork en GitHub, luego:
git clone https://github.com/tu-usuario/claude-pro-optimizer.git
cd claude-pro-optimizer
```

### 2. Crear Branch

```bash
git checkout -b feat/amazing-feature
# O
git checkout -b fix/bug-description
# O
git checkout -b docs/improvement
```

### 3. Hacer Cambios

- Mantén el estilo existente
- Configs en `configs/`
- Docs en `docs/`
- Ejemplos en `examples/`

### 4. Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: add new optimization skill"
git commit -m "fix: correct smart-init detection"
git commit -m "docs: improve setup guide"
```

**Prefijos:**
- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` cambios en documentación
- `refactor:` refactoring sin cambios funcionales
- `chore:` tareas de mantenimiento

### 5. Push y PR

```bash
git push origin feat/amazing-feature
```

Luego abre un Pull Request en GitHub.

## 💡 Ideas de Contribución

### Skills Útiles

¿Tienes un skill custom que sea útil? Compártelo:

```
configs/skills/tu-skill/
└── SKILL.md
```

### Mejoras al .claudeignore

¿Tu stack necesita patrones específicos? Añádelos con comentarios:

```gitignore
# Framework X specific
.framework-cache/
*.framework-temp
```

### Ejemplos Reales

¿Usaste el optimizer de forma interesante? Documéntalo:

```
examples/caso-uso-X.md
```

### Optimizaciones Nuevas

¿Descubriste nueva técnica de eficiencia? Agrégala a:

```
docs/token-optimization-theory.md
```

## 📋 Guidelines

### Configs

- Comentar decisiones no-obvias
- Mantener formato consistente
- Testear antes de commitear

### Documentación

- Español para docs generales
- Inglés para código/comentarios técnicos
- Ejemplos concretos sobre teoría abstracta
- Markdown lint-free

### Skills

- Nombre descriptivo y corto
- Description clara del propósito
- Smart defaults, no placeholders
- Instrucciones específicas

## 🐛 Reportar Bugs

Usa [GitHub Issues](../../issues) con:

**Template:**

```markdown
## Descripción
[Qué no funciona]

## Reproducir
1. [Paso 1]
2. [Paso 2]
3. [Error aparece]

## Esperado
[Qué debería pasar]

## Entorno
- OS: [Windows 11 / macOS 14 / Ubuntu 22.04]
- Claude Desktop: [versión]
- Config: [qué configs tienes instaladas]
```

## 💭 Sugerir Features

**Template:**

```markdown
## Problema
[Qué problema resuelve]

## Solución Propuesta
[Tu idea]

## Alternativas
[Otras opciones consideradas]

## Beneficio
[Por qué es valioso]
```

## ✅ Checklist PR

Antes de abrir PR, verifica:

- [ ] Código/configs funcionan localmente
- [ ] Docs actualizadas si necesario
- [ ] Commits siguen Conventional Commits
- [ ] Branch actualizado con main
- [ ] Descripción clara del cambio

## 🎯 Código de Conducta

- Sé respetuoso y constructivo
- Acepta críticas con apertura
- Enfócate en el código/configs, no en las personas
- Ayuda a crear ambiente de aprendizaje
- Asume buena intención en otros contributors

## 🌟 Reconocimiento

Contributors serán mencionados en:
- README.md (sección Contributors)
- CHANGELOG.md
- Commit history

## 🆘 ¿Necesitas Ayuda?

- Pregunta en [Discussions](../../discussions)
- Abre [Issue](../../issues) con tu duda
- Tag con `question` label

## 📚 Recursos

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Claude Documentation](https://docs.anthropic.com/claude/docs)

---

**¡Toda contribución, grande o pequeña, es valiosa!** 🚀

¿Dudas? Abre un issue. ¿Ideas? Abre una discussion. ¿Código listo? Abre un PR.

**Gracias por ayudar a mejorar Claude Pro Optimizer.** 🎉
