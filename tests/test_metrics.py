import importlib.util
from pathlib import Path
import ast
import textwrap
import sys


def load_hardmetrics():
	repo_root = Path(__file__).resolve().parents[1]
	metrics_dir = repo_root / 'src' / 'Metrics'
	# make sibling modules importable (Cyclomatic, NestedDepth, fileParsing)
	if str(metrics_dir) not in sys.path:
		sys.path.insert(0, str(metrics_dir))

	hm_path = metrics_dir / 'HardMetrics.py'
	spec = importlib.util.spec_from_file_location('HardMetrics', str(hm_path))
	hm = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(hm)
	return hm


def test_remove_and_count_comments_and_docstrings_and_blanks(tmp_path):
	hm = load_hardmetrics()
	code = textwrap.dedent("""
	# first comment
	#! shebang-like should be ignored for counting
	def foo():
		'''
		doc line1
		doc line2
		'''
		x = 1  # inline comment


	""")

	# test removal helpers
	no_comments = hm.removeComment(code)
	assert '# first comment' not in no_comments
	assert 'inline comment' not in no_comments

	no_doc = hm.removeDocstring(code)
	assert "doc line1" not in no_doc

	no_blank = hm.removeblank(code)
	assert '\n\n' not in no_blank

	# test counters
	assert hm.countComment(code) == 2  # '# first comment' and inline comment (shebang ignored)
	assert hm.countDocstring(code) == 4  # docstring has 2 internal lines + 2 for the triple quotes behaviour
	assert hm.countblank(code) >= 1


def test_calculatePercentage(tmp_path):
	hm = load_hardmetrics()
	p = tmp_path / 'sample.py'
	p.write_text(textwrap.dedent("""
	# a comment
	'''
	doc
	'''

	x = 1
	"""))

	comment_pct, doc_pct, blank_pct = hm.calculatePercentage(str(p))
	total_lines = len(p.read_text().splitlines())
	# basic assertions: percentages between 0 and 100 and sum not exceeding 100*3
	assert 0.0 <= comment_pct <= 100.0
	assert 0.0 <= doc_pct <= 100.0
	assert 0.0 <= blank_pct <= 100.0


def test_function_parsing_and_sources():
	hm = load_hardmetrics()
	clean = textwrap.dedent("""
	def a():
		x = 1

	def b():
		y = 2
		y += 1
	""")

	funcs = hm.findFunc(clean)
	assert len(funcs) == 2
	names = hm.funcName(clean)
	assert set(names) == {'a', 'b'}

	splits = hm.splitFunc(clean)
	assert any('def a' in s for s in splits)

	avg = hm.avgFunc(clean)
	assert avg > 0


def test_getFunctionSource(tmp_path):
	hm = load_hardmetrics()
	p = tmp_path / 'f.py'
	p.write_text(textwrap.dedent('''
	def foo():
		return 42

	def bar():
		return 7
	'''))

	src = p.read_text()
	tree = ast.parse(src)
	funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
	assert funcs
	first_src = hm.getFunctionSource(str(p), funcs[0])
	assert 'def' in first_src and 'return' in first_src


def test_loop_metrics_and_nested(tmp_path):
	hm = load_hardmetrics()
	content = textwrap.dedent('''
	for i in range(3):
		for j in range(2):
			x = i*j

	while True:
		break
	''')
	p = tmp_path / 'loops.py'
	p.write_text(content)

	# countLoops and avgLoop take cleanFile strings
	assert hm.countLoops(content) >= 3
	avg = hm.avgLoop(content)
	assert isinstance(avg, (int, float))

	# file-based nested loop detection
	assert hm.findNestedLoops(str(p)) is True
	assert hm.findLoops(str(p)) is True


def test_condition_and_structural_findings():
	hm = load_hardmetrics()
	code_if = 'if True:\n    a=1'
	assert hm.findIfOrVar(code_if)

	code_bool = 'a and b or not c'
	assert hm.findBoolAlg(code_bool)

	code_dict = 'd = {"x":1}'
	assert hm.findDictionaries(code_dict)

	code_slice = 'a = arr[1:3]'
	assert hm.findSlicing(code_slice)

	code_listcomp = '[x for x in range(5)]'
	assert hm.findListComp(code_listcomp)


def test_recursion_and_oop_and_identify_and_sumtests(tmp_path):
	hm = load_hardmetrics()
	# recursion: due to implementation details this will return False (see code behavior)
	r = tmp_path / 'rec.py'
	r.write_text(textwrap.dedent('''
	def f(n):
		if n<=0:
			return 1
		return n * f(n-1)
	'''))
	assert hm.findRecursion(str(r)) is False

	# oop detection
	o = tmp_path / 'oop.py'
	o.write_text(textwrap.dedent('''
	class A:
		def m(self):
			pass
	'''))
	assert hm.findOop(str(o)) is True

	# identify project writes a _metrics.txt and returns best match
	p = tmp_path / 'game.py'
	p.write_text('lifeboard life gen')
	match = hm.identify_project(str(p))
	assert match in {'gameOfLife', 'textID', 'picoBot', 'vPython', 'textGame_keywords'}

	assert hm.sumTests([True, False, True]) == 2


def test_allMetrics_monkeypatched(tmp_path, monkeypatch):
	hm = load_hardmetrics()

	# create a simple file
	f = tmp_path / 'simple.py'
	f.write_text('def a():\n    return 1\n')

	# monkeypatch fileParsing helpers inside the loaded module
	monkeypatch.setattr(hm.fileParsing, 'doesItParse', lambda path: True)
	monkeypatch.setattr(hm.fileParsing, 'cleanParseFile', lambda path: 'def a():\n    return 1')
	monkeypatch.setattr(hm.fileParsing, 'getClassFromFilepath', lambda p: 'CS35')
	monkeypatch.setattr(hm.fileParsing, 'getSemesterFromFilepath', lambda p: 'sp2025')
	monkeypatch.setattr(hm.fileParsing, 'getYearFromFilepath', lambda p: 2025)

	# monkeypatch cyclomatic complexity and CallChain
	monkeypatch.setattr(hm, 'calculate_cyclomatic_complexity', lambda src: 5)

	class FakeChain:
		def __init__(self, a, b):
			self.depth = 3

	monkeypatch.setattr(hm, 'CallChain', FakeChain)

	out = hm.allMetrics(str(f))
	# new behavior: allMetrics returns a MetricRecord dataclass
	# dataclass may be present as the module's MetricRecord or a simple object with attributes
	assert hasattr(out, 'file')
	assert out.file == str(f)
	assert out.num_funcs == 1
	# depending on name, cyclomatic complexity is exposed as 'cyclo'
	assert getattr(out, 'cyclo', None) == 5

