# Description: This file contains the Tracer class which is used to trace the time taken
# by different parts of the code.
import time

class Tracer:
    def __init__(self):
        self._tracers = {}

    def start_tracing(self, tracer_name: str):
        self._tracers[tracer_name] = time.time()

    def stop_tracing(self, tracer_name: str, message_template: str = None):
        if tracer_name in self._tracers:
            elapsed_time = time.time() - self._tracers[tracer_name]
            if message_template:
                print(message_template.format(elapsed_time))
            del self._tracers[tracer_name]
            return elapsed_time
        else:
            print(f'{tracer_name} is not being traced.')