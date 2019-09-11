#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

import platform
install_requires = ['mock', 'svgpathtools']
if platform.system() == 'Darwin':
    install_requires += 'PyObjC'
elif platform.system() == 'Linux':
    install_requires += ['dbus-python', 'Adafruit_Python_BluefruitLE']

setuptools.setup(
    name="WonderPy",
    version="0.1.0",
    author="Orion Elenzil",
    author_email="orion@makewonder.com",
    description="Python API for working with Wonder Workshop robots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/playi/WonderPy",
    packages=setuptools.find_packages(),
    package_data={'WonderPy': ['lib/WonderWorkshop/osx/*.dylib', 'lib/WonderWorkshop/linux_x64/*.so']},
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Framework :: Robot Framework",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 2.7",
    ),
    keywords=['robots', 'dash', 'dot', 'cue', 'wonder workshop', 'robotics', 'sketchkit',],
    test_suite='test',
    install_requires=install_requires,
    # this also requires pip install git+git://github.com/playi/Adafruit_Python_BluefruitLE@928669a#egg=Adafruit_BluefruitLE
)
