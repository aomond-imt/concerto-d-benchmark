import subprocess
import time

from concerto import global_variables, debug_logger
from concerto.assembly import Assembly
from concerto.component import Component
from concerto.dependency import DepType

nb_comps = 100


class SingleTransition(Component):
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
            f"dep{i}": (DepType.USE, ["running"]) for i in range(1)
        }
        self.initial_place = "undeployed"

    def run(self):
        self.print_color("preparing to run")
        # subprocess.run(["stress", "-c", "1", "-t", "3"])
        time.sleep(3)
        self.print_color("running")


class BenchAssembly(Assembly):
    def __init__(self):
        Assembly.__init__(
            self,
            "bench_comp_assembly",
            {"SingleTransition": SingleTransition},
            {},
            {f"bench_comp{i}": {} for i in range(nb_comps)},
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
    for i in range(nb_comps):
        sc.add_component(f"bench_comp{i}", "SingleTransition")
    for i in range(nb_comps):
        sc.connect(f"bench_comp{i}", f"dep0", f"other_bench_comp{i}", "other_bench_port")
    for i in range(nb_comps):
        sc.push_b(f"bench_comp{i}", "deploy")
    sc.wait_all()
