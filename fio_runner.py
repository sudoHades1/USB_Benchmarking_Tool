import os
import shutil
import subprocess
import tempfile
from pathlib import Path


class FioRunner:
    """
    YAML driven fio benchmark runner.

    Config example:

    benchmark:
      test_file_size: 1G
      profiles:
        seq1m_q8t1_read:
          rw: read
          bs: 1M
          iodepth: 8
          numjobs: 1

    fio:
      runtime: 10
      ramp_time: 5
      direct: 1
      ioengine: libaio
    """

    def __init__(self, config: dict):

        self.config = config

        self.benchmark_cfg = config.get(
            "benchmark",
            {}
        )

        self.fio_cfg = config.get(
            "fio",
            {}
        )


        # fio binary

        self.binary = self.fio_cfg.get(
            "binary",
            "fio"
        )


        self.output_format = self.fio_cfg.get(
            "output_format",
            "json"
        )


        self.temp_filename = self.fio_cfg.get(
            "temp_filename",
            "usbbench.tmp"
        )


        # benchmark

        self.test_size = self.benchmark_cfg.get(
            "test_file_size",
            "1G"
        )


        self.required_free_space_gb = self.benchmark_cfg.get(
            "required_free_space_gb",
            2
        )


        self.profiles = self.benchmark_cfg.get(
            "profiles",
            {}
        )


        # fio settings

        self.ioengine = self.fio_cfg.get(
            "ioengine",
            "libaio"
        )


        self.direct = int(
            self.fio_cfg.get(
                "direct",
                1
            )
        )


        self.runtime = self.fio_cfg.get(
            "runtime",
            10
        )


        self.ramp_time = self.fio_cfg.get(
            "ramp_time",
            5
        )


        self.time_based = int(
            self.fio_cfg.get(
                "time_based",
                1
            )
        )


        self.group_reporting = int(
            self.fio_cfg.get(
                "group_reporting",
                1
            )
        )


        self.invalidate_cache = int(
            self.fio_cfg.get(
                "invalidate_cache",
                True
            )
        )


        self.randrepeat = int(
            self.fio_cfg.get(
                "randrepeat",
                0
            )
        )


        self._validate()



    def run(
        self,
        profile_name: str,
        mountpoint: str,
        output_file: Path
    ):

        if profile_name not in self.profiles:

            raise KeyError(
                f"Unknown benchmark profile: {profile_name}"
            )


        profile = self.profiles[profile_name]


        mountpoint = Path(
            mountpoint
        )


        test_file = (
            mountpoint /
            self.temp_filename
        )


        self._check_free_space(
            mountpoint
        )


        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        fio_job = self._create_job_file(
            profile_name,
            profile,
            test_file
        )


        command = [

            self.binary,

            str(fio_job),

            f"--output-format={self.output_format}"

        ]


        try:

            with output_file.open(
                "w",
                encoding="utf-8"
            ) as output:


                result = subprocess.run(

                    command,

                    stdout=output,

                    stderr=subprocess.PIPE,

                    text=True

                )


            if result.returncode != 0:

                raise RuntimeError(
                    result.stderr
                )


        finally:

            fio_job.unlink(
                missing_ok=True
            )



    def _create_job_file(
        self,
        profile_name,
        profile,
        test_file
    ):


        job = f"""

[global]

filename={test_file}

ioengine={self.ioengine}

direct={self.direct}

time_based={self.time_based}

runtime={self.runtime}

ramp_time={self.ramp_time}

group_reporting={self.group_reporting}

invalidate={self.invalidate_cache}

randrepeat={self.randrepeat}


[{profile_name}]

rw={profile.get("rw","read")}

bs={profile.get("bs","1M")}

iodepth={profile.get("iodepth",1)}

numjobs={profile.get("numjobs",1)}

size={self.test_size}

"""


        temp = tempfile.NamedTemporaryFile(

            mode="w",

            suffix=".fio",

            delete=False

        )


        temp.write(
            job
        )


        temp.close()


        return Path(
            temp.name
        )



    def prepare(
        self,
        mountpoint
    ):

        """
        Creates a real allocated benchmark file.
        Avoids sparse file results.
        """


        mountpoint = Path(
            mountpoint
        )


        test_file = (
            mountpoint /
            self.temp_filename
        )


        if test_file.exists():

            return


        print(
            "Creating benchmark file..."
        )


        block = (
            b"\0" *
            (1024 * 1024)
        )


        remaining = self._size_to_bytes(
            self.test_size
        )


        with open(
            test_file,
            "wb"
        ) as f:


            while remaining > 0:


                size = min(
                    remaining,
                    len(block)
                )


                f.write(
                    block[:size]
                )


                remaining -= size



        os.sync()



    def cleanup(
        self,
        mountpoint
    ):


        test_file = (

            Path(mountpoint)
            /
            self.temp_filename

        )


        try:

            test_file.unlink(
                missing_ok=True
            )

        except Exception:

            pass



    def _check_free_space(
        self,
        mountpoint
    ):


        stat = os.statvfs(
            mountpoint
        )


        free = (

            stat.f_bavail *
            stat.f_frsize

        )


        required = (

            self.required_free_space_gb *
            (1024 ** 3)

        )


        if free < required:

            raise RuntimeError(

                f"Not enough free space. "
                f"Required {self.required_free_space_gb}GB"

            )



    def _size_to_bytes(
        self,
        size
    ):


        units = {

            "K":1024,

            "M":1024**2,

            "G":1024**3

        }


        return int(
            size[:-1]
        ) * units[
            size[-1].upper()
        ]



    def _validate(
        self
    ):


        if shutil.which(
            self.binary
        ) is None:

            raise FileNotFoundError(

                f"fio executable '{self.binary}' not found"

            )


        if not self.profiles:

            raise ValueError(

                "No benchmark profiles configured"

            )

