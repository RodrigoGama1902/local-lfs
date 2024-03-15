# Local LFS

Local LFS is a Python package that offers a simple and cost-free alternative to Git LFS (Large File Storage). 

It arose from the need to develop applications requiring heavy binary files for testing validation (such as 3D files), where tracking these heavy files alongside the Git repository became impractical. 

The solution was to use cloud storage (OneDrive, Drive, Dropbox) exclusively for files that couldn't be tracked by Git, and provide an easy and practical way to sync these files with the Git repository from any device sharing the same cloud. 

## Requirements

Any cloud application allowing access through the device's file manager.

## Limitations

- Since these files are primarily static and binary, the system doesn't track changes in the files, only their latest state.
- Does not allow separation by branches

## Installation

```bash
git clone https://github.com/RodrigoGama1902/local-lfs.git
pip install .
```

## Future Implementations

- Allow direct installation via PyPI
- Enable separation by branches (Maybe get this info directly from the local Git repository)
- Integrate with S3 API
- Directly integrate with the APIs of major cloud services, eliminating the need to have the cloud service's application installed on the machine

## Usage

Define a folder on your device to be the local LFS repository.

To push information to the local repository:
```bash
local_lfs push -d path/to/lfs_dest_folder
```

To pull changes from the local repository:
```bash
local_lfs pull -d path/to/lfs_dest_folder
```

To check changes compared to the local repository:
```bash
local_lfs status -d path/to/lfs_dest_folder
```