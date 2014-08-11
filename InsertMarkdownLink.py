import sublime
import sublime_plugin


MARKDOWN_LINK_SNIPPET = "[${{1:{}}}](${{2:{}}})"


class InsertMarkdownLinkCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        import re

        def on_done(link):
            import urllib.request
            with urllib.request.urlopen(link) as page:
                encoding = page.headers.get_content_charset()
                if encoding is None:
                    encoding = "utf-8"
                text = page.read().decode(encoding)
                match = re.search("<title>(.+)</title>", text, re.IGNORECASE)
                if match is None:
                    title = link
                else:
                    title = match.group(1)

            markdown_link = MARKDOWN_LINK_SNIPPET.format(title, link)
            self.view.run_command("insert_snippet", {"contents": markdown_link})

        clipboard_text = sublime.get_clipboard(2000)
        if re.match("http://", clipboard_text, re.IGNORECASE) is not None:
            initial_text = clipboard_text
        else:
            initial_text = ""
        input_view = self.view.window().show_input_panel("Link", initial_text, on_done, None, None)
        input_view.sel().clear()
        input_view.sel().add(sublime.Region(0, input_view.size()))
