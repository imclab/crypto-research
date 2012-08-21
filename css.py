
import argparse, base64, sys

def slurp(stream):
    return stream.read()

# TODO: Implement
def reverse(key):
    return key

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

def run():
    parser=argparse.ArgumentParser(description='''
      Content Scrambling System
    '''.strip())
    parser.add_argument('action',choices=['enc','dec'],
                        help='encrypt or decrypt')
    parser.add_argument('key',help='the key')
    parser.add_argument('-f','--file',dest='file',
                        help='file to act on')
    options=parser.parse_args()
    if options.file:
        stream=open(options.file,'r')
    else:
        stream=sys.stdin
    input_bytes=slurp(stream).encode()
    init_state=init(input_bytes)
    print(options.key)
    print(init_state)

if __name__=='__main__':
    run()
