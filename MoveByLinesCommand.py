import sublime
import sublime_plugin


class MoveByLinesCommand(sublime_plugin.TextCommand):

    def is_selection_in_sight(self):
        sel = self.view.sel()[0]
        visible_region = self.view.visible_region()
        in_sight = visible_region.intersects(sel) or visible_region.contains(sel)
        return in_sight

    def run(self, edit, forward=True, extend=False, number_of_lines=1):

        # Handle the special case where the view was scrolled away from the current location of
        # the cursor. Trying to move the cursor will cause the view to scroll back to the current
        # position of the cursor first. Bring the cursor into the current view, and then start
        # moving it from there. Only do this if multiple selections are not present, just in case
        # I'm trying to do something funky there.
        if len(self.view.sel()) == 1 and not self.is_selection_in_sight():
            visible_region = self.view.visible_region()
            self.view.sel().clear()
            if forward:
                pos = visible_region.begin()
            else:
                pos = visible_region.end()
            self.view.sel().add(sublime.Region(pos, pos))

        for _ in range(number_of_lines):
            self.view.run_command('move', {"by": "lines", "forward": forward, "extend": extend})
