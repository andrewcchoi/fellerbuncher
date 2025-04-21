# Modern Python Logging
[source: mcoding](https://github.com/mCodingLLC/VideosSampleCode/tree/master/videos/135_modern_logging)
This repo contains the code for this video: https://youtu.be/9L77QExPmI0

## Python Version Compatibility Warning
- To fully follow this video, you will need Python 3.12+. Most of the code can be adapted for lower versions with minor changes.
- The contained logging configs are *INCORRECT* for Python 3.8 or below.
  - This is because "root" was not added as a synonym for the root logger until Python 3.9: https://docs.python.org/3/whatsnew/3.9.html.
  - In Python 3.8 and below, use the empty string "" instead of "root", or use the top-level key "root" instead of putting the root config under "loggers".
- The way of setting up the QueueHandler specified in the video only works in 3.12+. You will need to manually hook up your QueueListener in lower versions.