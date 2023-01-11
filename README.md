# Rename

This is a tool for renaming files in Linux.

## Syntax

```
$ rename <file_name> <new_name>
$ rename [options]
```

### Options

| Option | Description |
|:---|:---|
| -e \<ext1> \<ext2> | Change the extension of the files from \<ext1> to \<ext2>. |
| -h, --help | Display help. |
| -n \<ext> | Enumerate the files with extension \<ext>, starting from zero. |
| -v, --version | Display program version info. |

## Usage examples

Rename `file1.txt` to `file2.txt`:
```
$ rename file1.txt file2.txt
```

Rename `*.jpeg` to `*.jpg`:
```
$ rename -e jpeg jpg
```

Enumerate all the jpg files:
```
$ rename -n jpg
```
