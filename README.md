Image databases recorded from around the University of Sussex campus using our RC car robot. Data includes images from a Kodak PixPro camera, as well as IMU and GPS information.

The image databases are in the same form used elsewhere on the Brains on Board project (e.g. [BoB robotics](../bob_robotics)). In brief, that means that each database is comprised of a series of image files, which are described in the ``database_entries.csv`` file (e.g. see [here](2020-11-04/dataset1/database_entries.csv) for example). Each line of the CSV file contains coordinates and sensor readings corresponding to when a given image was recorded. For example code, see [here](example_code.ipynb).

Note that you probably want the unwrapped versions of the databases which are in the folders whose names start with ``unwrapped_*``: these contain the unwrapped versions of the panoramic images.
