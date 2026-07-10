from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class HTMLReport:

    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader("templates")
        )

    def render(self, summary, usb, result_dir):

        template = self.env.get_template("report.html")

        html = template.render(
            results=summary,
            device=usb.model,
            vendor=usb.vendor,
            serial=usb.serial,
            filesystem=usb.filesystem,
            capacity=usb.capacity_gb,
            timestamp=str(result_dir.name)
        )

        output_file = result_dir / "report.html"

        with open(output_file, "w") as f:
            f.write(html)

        return output_file
