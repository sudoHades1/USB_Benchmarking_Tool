from pathlib import Path
import yaml


class Config:

    def __init__(self, filename="config.yaml"):

        self.filename = Path(filename)

        if not self.filename.exists():
            raise FileNotFoundError(
                f"Missing config file: {self.filename}"
            )

        with open(self.filename, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f) or {}


    def get(self, *keys, default=None):
        """
        Retrieve nested configuration values.

        Example:
            config.get("benchmark", "runs")
            config.get("application", "name")
        """

        value = self.data

        for key in keys:

            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default

            if value is None:
                return default

        return value


    # Application settings
    @property
    def application_name(self):
        return self.get(
            "application",
            "name",
            default="USB Benchmark Station"
        )


    @property
    def application_version(self):
        return self.get(
            "application",
            "version",
            default="1.0.0"
        )


    # Output paths
    @property
    def output_dir(self):

        path = Path(
            self.get(
                "output",
                "directory",
                default="Results"
            )
        )

        path.mkdir(parents=True, exist_ok=True)

        return path


    # Benchmark settings
    @property
    def benchmark_runs(self):
        return self.get(
            "benchmark",
            "runs",
            default=1
        )


    @property
    def test_file_size(self):
        return self.get(
            "benchmark",
            "test_file_size",
            default="1G"
        )


    @property
    def benchmark_profiles(self):
        return self.get(
            "benchmark",
            "profiles",
            default=[]
        )


    @property
    def cleanup_enabled(self):
        return self.get(
            "benchmark",
            "cleanup",
            default=True
        )


    # Report settings
    @property
    def reports(self):
        return self.get(
            "reports",
            default={}
        )


    # FIO settings
    @property
    def fio_binary(self):
        return self.get(
            "fio",
            "binary",
            default="fio"
        )


    @property
    def fio_output_format(self):
        return self.get(
            "fio",
            "output_format",
            default="json"
        )


    # USB settings
    @property
    def removable_only(self):
        return self.get(
            "usb",
            "detect_removable_only",
            default=True
        )


    # Logging settings
    @property
    def log_file(self):
        return self.get(
            "logging",
            "file",
            default="usbbench.log"
        )

