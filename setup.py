from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="apng2gif",
    version="1.0",
    author="ThanatosDi",
    author_email="ThanatosDi@kttsite.com",
    description="convert apng to gif.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThanatosDi/APNG2GIF",
    packages=find_packages(),
    install_requires=[
        'apng==0.3.3',
        'Pillow>=6.2.0'
    ],
    entry_points={
        'console_scripts': [
            'apng2gif=apng2gif:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
)