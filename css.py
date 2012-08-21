
import argparse, base64, sys

def slurp(stream):
    return stream.read()

# TODO: Implement
def reverse(key):
    return key

def run():
    parser=argparse.ArgumentParser(description='''
      Content Scrambling System
    '''.strip())
    parser.add_argument('action',choices=['enc','dec'],
                        help='encrypt or decrypt')
    parser.add_argument('-f','--file',dest='file',
                        help='file to act on')
    options=parser.parse_args()
    if options.file:
        stream=open(options.file,'r')
    else:
        stream=sys.stdin
    cipher_bytes=slurp(stream).encode()
    print(cipher_bytes)

if __name__=='__main__':
    run()
