from rich import Console
# TODO: top level setup for instantiation of tools like rich
# easier management and access for CLI
# should also make config setup easier


class App(object):
    console = Console()


dumpster_obj = App()
