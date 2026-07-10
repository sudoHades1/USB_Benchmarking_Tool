from dataclasses import dataclass
from pathlib import Path
import psutil
import subprocess
import os


@dataclass
class USBDevice:

    device: str
    mountpoint: str

    vendor: str = "Unknown"
    model: str = "Unknown"
    serial: str = "Unknown"

    filesystem: str = "Unknown"

    capacity: int = 0

    vid: str = "Unknown"
    pid: str = "Unknown"

    def discover(self):

        self._filesystem()

        self._capacity()

        self._udev()

        return self

    def _filesystem(self):

        for part in psutil.disk_partitions():

            if part.device == self.device:

                self.filesystem = part.fstype

                return

    def _capacity(self):

        try:

            self.capacity = psutil.disk_usage(
                self.mountpoint
            ).total

        except Exception:
            self.capacity = 0

    def _udev(self):

        try:

            output = subprocess.check_output(
                [
                    "udevadm",
                    "info",
                    "--query=property",
                    "--name",
                    self.device
                ],
                text=True
            )

            for line in output.splitlines():

                if "=" not in line:
                    continue

                key, value = line.split("=", 1)

                if key == "ID_VENDOR":
                    self.vendor = value

                elif key == "ID_MODEL":
                    self.model = value

                elif key == "ID_SERIAL_SHORT":
                    self.serial = value

                elif key == "ID_VENDOR_ID":
                    self.vid = value

                elif key == "ID_MODEL_ID":
                    self.pid = value

        except Exception:
            pass

    @property
    def capacity_gb(self):

        return round(self.capacity / (1024**3), 2)

    @property
    def benchmark_file(self):

        return Path(self.mountpoint) / "usbbench.tmp"
