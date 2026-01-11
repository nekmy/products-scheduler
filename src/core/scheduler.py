class Scheduler:
    """
    Jobを内包するクラス.
    Jobとその開始タイムバケットのみを保持する.
    """

    def __init__(self):
        self.lines = []
        self.jobs = []

    @property
    def n_jobs(self):
        return len(self.jobs)

    @property
    def n_lines(self):
        return len(self.lines)

    def add_line(self, line):
        self.lines.append(line)

    def add_job(self, job):
        self.jobs.append(job)
