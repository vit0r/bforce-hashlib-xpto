##### gen wordlist

´
apt install crunch -y
´

´
crunch 4 4 ABCDEFGHIJKLMNOPQRSTUVWXYZ > wordlist_xpto.txt
´

#### how to use

´
python decode_xpto.py your-hash-code wordlist.txt
´