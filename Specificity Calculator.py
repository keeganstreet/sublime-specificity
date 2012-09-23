import sublime, sublime_plugin, subprocess, threading

class SpecificityCalculatorCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		# Get the text from the currently active line/s
		text = ''
		for region in self.view.sel():
			line = self.view.line(region)
			text += self.view.substr(line) + '\n'

		# Send the text to the specificity.js Node app
		cmd = [
			sublime.load_settings(__name__ + '.sublime-settings').get('node_path'),
			sublime.packages_path() + '/' + __name__ + '/lib/specificity.js',
			'--selectors', text
		]
		threading.Thread(target = _run, args = cmd).start()

def _run(cmd, args):

	try:
		process = subprocess.Popen([cmd, args],
			stdin = subprocess.PIPE,
			stdout = subprocess.PIPE,
			stderr = subprocess.STDOUT)
		print process.communicate()[0]

	except OSError:
		sublime.error_message('Error calling NodeJS app')
