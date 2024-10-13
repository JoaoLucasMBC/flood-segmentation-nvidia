from sentinel_downloader import SentinelDownloader

downloader = SentinelDownloader(mode="json", config_file="config.json")
downloader.run()