Plans:
- Implement CSS
- Break CSS
- Implement Knapsack algorithm
- Implement Blowfish?

# Attacking DVD
- Each DVD has a Title Key (`Tk`) which decrypts the content (actually, it may
  have more than one, but this detail isn't necessary for this discussion).

      Dec(Ciphertext, Tk) = Plaintext

- The Title Key is not stored on the disc directly. Instead, it is encrypted
  with any number of Player Keys (`Pk`). Each encryption of the Title Key is
  stored on the disc.

      Enc(Tk, Pk1) = Tk1
      [ ... ]
      Enc(Tk, Pkn) = Tkn

  By controlling the Player Keys assigned to DVD manufacturers, DVDs may be
  region-locked.

- After finding the Title Key by breaking one encryption, all Player Keys can
  be deciphered with a chosen plaintext attack

