import multiprocessing
import platform

if platform.system() in ("Darwin", "Windows"):
    multiprocessing.set_start_method("fork", force=True)
