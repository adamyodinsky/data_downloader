from fredapi import Fred

class FredExtension(Fred):
    def get_series_first_release_by_dates(self, series_id, realtime_start=None, realtime_end=None):
        df = self.get_series_all_releases(series_id, realtime_start=realtime_start, realtime_end=realtime_end)
        first_release = df.groupby('date').head(1)
        data = first_release.set_index('date')['value']
        return data


