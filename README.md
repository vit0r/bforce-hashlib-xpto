# Get clean text from hashes with word list

```sh

apt install crunch -y
crunch 4 4 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ > wordlist_xpto.txt
python decode_xpto.py your-hash-code wordlist.txt

```
