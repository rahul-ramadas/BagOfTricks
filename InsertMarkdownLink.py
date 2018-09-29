import sublime
import sublime_plugin


MARKDOWN_LINK_SNIPPET = "[${{1:{}}}](${{2:{}}})"


class InsertMarkdownLinkCommand(sublime_plugin.TextCommand):

    def decode_page(self, page_bytes, potential_encoding=None):
        if potential_encoding:
            try:
                text = page_bytes.decode(potential_encoding)
                return text
            except:
                pass

        encodings_to_try = ["utf-8", "iso-8859-1"]

        for encoding in encodings_to_try:
            if encoding == potential_encoding:
                continue

            try:
                text = page_bytes.decode(encoding)
                return text
            except:
                pass

        raise UnicodeDecodeError

    def run(self, edit):
        import re

        def on_done(link):
            import urllib.request
            request = urllib.request.Request(link, headers={'User-Agent' : 'Google Internal-Only Browser'})
            with urllib.request.urlopen(request) as page:
                encoding = page.headers.get_content_charset()
                text = self.decode_page(page.read(), encoding)
                match = re.search("<title>(.+?)</title>", text, re.IGNORECASE | re.DOTALL)
                if match is None:
                    title = link
                else:
                    title = match.group(1).strip()

            markdown_link = MARKDOWN_LINK_SNIPPET.format(title, link)
            self.view.run_command("insert_snippet", {"contents": markdown_link})

        clipboard_text = sublime.get_clipboard(2000)
        if re.match("https?://", clipboard_text, re.IGNORECASE) is not None:
            initial_text = clipboard_text
        else:
            initial_text = ""
        input_view = self.view.window().show_input_panel("Link", initial_text, on_done, None, None)
        input_view.sel().clear()
        input_view.sel().add(sublime.Region(0, input_view.size()))
