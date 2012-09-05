
import argparse, base64, sys

def slurp(stream):
    return stream.read()

def reverse(byt):
    res=0
    for x in range(8):
        if byt & (1<<(7-x)) > 0:
            res |= 1<<x
    return res

# Initialize state machine
def init(key):
    lfsr1=reverse(key[0] << 9) \
        | 0x100 \
        | reverse(key[1])
    lfsr2=(reverse(key[2] & 0x07) << 17) \
        | 0x00200000 \
        | (reverse(key[2] & 0xf8) << 16) \
        | (reverse(key[3]) << 8) \
        | reverse(key[4])
    cc=0
    return [lfsr1, lfsr2, cc]

def _lfsr1(lfsr1):
    lfsr1=(lfsr1<<9) | (lfsr1 >> 8)
    bits=lfsr1 & 0x03fc0
    product = (bits << 3) ^ (bits << 6) ^ (bits << 9)
    lfsr1 ^= product
    lfsr1 &= 0x1ffff
    return lfsr1

def _lfsr2(lfsr2):
    left8=lfsr2 ^ (lfsr2 >> 3) ^ (lfsr2 >> 4) ^ (lfsr2 >> 12)
    lfsr2=(left8<<17) | (lfsr2 >> 8)
    lfsr2 &= 0x1ffffff
    return lfsr2

def gen_lfsrbyte(lfsr1,lfsr2,cc,mode):
    while True:
        lfsr1=_lfsr1(lfsr1)
        lfsr2=_lfsr2(lfsr2)
        h1=0xff if (mode & 1) else 0x00
        h2=0xff if (mode & 2) else 0x00
        print(lfsr1,lfsr2,h1,h2)
        s=((lfsr1 >> 9) ^ h1) + ((lfsr2 >> 17) ^ h2) + cc
        cc=s>>8
        yield s & 0xff

def run():
    parser=argparse.ArgumentParser(description='''
      Content Scrambling System
    '''.strip())
    parser.add_argument('action',choices=['enc','dec'],
                        help='encrypt or decrypt')
    parser.add_argument('key',help='the key')
    parser.add_argument('-m','--mode',dest='mode')
    parser.add_argument('-o','--out',dest='output')
    parser.add_argument('-f','--file',dest='file',
                        help='file to act on')
    options=parser.parse_args()
    mode=int(options.mode)
    if options.file:
        stream=open(options.file,'r')
    else:
        stream=sys.stdin
    input_bytes=slurp(stream).encode()
    key=None
    if len(options.key) == 10:
        tmp=options.key
        key=[]
        for x in range(0,10,2):
            key.append(int(tmp[x:x+2],16))
    if key:
        init_state=init(key)
        init_state.append(mode)
        css_gen=gen_lfsrbyte(*init_state)
        res=bytearray()
        for by in input_bytes:
            xor=next(css_gen)
            res.append(xor ^ by)
        if options.output:
            with open(options.output,'wb') as f:
                f.write(res)
        else:
            print(bytes(res))
    else:
        print('no key')
    
    

if __name__=='__main__':
    run()
