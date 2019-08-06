import hashlib
from pathlib import Path

wordlist = Path('wordlist_xpto.txt').open(mode='r').readlines()
xpto='21e32f5321cad49ab4cf78ba5ed231e0f36d0c78d34108fda1be939f33fba149'

try:
    for hashlib_al in hashlib.algorithms_available:
        hn = hashlib.new(hashlib_al)        
        for w in wordlist:
            hn.update(bytes(w.strip(), 'utf-8'))        
            if getattr(hn, 'hexdigest'):
                hexdigest = str(hn.hexdigest())
                if hexdigest:
                    print(hexdigest, hashlib_al)
                    if (hexdigest == xpto):
                        print('MY PASSWORD:', w)
except ValueError as err:
    print(err)