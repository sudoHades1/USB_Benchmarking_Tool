from fio_runner import FioRunner


class Benchmark:

    def __init__(self, config):

        self.config = config

        self.runner = FioRunner(
            config
        )


    def run(
        self,
        usb,
        output_dir
    ):

        benchmark = self.config.get(
            "benchmark",
            {}
        )


        profiles = benchmark.get(
            "profiles",
            {}
        )


        runs = benchmark.get(
            "runs",
            5
        )


        if not isinstance(profiles, dict):

            raise ValueError(
                "benchmark.profiles must be a dictionary in config.yaml"
            )


        # Create benchmark file once

        self.runner.prepare(
            usb.mountpoint
        )


        try:

            for profile_name in profiles.keys():

                print(
                    f"\n{profile_name}"
                )


                for run in range(
                    1,
                    runs + 1
                ):


                    print(
                        f"Run {run}/{runs}"
                    )


                    output_file = (

                        output_dir
                        /
                        "raw"
                        /
                        f"{profile_name}_run{run}.json"

                    )


                    self.runner.run(

                        profile_name,

                        usb.mountpoint,

                        output_file

                    )


        finally:

            if benchmark.get(
                "cleanup",
                True
            ):


                self.runner.cleanup(
                    usb.mountpoint
                )

