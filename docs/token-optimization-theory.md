# Token Optimization Theory

Principios y técnicas para maximizar eficiencia en Claude Pro.

## 🎯 Por Qué Importa

### Límites de Claude Pro

Claude Pro tiene límites de uso diarios:
- **Mensajes por día:** Limitados
- **Tokens por mensaje:** Contabilizados
- **Contexto acumulativo:** Se suma en conversaciones largas

**Cada token cuenta para estos límites.**

### El Problema de Prompts Ineficientes

```markdown
❌ MAL (verbose, 150 tokens):
"Hola, me gustaría que por favor me ayudaras a entender de manera 
muy detallada y completa, con todos los detalles posibles, exactamente 
qué es lo que hace este código y cómo funciona paso a paso cada una 
de las líneas, porque necesito comprenderlo bien para mi proyecto..."

✅ BIEN (conciso, 25 tokens):
"Explica este código línea por línea"
```

**Ahorro:** 83% de tokens, mismo resultado.

## 🧠 Principios de Optimización

### 1. Eliminar Redundancia

**Antes:**
```
Por favor, me gustaría que me ayudaras a...
```

**Después:**
```
Ayúdame a...
```

**Regla:** Ve al grano. Claude entiende contexto implícito.

### 2. Ser Específico, No Verbose

**Antes:**
```
Crea una función que tome como parámetros un número entero y otro 
número entero y que retorne la suma de ambos números
```

**Después:**
```
Función: suma de dos enteros
```

**Regla:** Especificidad ≠ Verbosidad

### 3. Usar Comandos Built-in

**Antes:**
```
Por favor lee este archivo y dime qué contiene
```

**Después:**
```
/view archivo.py
```

**Regla:** Usa herramientas nativas cuando existan.

### 4. Batch Operations

**Antes (3 mensajes):**
```
1. "Crea función suma"
2. "Ahora función resta"  
3. "Ahora función multiplica"
```

**Después (1 mensaje):**
```
Crea funciones: suma, resta, multiplica
```

**Regla:** Agrupa requests relacionados.

### 5. Context Management

**Antes:**
```
[Todo el historial de 50 mensajes cargado]
```

**Después:**
```
/compact  # Compacta contexto automáticamente
```

**Regla:** Usa `/compact` cuando contexto >50%.

## 🛠️ Técnicas Avanzadas

### A. Configuración Global

`~/.claude/global.md`:

```markdown
## Token Efficiency
- Use `/btw` for questions that don't need context
- Read files only when explicitly needed
- Batch related edits in single operation
```

**Efecto:** Claude aplica estas reglas automáticamente.

### B. Custom Ignorefile

`.claudeignore` optimizado:

```
# Bloquear ruido
node_modules/
*.log
__pycache__/

# Permitir cuando necesario
# dist/  ← NO bloqueado por defecto
```

**Efecto:** Claude no lee 10,000 archivos de node_modules.

### C. Smart-Init

Generar configs automáticamente:

```
/init
```

**Efecto:** Setup perfecto en segundos, sin manual config.

### D. Explicit File Reading

**Antes:**
```
"Lee todos los archivos del proyecto"
```

**Después:**
```
/view src/main.py
/view tests/test_main.py
```

**Regla:** Especifica qué leer, no "todo".

## 📊 Estrategias por Caso de Uso

### Debugging

```markdown
❌ "El código no funciona, ayúdame"
✅ "Error en línea 42: NameError 'x' not defined"
```

### Code Review

```markdown
❌ "Revisa todo este archivo"
✅ "Revisa función `process_data()` (líneas 30-45)"
```

### Refactoring

```markdown
❌ "Mejora el código"
✅ "Refactor: extraer lógica de validación a función separada"
```

### Documentation

```markdown
❌ "Documenta este proyecto completo"
✅ "Documenta función `calculate_metrics()`"
```

## 🎯 Workflow Óptimo

### Setup Inicial (una vez)

1. Instalar configs de este repo
2. Configurar `.claudeignore` para tu stack
3. Ejecutar `/init` en proyectos

### Uso Diario

```
1. Mensaje específico y conciso
2. Usar /btw para quick questions
3. Batch operations relacionadas
4. /compact cuando contexto alto
5. Verificar límites en settings
```

### Conversaciones Largas

```
- Cada 10-15 mensajes → /compact
- Si hitting límites → Nueva conversación
- Exportar info importante antes de compact
```

## 📈 Métricas de Éxito

### Antes de Optimizar

- Prompts: ~200 tokens promedio
- Mensajes útiles/día: ~30
- Hit límite: frecuente

### Después de Optimizar

- Prompts: ~50 tokens promedio
- Mensajes útiles/día: ~80
- Hit límite: raro

**Resultado:** 2.5x más conversaciones con mismo plan.

## 🔍 Anti-Patterns

### ❌ Sobre-optimización

```
"fnc sum(a,b)ret a+b"  # Ilegible
```

**Balance:** Claridad > Tokens extremos

### ❌ Omitir Contexto Crítico

```
"Arregla el bug"  # ¿Qué bug?
```

**Balance:** Específico ≠ Mínimo

### ❌ Abusar de /compact

```
/compact después de cada mensaje
```

**Balance:** Compactar cada 10-15 mensajes

## 💡 Tips Avanzados

### 1. Use Markdown Efficientemente

```markdown
Antes: "La función debe hacer X, Y, y Z"

Después:
Función debe:
- X
- Y  
- Z
```

### 2. Code Snippets Parciales

```markdown
Antes: [Pegar 500 líneas de código]

Después: "Ver src/main.py líneas 100-120"
```

### 3. Aliases Mentales

```markdown
Antes: "El sistema de procesamiento de datos"

Después (primera mención):
"El sistema de procesamiento de datos (SPD)"

Después (resto):
"SPD debe..."
```

## 📚 Referencias

- [Setup Guide](setup-guide.md) - Cómo instalar
- [Creating Skills](creating-skills.md) - Automatización avanzada
- [Workflow Demo](../examples/workflow-demo.md) - Ejemplos reales

## 🎓 Ejercicio

**Optimiza este prompt:**

```
"Hola Claude, espero que estés bien. Me gustaría que por favor me 
ayudaras con algo. Tengo un proyecto en Python y necesito que me 
ayudes a crear una función que reciba como parámetros dos números 
enteros y que retorne la suma de esos dos números. ¿Podrías por 
favor ayudarme con eso? Gracias!"
```

**Solución:**

```
"Función Python: suma dos enteros"
```

**Reducción:** ~90% de tokens, claridad mantenida.

---

**Recuerda:** Eficiencia ≠ Sacrificar claridad. El objetivo es comunicación clara con mínimo desperdicio. 🎯
