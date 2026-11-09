import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

PACKAGE=Path(__file__).resolve().parents[1]/'agent-docs'
BOOT=PACKAGE/'scripts/bootstrap.py'
class Portable(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'project';self.root.mkdir()
  (self.root/'README.md').write_text('# Example\n\nA small project with actual source and a local command.\n')
  (self.root/'app.py').write_text('print("ready")\n')
 def tearDown(self):self.temp.cleanup()
 def run_cmd(self,*args,ok=True):
  result=subprocess.run([sys.executable,*map(str,args)],cwd=self.root,capture_output=True,text=True)
  if ok:self.assertEqual(result.returncode,0,result.stdout+result.stderr)
  else:self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
  return result
 def init(self,*args):return self.run_cmd(BOOT,'--root',self.root,'--apply',*args)
 def tool(self,*args,ok=True):return self.run_cmd(self.root/'.agents/doc-tools/docs.py',*args,'--root',self.root,ok=ok)
 def report(self):
  (self.root/'docs/development.md').write_text('# Development\n\nRun `python3 app.py` from the project root. The program prints ready and exits. The entry point is [app.py](../app.py). No external service or network is required.\n')
  data={'outputs':[{'path':'docs/development.md','sources':['app.py']}],
        'reviews':[{'principle':p,'path':'docs/development.md','finding':'Test evidence: the local Python entry point and its observable ready output are preserved.'} for p in ['fact-ownership','complete-propositions','session-independent','existing-content-preserved']],
        'verification':['python3 app.py printed ready in this isolated test fixture.']}
  p=self.root/'review.json';p.write_text(json.dumps(data));return p
 def test_plan_and_portable_links(self):
  self.run_cmd(BOOT,'--root',self.root);self.assertFalse((self.root/'.agents').exists())
  self.init();self.tool('check')
 def test_preserve_existing_rules_and_rerun(self):
  original='# Local instructions\n\nKeep this exact user rule.\n';(self.root/'AGENTS.md').write_text(original)
  self.init();self.assertTrue((self.root/'AGENTS.md').read_text().startswith(original))
  p=self.root/'.agents/skills/prose-standard/SKILL.md';p.write_text(p.read_text()+'\nProject-specific addition.\n')
  before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
  self.init();after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()};self.assertEqual(before,after)
 def test_collision_has_no_partial_writes(self):
  p=self.root/'.agents/skills/prose-standard/SKILL.md';p.parent.mkdir(parents=True);p.write_text('existing skill')
  self.run_cmd(BOOT,'--root',self.root,'--apply',ok=False)
  self.assertFalse((self.root/'AGENTS.md').exists());self.assertFalse((self.root/'.agents/docs-config.json').exists());self.assertEqual(p.read_text(),'existing skill')
 def test_path_escape_and_symlink(self):
  self.run_cmd(BOOT,'--root',self.root,'--docs','../outside','--apply',ok=False)
  outside=Path(self.temp.name)/'outside';outside.mkdir();(self.root/'docs').symlink_to(outside,target_is_directory=True)
  self.run_cmd(BOOT,'--root',self.root,'--apply',ok=False);self.assertEqual(list(outside.iterdir()),[])
 def test_native_adr_unchanged(self):
  p=self.root/'documentation/adr/0001-storage.md';p.parent.mkdir(parents=True);p.write_text('# Storage\n\nAccepted: files.\n')
  original=p.read_bytes();self.init();c=json.loads((self.root/'.agents/docs-config.json').read_text())
  self.assertEqual(c['notes_format'],'native');self.assertEqual(c['notes_root'],'documentation/adr');self.assertEqual(p.read_bytes(),original);self.tool('check')
 def test_activation_required_and_stale(self):
  self.init();report=self.report();self.tool('finish','--report',report,ok=False)
  for part in ['docs','prose','trim','archive']:
   result=self.tool('activate','--part',part);self.assertIn('FILE:',result.stdout)
  self.tool('finish','--report',report)
  p=self.root/'.agents/skills/prose-standard/SKILL.md';p.write_text(p.read_text()+'\nA changed rule.\n')
  result=self.tool('finish','--report',report,ok=False);self.assertIn('stale',result.stderr)
 def test_no_scaffold_only_completion(self):
  self.init()
  for part in ['docs','prose','trim','archive']:self.tool('activate','--part',part)
  p=self.root/'review.json';p.write_text(json.dumps({'outputs':[],'reviews':[],'verification':[]}))
  self.tool('finish','--report',p,ok=False)
 def test_links_and_proposal_structure(self):
  self.init();p=self.root/'docs/bad.md';p.write_text('# Bad\n\n[Missing](missing.md)\n');self.tool('check',ok=False);p.unlink()
  p=self.root/'.agents/notes/implemented/architecture/2026-11-10-storage.md';p.parent.mkdir(parents=True,exist_ok=True)
  p.write_text('# Agent Note: Storage\n\nStatus: proposed\n\n## Problem\nA real problem.\n');self.tool('check',ok=False)
 def test_archive_seal_tamper_and_baseline(self):
  self.init();p=self.root/'.agents/notes/archived/architecture/2026-11-10-storage.md';p.parent.mkdir(parents=True,exist_ok=True)
  p.write_text('# Agent Note: Storage\n\nStatus: implemented\nArchived: 2026-11-10\n\nHistorical body and [old link](no-longer-exists.md).\n')
  self.tool('check',ok=False);self.tool('seal');self.tool('check')
  subprocess.run(['git','init','-q'],cwd=self.root,check=True)
  subprocess.run(['git','add','.'],cwd=self.root,check=True)
  subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','baseline'],cwd=self.root,check=True)
  p.write_text(p.read_text()+'changed\n');self.tool('seal',ok=False)
  manifest=self.root/'.agents/doc-tools/archive-seals.json';data=json.loads(manifest.read_text());data['files'][p.relative_to(self.root).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest();manifest.write_text(json.dumps(data))
  self.tool('check');self.tool('check','--baseline','HEAD',ok=False)
 def test_cjk_budget(self):
  self.init();p=self.root/'docs/chinese.md';p.write_text('中文内容不使用空格也应计入预算')
  c=self.root/'.agents/docs-config.json';data=json.loads(c.read_text());data['budgets']={'docs/chinese.md':3};c.write_text(json.dumps(data));self.tool('check',ok=False)
 def test_relocated_package_no_upstream_needed(self):
  copy=Path(self.temp.name)/'relocated-skill';shutil.copytree(PACKAGE,copy,ignore=shutil.ignore_patterns('__pycache__'))
  self.run_cmd(copy/'scripts/bootstrap.py','--root',self.root,'--apply');self.tool('check')

if __name__=='__main__':unittest.main(verbosity=2)
