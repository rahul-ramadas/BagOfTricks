import sublime
import sublime_plugin


class RunMultipleCommandsCommand(sublime_plugin.TextCommand):

    def run(self, edit, commands=None, command=None, times=1):
        if commands is None:
            commands = [command] if command is not None else []

        for _ in range(times):
            for command in commands:
                self.exec_command(command)

    def exec_command(self, command):
        if not "command" in command:
            if isinstance(command, str):
                command = {"command": command}
            else:
                raise ValueError("No command name provided.")

        args = command.get("args")

        contexts = {
            "window": self.view.window(), "app": sublime, "text": self.view}
        context = contexts[command.get("context", "text")]

        context.run_command(command["command"], args)
