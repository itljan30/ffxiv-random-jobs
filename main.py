import os
import pandas
import pathlib
import random
import sys
from collections import defaultdict

def read_jobs_files(f: str) -> dict[str, list[tuple[str, int]]]:
    root_dir = pathlib.Path(__file__).parent
    jobs_file = root_dir / "csv" / f"{f}.jobs"

    if not os.path.exists(jobs_file):
        sys.exit(f"ERROR: {jobs_file} not found")

    with open(jobs_file, "r") as file:
        reader = pandas.read_csv(file)

    res = defaultdict(list[tuple[str, str]])
    columns = reader.columns
    for _, row in reader.iterrows():
        job_name = row["JOB"]
        for col in columns:
            if col != "JOB":
                if row[col] != "-":
                    player_data = (job_name, str(row[col]))
                    res[str(col)].append(player_data)

    return res

def get_results(data: dict[str, list[tuple[str, int]]]) -> dict[str, str]:
    available_jobs = {player : [job for job, _weight in jobs] for player, jobs in data.items()}
    sorted_players = sorted(available_jobs.keys(), key=lambda p: len(available_jobs[p]))

    assigned = set()
    res = {}
    for player in sorted_players:
        if player.lower() == "roman":
            res["roman"] = "MCH but without pants"
            assigned.add("MCH")
            continue
        available = [job for job in available_jobs[player] if job not in assigned]
        if not available:
            return get_results(data)
        chosen_job = random.choice(available)
        res[player] = chosen_job
        assigned.add(chosen_job)

    return res


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} NAME")

    file = sys.argv[1]
    data = read_jobs_files(file)
    results = get_results(data)
    print(results)

if __name__ == "__main__":
    main()
