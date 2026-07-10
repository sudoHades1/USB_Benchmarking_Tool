import json


class FioParser:

    def parse_file(self, path):

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        jobs = data.get("jobs", [])

        if not jobs:
            return 0


        read_bw = 0
        write_bw = 0


        for job in jobs:

            read_bw += (
                job.get("read", {})
                .get("bw", 0)
            )

            write_bw += (
                job.get("write", {})
                .get("bw", 0)
            )


        # Convert KiB/s to MB/s
        if read_bw > 0:
            return round(
                read_bw / 1024,
                2
            )

        if write_bw > 0:
            return round(
                write_bw / 1024,
                2
            )


        return 0

