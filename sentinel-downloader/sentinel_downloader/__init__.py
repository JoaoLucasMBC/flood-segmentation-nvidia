# Classes that should be exposed
from sentinel_downloader.sentinel_downloader import SentinelDownloader  
from sentinel_downloader.cli import CLI
from sentinel_downloader.json_runner import JSONRunner

# What will be available if users import *
__all__ = [
    "SentinelDownloader", 
    "CLI",                 
    "JSONRunner",          
]