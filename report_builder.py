from parser import FioParser
from pathlib import Path
import json


class ReportBuilder:

    def __init__(self):
        self.parser = FioParser()


    def build_summary(self, result_dir: Path):

        summary = {}

        raw_dir = result_dir / "raw"

        if not raw_dir.exists():
            return summary


        for file in raw_dir.glob("*.json"):

            if file.name == "summary.json":
                continue


            name = file.stem

            # Remove run number
            # seq1m_q8t1_read_run1
            # becomes
            # seq1m_q8t1_read

            parts = name.rsplit("_run", 1)

            if len(parts) != 2:
                continue


            profile = parts[0]


            bandwidth = self.parser.parse_file(
                file
            )


            if profile.endswith("_read"):

                test = profile[:-5]

                if test not in summary:
                    summary[test] = {
                        "read_mb_s": 0,
                        "write_mb_s": 0
                    }

                summary[test]["read_mb_s"] = bandwidth


            elif profile.endswith("_write"):

                test = profile[:-6]

                if test not in summary:
                    summary[test] = {
                        "read_mb_s": 0,
                        "write_mb_s": 0
                    }

                summary[test]["write_mb_s"] = bandwidth


        return summary



    def save_summary_json(
        self,
        summary,
        result_dir
    ):

        path = result_dir / "summary.json"

        with open(
            path,
            "w"
        ) as f:

            json.dump(
                summary,
                f,
                indent=4
            )


        return path

