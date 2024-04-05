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

- Enable direct installation via PyPI.
- Implement branch separation, potentially retrieving this information directly from the local Git repository.
- Integrate with the S3 API.
- Directly integrate with the APIs of major cloud services, removing the necessity of installing the cloud service's - application on the local machine.

## Usage

Define a folder on your device to be the local LFS repository with the -d flag:

To push information to the local LFS repository:
```bash
local_lfs push -d path/to/lfs_dest_folder
```

You can also use the -i flag to specify only certain folders to be included in the push:

```bash
local_lfs push -d path/to/lfs_dest_folder -i path/to/include_folder, path/to/include_folder2
```

By default, the source path is set to the current directory, but you can change it by passing a different path as a positional argument:

```bash
local_lfs push path/to/src_folder -d path/to/lfs_dest_folder
```

To pull changes from the local repository:

```bash
local_lfs pull -d path/to/lfs_dest_folder
```

To check changes compared to the local repository (Not Implemented):
```bash
local_lfs status -d path/to/lfs_dest_folder
```

## Pyproject.toml

You can also specify all arguments in the `pyproject.toml` file of your project:

```toml
[tool.local_lfs]
src_path = "."
dest_path= "path/to/lfs_dest_folder"
include=["tests/fixtures/", "tests/fixtures2/"]
```

After that, you can run the commands without any flags:

```bash
local_lfs push
```



