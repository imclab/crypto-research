
import argparse, base64, sys

def slurp(stream):
    return stream.read()



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
    cipher_bytes=slurp(stream).encode()
    print(options.key)
    print(cipher_bytes)

if __name__=='__main__':
    run()
