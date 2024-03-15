from setuptools import setup, find_packages

setup(
    name="local_lfs",
    version="0.1",
    packages=find_packages(),
    package_dir={"local_lfs": "local_lfs"},
    entry_points={
        "console_scripts": [
            "local_lfs = local_lfs.__main__:main",
        ],
    },
    install_requires=[],
)
