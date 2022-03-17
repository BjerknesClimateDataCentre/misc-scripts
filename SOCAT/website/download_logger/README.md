The Carbon Portal wish to track usage of ICOS data. The ICOS data downloaded
through SOCAT is currently not tracked as usage of ICOS data.

The download_logger script will run daily and track downloads of ICOS data from
the SOCAT website and report this information the Carbon Portal. This tracking
 info will be registered at the relevant data collection at CP (the collection
 for that specific SOCAT region and version related to the download).

The tracking will only be for v2021 onwards. Initially, it will not track when
 someone downloads from the ncei link, only the bcdc mirror link.