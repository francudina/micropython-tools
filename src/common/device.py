import gc
import os


class Memory:

    @staticmethod
    def free_flash_storage() -> float:
        """
        Free device flash storage in KB.
        Info: https://raspberrypi.stackexchange.com/questions/140902/useful-statistics-from-pi-pico
        """
        s = os.statvfs('/')
        return s[0]*s[3]/1024

    @staticmethod
    def used_ram_storage() -> (float, float):
        """
        Used and free device RAM memory in bytes.

        Returns
        -------
        float
            Number of bytes of heap RAM that are allocated by code, number of bytes of heap RAM that
            is available for Python code to allocate, or -1 if this amount is not known
        """
        return gc.mem_alloc(), gc.mem_free()

    @staticmethod
    def enable_gc(enable: bool):
        if enable:
            gc.enable()
        else:
            gc.disable()

    @staticmethod
    def collect():
        """
        Explicitly invoke the Garbage Collector to release unreferenced memory.
        """
        gc.collect()
