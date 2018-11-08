# getpdftitle
getpdftitle extracts titles from pdf files

## Usage
getpdftitle [-h] [-n] [-s] [filename [filename ...]]

Extracts title from pdf file

positional arguments:
  filename    Extracts title from file.pdf. Extracts from all pdf files in the
              current directory if a filename is not specified

optional arguments:
  -h, --help  show this help message and exit
  -n, --name  Include filename in output
  -s, --stat  Show statistics of files parsed

## Requirements
sudo pip install pdfrw

## Author
[Cibin Joseph](https://github.com/cibinjoseph) (cibinjoseph92@gmail.com).

## License
MIT License
See [LICENSE](LICENSE) for full text.
