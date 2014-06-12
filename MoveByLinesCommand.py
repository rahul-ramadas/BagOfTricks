import sublime
import sublime_plugin


class MoveByLinesCommand(sublime_plugin.TextCommand):

    def run(self, edit, forward=True, number_of_lines=1):
        for _ in range(number_of_lines):
            self.view.run_command('move', {"by": "lines", "forward": forward})
