#!/usr/bin/env python3
"""Validate project docs and the exact source-to-consumer material mapping."""
import argparse
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True

def check_project(root):
    root = root.resolve()
    assets = root / 'agent-docs/assets/project'
    spec = importlib.util.spec_from_file_location('agent_docs_checker', assets / '.agents/doc-tools/docs.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    errors = checker.check(root, checker.load(root))
    for source in assets.rglob('*'):
        if not source.is_file() or '__pycache__' in source.parts or source.suffix == '.pyc':
            continue
        relative = source.relative_to(assets)
        deployed = root / relative
        if not deployed.is_file():
            errors.append(f'{relative}: missing project copy')
        elif deployed.read_bytes() != source.read_bytes():
            errors.append(f'{relative}: differs from agent-docs/assets/project; review the owner and synchronize deliberately')
    for document in (root / 'agent-docs').rglob('*.md'):
        relative = document.relative_to(root).as_posix()
        errors.extend(checker.link_errors(root, relative, document.read_text()))
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    try:
        errors = check_project(Path(args.root).resolve())
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit(f'project-docs: {error}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print('project-docs: passed local-target, document-structure, and source/copy checks')

if __name__ == '__main__':
    main()
