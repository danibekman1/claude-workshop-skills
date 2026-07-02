# Python Language Pack

Manifest of Python-specific syntax and idiom rules. The shared `language-pack-reviewer.md`
template reads this file and applies these patterns to the `*.py` files in the diff.
Glob and dispatch are owned by the registry table in `../SKILL.md`, not here.

Scope is Python syntax and idiom only. Language-agnostic concerns (naming, error
handling in general, magic numbers, guard clauses, secrets in logs) belong to code-style;
do not repeat them here.

Each pattern carries a `SEVERITY` of `flag` (a genuine safety or correctness issue) or
`report` (idiom and style). The reviewer routes findings by that marker.

## The 7 Patterns

**[PY: MUTABLE-DEFAULT] Mutable default argument**
- TRIGGER: a function or method parameter whose default is a mutable literal or call -
  `[]`, `{}`, `set()`, `dict()`, `list()`, or anything returning a mutable object. The
  default is created once at definition time and shared across every call, so one call's
  mutation leaks into the next.
- DETECT: scan `def` signatures for a parameter default that is a mutable container.
  Confirm the body (or any caller path) mutates it; a shared default that is mutated is
  the bug.
- DO NOT FLAG: immutable defaults (`None`, numbers, strings, tuples, `frozenset()`); a
  default that is genuinely never mutated and is documented as intentional, though `None`
  plus in-body init is still preferred.
- VOICE: "mutable default shared across calls - use None and init in the body."
- SEVERITY: flag

**[PY: EVAL-EXEC] eval / exec on dynamic input**
- TRIGGER: `eval(`, `exec(`, or `compile(..., 'exec')` applied to anything that is not a
  trusted literal constant - user input, file or network data, or a value derived from
  them. This is arbitrary code execution.
- DETECT: find `eval(` / `exec(`. Trace the argument. Flag when the argument is dynamic
  rather than a hard-coded constant.
- DO NOT FLAG: a tightly scoped, documented metaprogramming use on a trusted constant
  where there is no reasonable alternative. For parsing literals, `ast.literal_eval` is
  the safe replacement and should be suggested.
- VOICE: "eval on dynamic input - use ast.literal_eval or an explicit parser."
- SEVERITY: flag

**[PY: RAISE-FROM] Exception chaining dropped**
- TRIGGER: inside an `except SomeError as e:` block, a `raise NewError(...)` with no
  `from e` (and no deliberate `from None`), so the original cause is dropped from the
  traceback and the root failure is hidden.
- DETECT: find `raise` statements inside `except` blocks that bind the caught exception.
  Check for a `from` clause on the raise.
- DO NOT FLAG: a bare `raise` (it re-raises the original, chain intact); `raise ... from
  None` when suppression is deliberate; an except block that does not bind the exception
  and raises something unrelated where a chain would add no signal.
- VOICE: "raise inside except without `from e` - the original cause is lost."
- SEVERITY: flag

**[PY: IMPORTS-TOP] Imports not at module top (PEP 8)**
- TRIGGER: an `import` or `from ... import` placed below the first executable statement
  of a module, or buried inside a function, without a reason.
- DETECT: imports appearing after module-level code runs, or inside function bodies with
  no circular-dependency or lazy-loading justification.
- DO NOT FLAG: a lazy import that breaks a circular dependency or defers a heavy or
  optional dependency (with a comment saying so); imports inside an `if TYPE_CHECKING:`
  block; a conditional import guarding an optional feature.
- VOICE: "import belongs at the top - move it up unless this is a deliberate lazy import."
- SEVERITY: report

**[PY: VALUE-DATACLASS] Value objects should be frozen and slotted**
- TRIGGER: a value object (its identity is its field values, no behavior beyond holding
  data) written as a plain class or a mutable `@dataclass`, where
  `@dataclass(slots=True, frozen=True)` would make it immutable and cheap.
- DETECT: data-holder classes and dataclasses that are compared by value and not mutated
  after construction.
- DO NOT FLAG: a class with real behavior or identity semantics; a dataclass that is
  intentionally mutable because callers update it in place; a class whose required
  inheritance is incompatible with `slots`.
- VOICE: "value object - `@dataclass(slots=True, frozen=True)`?"
- SEVERITY: report

**[PY: DOCSTRING] Google-style docstrings on public APIs**
- TRIGGER: a public (no leading underscore) function, method, or class with no docstring,
  or a docstring that does not follow the Google format - a one-line summary, then
  `Args:` / `Returns:` / `Raises:` sections where they apply.
- DETECT: public defs and classes; check for a docstring and its shape.
- DO NOT FLAG: private (leading-underscore) members; a trivial function whose summary
  line alone is enough; test functions; an override that inherits its docstring.
- VOICE: "public API - Google-style docstring with Args/Returns?"
- SEVERITY: report

**[PY: TYPING] Python typing idiom on public signatures**
- TRIGGER: a public function or method using imprecise or non-idiomatic Python typing -
  bare containers where PEP 585 builtin generics (`list[X]`, `dict[K, V]`) or a precise
  `typing` shape (`Protocol`, `TypedDict`, `Literal`, `Sequence` / `Mapping`) would
  document the contract, or `Any` where the shape is known.
- DETECT: public defs whose annotations are present but imprecise, or that would read
  better with a PEP 585 / `typing` construct.
- DO NOT FLAG: private helpers where the type is obvious; `self` / `cls`; `*args` /
  `**kwargs` where annotating adds noise; test functions.
- NOTE: the general "annotate the public boundary at all" rule now lives in code-style as
  `[LA: TYPE-BOUNDARY]`. A public symbol with NO annotation is one
  `[LA: TYPE-BOUNDARY]` finding; this rule is the Python-specific complement, for idiom and
  precision on symbols that already carry annotations. Do not raise both for the same
  missing annotation on the same symbol.
- VOICE: "use `list[Record]` / a precise typing shape here."
- SEVERITY: report
