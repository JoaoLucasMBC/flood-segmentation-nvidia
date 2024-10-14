from sentinel_downloader.json_runner import JSONRunner
from sentinel_downloader.cli import CLI

class SentinelDownloader():
    def __init__(self, mode="cli", config_file=None, cli_args=None):
        """
        Initialize SentinelDownloader.

        Args:
            mode (str): Either 'cli' or 'json'. Defaults to 'cli'.
            config_file (str): Path to the JSON config file. Required if mode is 'json'.
            cli_args (list): Command line arguments. Required if mode is 'cli'.
        """

        self.mode = mode
        self.config_file = config_file
        self.cli_args = cli_args

        if self.mode == "json":
            if not self.config_file:
                raise ValueError("A config file must be provided for JSON mode.")
            self.runner = JSONRunner(self.config_file)
        elif self.mode == "cli":
            if not self.cli_args:
                raise ValueError("CLI arguments must be provided for CLI mode.")
            self.runner = CLI(self.cli_args)
        else:
            raise ValueError("Mode must be either 'cli' or 'json'.")
        
    def run(self):
        """
        Run the SentinelDownloader.
        """
        self.runner.run()