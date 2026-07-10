import time
import pyudev
import psutil

from device import USBDevice

class USBMonitor:
    def __init__(self):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem="block")

    def wait_for_device(self):
        print("Waiting for removable USB storage...")

        for device in iter(self.monitor.poll, None):

            # Only care about newly added partitions
            if device.action != "add":
                continue

            if device.device_type != "partition":
                continue

            # Walk up the device tree until we find the USB device
            usb_parent = device.find_parent("usb", "usb_device")

            if usb_parent is None:
                # Not a USB device (could be NVMe, SATA, loopback, etc.)
                continue

            # Find the parent block disk (e.g. /dev/sdb)
            disk = device.find_parent("block", "disk")

            if disk is None:
                continue

            removable = disk.attributes.asstring("removable").strip()

            if removable != "1":
                continue

            mountpoint = self.wait_for_mount(device.device_node)

            if mountpoint is None:
                continue


            usb = USBDevice(
                device=device.device_node,
                mountpoint=mountpoint
            ).discover()

            yield usb 

    def wait_for_mount(self, device_node, timeout=15):
        """Wait until the partition is mounted."""

        end = time.time() + timeout

        while time.time() < end:

            for part in psutil.disk_partitions(all=False):

                if part.device == device_node:
                    return part.mountpoint

            time.sleep(0.5)

        return None
