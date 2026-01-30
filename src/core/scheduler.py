class Scheduler:
    """
    Jobを内包するクラス.
    Jobとその開始タイムバケットのみを保持する.
    """

    def __init__(self):
        self.lines = []
        self.job_map = {}

    @property
    def n_jobs(self):
        return len(self.jobs)

    @property
    def n_lines(self):
        return len(self.lines)

    def add_line(self, line):
        self.lines.append(line)

    def add_job(self, job_id, job):
        assert (
            not job_id in self.job_map.keys()
        ), "job_id={0}はすでに存在します.".format(job_id)
        self.job_map[job_id] = job
