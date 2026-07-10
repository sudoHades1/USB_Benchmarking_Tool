from pathlib import Path
from datetime import datetime

from usbdetect import USBMonitor
from benchmark import Benchmark

from report_builder import ReportBuilder
from html_report import HTMLReport
from csv_report import CSVReport

from config import Config


# Load configuration first
config = Config()

# Create services
monitor = USBMonitor()
bench = Benchmark(config.data)


print("========================================")
print(" USB Benchmark Station v0.1")
print("========================================")
print("Waiting for removable USB devices...\n")

for usb in monitor.wait_for_device():

    print(f"USB Device : {usb.device}")
    print(f"Mount Point: {usb.mountpoint}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    base_output = config.get("output", "directory", default="Results")
    output_dir = Path(base_output) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Using output directory: {output_dir}")
    print(f"Application: {config.get('application', 'name')}")
    print("\nStarting benchmark...\n")

    try:
        # Run all fio profiles
        bench.run(usb, output_dir)

        print("\n✓ Benchmark completed successfully.")

        # Build reports
        builder = ReportBuilder()
        html = HTMLReport()
        csvr = CSVReport()

        summary = builder.build_summary(output_dir)

        builder.save_summary_json(summary, output_dir)

        csvr.export(summary, output_dir)

        html.render(summary, usb, output_dir)

        print("✓ Reports generated.")

    except Exception as e:
        print(f"\n✗ Benchmark failed: {e}")

    print("\nWaiting for next USB...\n")

