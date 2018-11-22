from setuptools import setup, find_packages
from beepbeep.statistics import __version__


setup(name='beepbeep-statistics',
      version=__version__,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      [console_scripts]
      beepbeep-statistics = beepbeep.statistics.run:main
      """)
