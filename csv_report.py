import csv


class CSVReport:

    def export(
        self,
        summary,
        result_dir
    ):

        path = result_dir / "summary.csv"


        with open(
            path,
            "w",
            newline=""
        ) as f:


            writer = csv.writer(f)


            writer.writerow(
                [
                    "Profile",
                    "Read MB/s",
                    "Write MB/s"
                ]
            )


            for profile, values in summary.items():

                writer.writerow(
                    [
                        profile,
                        values["read_mb_s"],
                        values["write_mb_s"]
                    ]
                )


        return path

