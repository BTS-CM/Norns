from bitshares import BitShares
bitshares = BitShares()
bitshares.wallet.create("LOCAL_WALLET_PASSWORD") # Doesn't need to be the same password as your witness wallet.
bitshares.wallet.unlock("LOCAL_WALLET_PASSWORD")
bitshares.wallet.addPrivateKey("PRICE_FEED_PUBLISHER_ACTIVE_KEY") # Price feed publisher's active key.
