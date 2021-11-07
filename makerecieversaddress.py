from algosdk import account, mnemonic

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print ("My address: {}".format(address))
    print ("My private key: {}". format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

generate_algorand_keypair()

#My address: QLCTCCR2O4YLGN2JME5OFHGPYSZYDJXGTPV33HMUELGDOC7AL4Q7HHSZJ4
#My private key: J+rl/Bg/H7X6SvvjHIEvwMN+IQJCz5rlHAZHOlKELt2CxTEKOncwszdJYTrinM/Es4Gm5pvrvZ2UIsw3C+BfIQ==
#My passphrase: eager nut lazy various dinosaur pull fit win organ afford blind despair work marriage avoid soon rebuild inform loan piece piece patient truly absorb comic
