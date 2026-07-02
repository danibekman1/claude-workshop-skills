# TypeScript Language Pack (skeleton)

This is a skeleton pack. It declares no rules yet, so when the orchestrator dispatches it
on a `*.ts` or `*.tsx` diff, the reviewer returns a single "skeleton pack, no rules
defined yet" note and an Approve verdict. Its purpose is to keep the add-a-pack mechanism
testable and to serve as the copy-me template for a real pack.

Real TypeScript rules currently live inline in
`../../code-style-review/code-style-reviewer.md`, under "File-Type-Specific Rules". They
migrate into this pack in a future story; until then this pack stays empty and the inline
rules remain the source of truth for TypeScript.

## The Patterns

(none yet)

To turn this skeleton into a real pack, replace this section with patterns shaped like the
ones in `python.md`: a `[TS: NAME]` prefix, then a `TRIGGER`, `DETECT`, `DO NOT FLAG`,
`VOICE`, and a `SEVERITY` of `flag` or `report`. Then set the `ts` row in `../SKILL.md` to
status `active`.
