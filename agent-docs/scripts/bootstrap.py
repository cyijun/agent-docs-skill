#!/usr/bin/env python3
"""Copy portable materials without replacing existing project-owned content."""
import argparse
import json
import os
from pathlib import Path
import shutil

ASSETS = Path(__file__).resolve().parents[1] / 'assets/project'
BLOCK_START = '<!-- agent-docs:start -->'
BLOCK_END = '<!-- agent-docs:end -->'

def safe(root, name):
    p = Path(name)
    if p.is_absolute() or '..' in p.parts or not p.parts:
        raise ValueError('Expected a nonempty project-relative path: ' + str(name))
    target = root / p
    if not target.resolve().is_relative_to(root):
        raise ValueError('Path escapes project through symlink: ' + str(name))
    # Do not mutate shared/symlinked documents implicitly.
    if any(x.is_symlink() for x in [target, *target.parents] if x != root and x.is_relative_to(root)):
        raise ValueError('Symlinked destination needs an explicit project-specific adaptation: ' + str(name))
    return target

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--docs')
    parser.add_argument('--notes')
    parser.add_argument('--language', default='auto')
    parser.add_argument('--apply', action='store_true', help='Without this flag, only print the plan.')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise ValueError('Project root must already exist.')
    config_path = safe(root, '.agents/docs-config.json')
    if config_path.exists():
        config = json.loads(config_path.read_text())
        for key, requested in [('docs_root', args.docs), ('notes_root', args.notes)]:
            if requested and requested != config.get(key):
                raise ValueError('Existing mapping differs; adapt explicitly rather than reinitialize: ' + key)
        print(json.dumps({'status':'existing-materials-preserved','config':config,
                          'next':'Run the project docs.py activation parts, then review/update requested scope. Nothing was overwritten.'},ensure_ascii=False,indent=2))
        return
    docs = args.docs or next((p for p in ('docs','doc','documentation') if (root/p).is_dir()),'docs')
    notes = args.notes or next((p for p in (docs+'/adr',docs+'/decisions','.agents/notes') if (root/p).is_dir()),'.agents/notes')
    safe(root,docs);safe(root,notes)
    native = (root/notes).exists() and any((root/notes).rglob('*.md'))
    language = args.language
    if language == 'auto':
        sample = '\n'.join(p.read_text(errors='replace')[:3000] for p in root.glob('README*') if p.is_file())
        language = 'zh' if sum('\u3400' <= c <= '\u9fff' for c in sample) > 20 else 'en'
    files = {}
    for p in ASSETS.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc':
            files[p.relative_to(ASSETS).as_posix()] = p.read_bytes()
    config = {'version':1,'docs_root':docs,'notes_root':notes,'notes_format':'native' if native else 'managed',
              'archive_root':notes+'/archived','language':language,
              'exclude':['vendor','node_modules','.git','dist','build','.agents/doc-tools/.local'],
              'budgets':{},'check_command':'python3 .agents/doc-tools/docs.py check --root .'}
    files['.agents/docs-config.json']=(json.dumps(config,ensure_ascii=False,indent=2)+'\n').encode()
    standard = '.agents/skills/doc-maintenance/references/standard.md'
    def rel(from_file,to_file):
        return Path(os.path.relpath(to_file,str(Path(from_file).parent))).as_posix()
    # Preserve existing rules and append only a scoped pointer with explicit same-turn loading.
    instructions = {
        'AGENTS.md':f'''{BLOCK_START}
## Agent documentation

Follow [the documentation standard]({standard}) for affected docs. Current behavior, procedures, decision rationale, and incident history each have one owner. Update only documents affected by the requested work; never infer historical rationale from code.

Before authoring or reviewing initialization output, explicitly open [.agents/skills/doc-maintenance/SKILL.md](.agents/skills/doc-maintenance/SKILL.md), [prose-standard](.agents/skills/prose-standard/SKILL.md), and [trim-session-residue](.agents/skills/trim-session-residue/SKILL.md), including their required references, even if absent from the skill catalog. For decisions also read [archive-agent-notes](.agents/skills/archive-agent-notes/SKILL.md). Copying is not loading. Complete the review in the same turn; do not wait for discovery refresh.

Project paths and checks: [.agents/docs-config.json](.agents/docs-config.json). Use the configured decision format and preserve existing instructions. Frozen archives are historical evidence, not current authority.
{BLOCK_END}''',
        docs+'/AGENTS.md':f'''{BLOCK_START}
## Documentation ownership

Use [the documentation standard]({rel(docs+'/AGENTS.md',standard)}), [maintenance workflow]({rel(docs+'/AGENTS.md','.agents/skills/doc-maintenance/SKILL.md')}), and [prose standard]({rel(docs+'/AGENTS.md','.agents/skills/prose-standard/SKILL.md')}). Keep package contracts beside code, current behavior in references, actions in procedures, rationale in decisions, and chronology in incident reports. Preserve the project’s language and existing public routes. Read these files directly when skills have just been copied.
{BLOCK_END}'''
    }
    if not native:
        policy='.agents/skills/doc-maintenance/references/note-policy.md'
        files[notes+'/README.md']=(f'# Agent Notes\n\nFollow [the decision-record policy]({rel(notes+"/README.md",policy)}) for creation criteria, lifecycle, classification, consolidation, and archival. Search the active tree before adding a decision. No centralized status index is required.\n').encode()
        files[notes+'/implemented/AGENTS.md']=(f'# Implemented decisions\n\nKeep paths, symbols, defaults, and mechanisms current with the shipped implementation. A changed decision or rationale requires a new record and cross-links. Follow [the decision-record policy]({rel(notes+"/implemented/AGENTS.md",policy)}).\n').encode()
        files[notes+'/archived/AGENTS.md']=b'# Archived decisions\n\nThese records are frozen historical snapshots, never current authority. Do not update prose, translations, formatting, or outbound links. Archive only implemented decisions, add the archival date, repair active inbound links, and seal the complete existing document set with the project checker.\n'
    for name, block in instructions.items():
        p=safe(root,name)
        original=p.read_text() if p.exists() else '# Agent instructions\n'
        if BLOCK_START in original or BLOCK_END in original:
            raise ValueError('Existing managed block without configuration: '+name)
        files[name]=(original.rstrip()+'\n\n'+block+'\n').encode()
    rg=safe(root,'.rgignore')
    old=rg.read_text() if rg.exists() else ''
    rule='/'+config['archive_root'].strip('/')+'/'
    files['.rgignore']=(old.rstrip()+'\n'+rule+'\n').lstrip('\n').encode() if rule not in old.splitlines() else old.encode()
    # Preflight every destination before writing anything.
    appendable=set(instructions)|{'.rgignore'}
    for name in files:
        p=safe(root,name)
        if p.exists() and name not in appendable:
            raise ValueError('Existing file would be overwritten; resolve/adapt this collision first: '+name)
        if p.exists() and not p.is_file():
            raise ValueError('Destination is not a file: '+name)
    print(json.dumps({'status':'scaffold-pending-content' if args.apply else 'plan-only','config':config,
                      'files':sorted(files),'next':'Read all four activation parts in full, author source-backed project docs, review, then finish. Scaffolding is not completion.'},ensure_ascii=False,indent=2))
    if args.apply:
        created=[];replaced={}
        try:
            for name,data in files.items():
                p=safe(root,name)
                if p.exists():replaced[p]=p.read_bytes()
                else:created.append(p)
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(data)
        except Exception:
            for p,data in replaced.items():p.write_bytes(data)
            for p in reversed(created):p.unlink(missing_ok=True)
            raise

if __name__=='__main__':
    try: main()
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        raise SystemExit('bootstrap: '+str(exc))
