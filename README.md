# sync-py

These are python scripts for doing what the ```rsync link-dest``` does, but the difference is that the scripts copy the symlinks instead of creating hard links to the symlinks. Creating hard links to symlinks causes an error. This is a log file ```logs/python_script.log``` from the python scripts.

## How they work

```python3 main.py -b "backup dir"  -s "source dir"  -d "destination dir"```

1. Compare files in the source directory to files in the backup directory  
2. Create hard links (in the destination directory) unchanged files to backup     
3. Copy changed files from the source directory to the destination directory
4. Create symlinks to the aligned files. (e.g. ```bismark/some.fa -> ../../sequence/some.fa   ```)

## To Do list

* [ ] Create a dry run function if possible
* [ ] Refactor for a name of variables and functions
* [ ] Integrate these files into a snakemake pipeline 
