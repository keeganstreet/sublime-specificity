import sublime, sublime_plugin, subprocess, threading

class SpecificityCalculatorCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		# Get the text from the currently active line/s
		text = ''
		for region in self.view.sel():
			line = self.view.line(region)
			text += self.view.substr(line) + '\n'

		# Send the text to the specificity.js Node app
		# Do this by opening a subprocess in a new thread
		args = [
			sublime.load_settings(__name__ + '.sublime-settings').get('node_path'),
			sublime.packages_path() + '/' + __name__ + '/lib/specificity.js',
			'--selectors', text
		]

		thread = NodeJS(args)
		thread.start()
		self.handle_thread(thread)

	def handle_thread(self, thread):
		if (thread.isAlive()):
			sublime.set_timeout(lambda: self.handle_thread(thread), 100)
		elif (thread.result != False):
			self.show_result(thread.result)

	def show_result(self, result):
		# Show the result in an output window
		output_panel = self.view.window().get_output_panel('specificity')
		edit = output_panel.begin_edit()
		output_panel.insert(edit, output_panel.size(), result)
		output_panel.end_edit(edit)
		self.view.window().run_command('show_panel', {'panel': 'output.specificity'})

class NodeJS(threading.Thread):

	def __init__(self, args):
		self.args = args
		self.result = None
		threading.Thread.__init__(self)

	def run(self):
		try:
			process = subprocess.Popen(self.args,
				stdin = subprocess.PIPE,
				stdout = subprocess.PIPE,
				stderr = subprocess.STDOUT)

			# Make the result accessible by the main thread
			self.result = process.communicate()[0]

		except OSError:
			sublime.error_message('Error calling NodeJS app')
			self.result = False
