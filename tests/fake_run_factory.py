class FakeRunFactory:
    def __init__(self):
        self.created_run = 0

        self.runs = []
        self.stats = dict(
            run_names=[],
            distances=[],
            elapsed_times=[],
            average_speeds=[],
            elevation_gains=[],
            run_ids=[],
            average_heart_rates=[])

    def __call__(self, quantity=1):
        for _ in range(0, quantity):
            self.created_run += 1

            self.stats['run_names'].append('title' + str(self.created_run))
            self.stats['distances'].append(0.1 + self.created_run)
            self.stats['elapsed_times'].append(0.3 + self.created_run)
            self.stats['average_speeds'].append(0.4 + self.created_run)
            self.stats['elevation_gains'].append(0.5 + self.created_run)
            self.stats['run_ids'].append(self.created_run)

            self.runs.append(dict(
                title='title' + str(self.created_run),
                description='description' + str(self.created_run),
                strava_id=-self.created_run,
                distance=0.1 + self.created_run,
                startdate=0.2 + self.created_run,
                elapsed_time=0.3 + self.created_run,
                average_speed=0.4 + self.created_run,
                total_elevation_gain=0.5 + self.created_run,
                runner_id=0,
                id=self.created_run))
