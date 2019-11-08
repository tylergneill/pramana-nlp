import subprocess

for fn in [
	'Thakur1', 'Thakur2', 'Thakur3', 'Thakur4', 'Thakur5',
]:
	subprocess.call(
		"python3 apply.py data/input/%s.txt data/output/%s_unsandhied.txt" % (fn, fn),
		shell=True
	)