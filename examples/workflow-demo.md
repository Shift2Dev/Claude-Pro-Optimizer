# Workflow Demo

Ejemplos reales de cómo usar Claude Pro Optimizer en tu día a día.

## 🚀 Caso 1: Setup de Proyecto Nuevo

### Situación

Inicias un nuevo proyecto FastAPI.

### Sin Optimización (15 minutos)

```
1. "Hola Claude, voy a crear un proyecto nuevo con FastAPI..."
2. Crear estructura manual
3. "Ahora necesito configuración de pytest..."
4. "¿Qué comandos debo usar para...?"
5. "Cómo configuro el linting..."
6. [15 mensajes más configurando]
```

**Tiempo:** ~15 minutos  
**Mensajes usados:** ~20

### Con Optimización (30 segundos)

```
# En tu proyecto vacío
/init
```

**Output:**
```
✅ Generated .claude/CLAUDE.md

Detected:
- Stack: Python 3.13 + FastAPI
- Tests: pytest setup detected
- Commands: 5 scripts extracted from pyproject.toml
- Linting: ruff configured

Ready to use!
```

**Tiempo:** 30 segundos  
**Mensajes usados:** 1

---

## 💻 Caso 2: Debugging

### Situación

Tienes un error en tu código.

### ❌ Ineficiente (5 mensajes)

```
1. "Hola Claude, tengo un problema en mi código"
2. [Claude pregunta qué código]
3. [Pegas 500 líneas]
4. [Claude pregunta qué error]
5. "Ah sí, es NameError en línea 42"
```

**Tokens gastados:** ~3,000

### ✅ Eficiente (1 mensaje)

```
Error en src/main.py línea 42:
NameError: name 'process_data' is not defined

Context: función `run_pipeline()`
```

**Tokens gastados:** ~100

**Ahorro:** 96%

---

## 🔧 Caso 3: Refactoring

### Situación

Necesitas refactorizar código legacy.

### ❌ Ineficiente

```
1. "Por favor revisa este archivo completo"
   [Pega 1000 líneas]
   
2. "Ahora mejóralo"
   [Claude pregunta qué mejorar]
   
3. "Todo, hazlo mejor"
   [Resultado genérico]
```

### ✅ Eficiente

```
Refactor src/legacy.py:
- Extraer validación a función separada (líneas 50-80)
- Convertir clase DataProcessor a funciones puras
- Añadir type hints

Focus: mantenibilidad, no performance
```

**Resultado:** Refactor específico y útil.

---

## 📝 Caso 4: Documentation

### Situación

Documentar función compleja.

### ❌ Verbose

```
"Hola Claude, necesito que me ayudes a documentar esta función.
Es muy importante que la documentación sea clara y completa,
con todos los parámetros explicados, el return value, ejemplos
de uso, y también casos edge. La función se llama calculate_metrics
y está en el archivo analytics.py..."
```

**Tokens:** ~150

### ✅ Conciso

```
Documenta `calculate_metrics()` en analytics.py:
- Docstring con params, return, ejemplos
- Type hints
```

**Tokens:** ~30

**Ahorro:** 80%

---

## 🎯 Caso 5: Code Review

### Situación

Revisar PR antes de merge.

### Sin .claudeignore (MALO)

```
/view .  # Lee TODO el proyecto
```

**Archivos leídos:** 5,000+  
**Contexto:** Lleno inmediatamente  
**Resultado:** "Context limit exceeded"

### Con .claudeignore (BIEN)

```
/view src/
/view tests/
```

**Archivos leídos:** 50  
**Contexto:** 30%  
**Resultado:** Review útil

---

## 🔄 Caso 6: Conversación Larga

### Situación

Debugging session de 30 mensajes.

### Sin Gestión

```
Mensaje 25: "Context almost full"
Mensaje 26: [Error, no puede procesar]
```

**Solución:** Nueva conversación, perder contexto.

### Con /compact

```
Mensaje 10: /compact
# Continúa...

Mensaje 20: /compact
# Continúa...

Mensaje 30: Debugging completado con contexto intacto
```

**Resultado:** Conversación fluida sin límites.

---

## 💡 Caso 7: Quick Questions

### Situación

Pregunta rápida sin contexto necesario.

### ❌ Normal

```
"¿Cómo se hace un loop en Python?"
# Usa contexto completo de conversación actual
```

### ✅ Con /btw

```
/btw ¿Cómo se hace un loop en Python?
# NO usa contexto, respuesta rápida
```

**Ahorro:** No contamina conversación actual.

---

## 🎨 Caso 8: Batch Operations

### Situación

Crear múltiples funciones relacionadas.

### ❌ Secuencial (3 mensajes)

```
1. "Crea función suma"
2. "Ahora función resta"
3. "Ahora función multiplica"
```

**Tokens:** ~300  
**Tiempo:** 3x latencia

### ✅ Batched (1 mensaje)

```
Crea módulo math_ops.py:
- suma(a, b)
- resta(a, b)
- multiplica(a, b)

Type hints, docstrings, tests
```

**Tokens:** ~100  
**Tiempo:** 1x latencia

---

## 📊 Comparativa de Día Típico

### Antes de Optimizar

```
09:00 - Setup proyecto (20 mensajes)
10:30 - Debugging (15 mensajes)
12:00 - Code review (25 mensajes)
14:00 - Hit límite diario ❌
```

**Total:** 60 mensajes, límite alcanzado

### Después de Optimizar

```
09:00 - /init (1 mensaje)
09:30 - Debugging eficiente (5 mensajes)
10:00 - Code review con .claudeignore (8 mensajes)
11:00 - Features nuevas (20 mensajes)
14:00 - Refactoring (15 mensajes)
16:00 - Documentation (10 mensajes)
17:00 - Todavía con margen ✅
```

**Total:** ~60 mensajes, mucho más productivos

---

## 🎯 Template de Mensaje Eficiente

```markdown
[Acción específica] [Ubicación precisa]:
- [Requirement 1]
- [Requirement 2]

[Constraint importante si existe]
```

**Ejemplos:**

```
Fix bug src/api.py línea 89:
- IndexError en loop
- Manejar lista vacía

Mantener backward compatibility
```

```
Refactor components/Header.tsx:
- Extraer logic a hooks
- Memoizar renders pesados

Performance crítico
```

```
Test calculator.py:
- Edge cases (división por cero, overflow)
- Property-based testing

Pytest + hypothesis
```

---

## ✅ Checklist Diario

**Al empezar:**
- [ ] Revisar límites disponibles
- [ ] Configurar .claudeignore si proyecto nuevo
- [ ] Ejecutar /init si necesario

**Durante trabajo:**
- [ ] Mensajes específicos y concisos
- [ ] Usar /btw para quick questions
- [ ] Batch operations relacionadas
- [ ] /compact cada 10-15 mensajes

**Al terminar:**
- [ ] /compact si conversación larga
- [ ] Exportar decisiones importantes
- [ ] Revisar uso del día

---

## 📚 Recursos

- [Token Optimization Theory](../docs/token-optimization-theory.md)
- [Setup Guide](../docs/setup-guide.md)
- [Creating Skills](../docs/creating-skills.md)

---

**Pro tip:** Guarda este workflow demo como referencia. La eficiencia se construye con práctica. 🚀
