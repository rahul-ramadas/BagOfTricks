import sublime_plugin


class ReverseWordsCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            wordRegion = self.view.word(region)
            word = self.view.substr(wordRegion)
            self.view.replace(edit, wordRegion, word[::-1])
