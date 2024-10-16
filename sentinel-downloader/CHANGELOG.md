# Changelog

## [2.0.0] - 2024-10-16
### Added 
- Progress bar for downloading data.
- Added a info.txt file with information about the download.

### Fixed
- Fixed issue with saving images with wrong name, now it saves the i and j for each image.
- Fixed so that input coordinates are in the format: `lat,lon,lat,lon`. From nw to se. 

## [1.0.7] - 2024-10-15
### Added 
- Added support to removed directory due to interruption, siginit. 

## [1.0.6] - 2024-10-15
### Fixed
- Fixed issue with imput coordinates, now they follow the format: `lat,lon,lat,lon`. From nw to se.

## [1.0.5] - 2024-10-15
### Added
- Added sentinel-cli script to download Sentinel-1 and Sentinel-2 data.

## [1.0.0] - 2024-10-15
### Added
- Initial version of the project supporting downloading of Sentinel-1 and Sentinel-2.
- Sentinel1: Use of google earth engine API to download Sentinel-1 data.
- Sentinel2: Use of sentinelhub-py API to download Sentinel-2 data.