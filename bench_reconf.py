import time

from concerto import global_variables, debug_logger
from concerto.assembly import Assembly
from concerto.component import Component
from concerto.debug_logger import log
from concerto.dependency import DepType

nb_deps = 30


class BenchComp(Component):
    def __init__(self):
        Component.__init__(self)

    def create(self):
        self.places = [
            "undeployed",
            "running"
        ]

        self.transitions = {
            "run": ("undeployed", "running", "deploy", 0, self.run)
        }

        self.dependencies = {
            f"dep{i}": (DepType.USE, ["running"]) for i in range(nb_deps)
        }
        self.initial_place = "undeployed"

    def run(self):
        self.print_color("preparing to run")
        #time.sleep(0)
        self.print_color("running")


class BenchAssembly(Assembly):
    def __init__(self):
        Assembly.__init__(
            self,
            "bench_comp_assembly",
            {"BenchComp": BenchComp},
            {},
            {"bench_comp": {}},
            1,
            "synchronous",
            1,
            "bench")


if __name__ == "__main__":
    global_variables.execution_expe_dir = "."
    debug_logger.set_stdout_formatter("bench_comp_assembly")
    sc = BenchAssembly()
    sc.set_verbosity(2)
    sc.time_manager.start(10)
    sc.add_component("bench_comp", "BenchComp")
    for i in range(nb_deps):
        sc.connect("bench_comp", f"dep{i}", "other_bench_comp", "other_bench_port")
    sc.push_b("bench_comp", "deploy")
    sc.wait("bench_comp")
    # time.sleep(5)
