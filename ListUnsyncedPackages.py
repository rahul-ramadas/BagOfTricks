import sublime
import sublime_plugin
import os
import json


class ListUnsyncedPackagesCommand(sublime_plugin.TextCommand):

    def list_default_packages(self):
        """
        Returns a list of all default package names.
        """

        bundled_packages_path = os.path.join(os.path.dirname(sublime.executable_path()), 'Packages')
        files = os.listdir(bundled_packages_path)

        packages = [file.replace('.sublime-package', '') for file in files]
        packages = sorted(packages, key=lambda s: s.lower())
        return packages

    def list_packages(self):
        """
        Returns a list of all installed, non-default, package names.
        """

        package_names = os.listdir(sublime.packages_path())
        package_names = [path for path in package_names if path[0] != '.' and
                         os.path.isdir(os.path.join(sublime.packages_path(), path))]

        package_files = os.listdir(sublime.installed_packages_path())
        package_names += [f.replace('.sublime-package', '') for
                          f in package_files if f.endswith('.sublime-package')]

        # Ignore things to be deleted
        ignored = ['User']
        for package in package_names:
            cleanup_file = os.path.join(sublime.packages_path(), package, 'package-control.cleanup')
            if os.path.exists(cleanup_file):
                ignored.append(package)

        packages = list(set(package_names) - set(ignored) - set(self.list_default_packages()))
        packages = sorted(packages, key=lambda s: s.lower())

        return packages

    def list_synced_packages(self):
        """
        Returns a list of packages that will get synced automatically be Package Control.
        """

        package_control_settings_file = os.path.join(sublime.packages_path(),
                                                     'User',
                                                     'Package Control.sublime-settings')

        with open(package_control_settings_file) as f:
            package_control_settings = json.load(f)

        return package_control_settings['installed_packages']

    def run(self, edit):
        installed_packages = self.list_packages()
        installed_packages_lower = set(p.lower() for p in installed_packages)
        synced_packages = set(p.lower() for p in self.list_synced_packages())
        unsynced_packages = installed_packages_lower - synced_packages

        # Remove Package Control from the list, since we are not interested in that.
        unsynced_packages.remove('package control')

        unsynced_packages = [p for p in installed_packages if p.lower() in unsynced_packages]
        self.view.window().show_quick_panel(unsynced_packages, None)
