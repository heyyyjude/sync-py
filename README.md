# sync-py

These are python scripts for doing what the ```rsync link-dest``` does, aside from creating symlinks instead of creating hard links to symbolic links.
Rsync doesn't create hard links to symlinks, so these scripts are used to handle this issue. The output is the same.  

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
