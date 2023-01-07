from bitshares.asset import Asset
from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance
from bitshares.price import Price
from bitshares.market import Market
from bitsharesapi.websocket import BitSharesWebsocket
import pendulum
import math

def norn_feed(amplitude, reference_timestamp, current_timestamp, period, phase_offset):
	"""
	Given the reference timestamp, the current timestamp, the period (in days), the phase (in days), the reference asset value (ie 1.00) and the amplitude (> 0 && < 1), output the current value.
	"""
	waveform = math.sin(((((current_timestamp - (reference_timestamp + phase_offset))/period) % 1) * period) * ((2*math.pi)/period)) # Only change for an alternative HERTZ ABA.
	return 1 + (amplitude * waveform)

def publish_wyrd(block_param):
	"""
	Triggers every 3 seconds.
	Calculates then publishes the feeds for urthr, verthandi and skuld.
	"""
	print("publishing")
	reference_timestamp = pendulum.parse("2015-10-13T14:12:24+00:00").timestamp() # Retrieving the Bitshares 2.0 genesis block timestamp
	current_timestamp = pendulum.now().timestamp()

	urthr_value = norn_feed(
		0.05303030303, # amplitude
		reference_timestamp,
		current_timestamp,
		86400 * 28, # period
		0 # phase offset
		)
	print("urthr value established")

	verthandi_value = norn_feed(
		0.05303030303, # amplitude
		reference_timestamp,
		current_timestamp,
		86400 * 28, # period
		86400 * 9.33 # phase offset
		)
	print("verthandi value established")

	skuld_value = norn_feed(
		0.05303030303, # amplitude
		reference_timestamp,
		current_timestamp,
		86400 * 28, # period
		86400 * 18.66 # phase offset
		)
	print("skuld value established")

	#print("urthr:" + str(urthr_value) + " verthandi:" + str(verthandi_value) + " skuld:" + str(skuld_value))

	urthr = Price(urthr_value, "BTS/URTHR")
	verthandi = Price(verthandi_value, "BTS/VERTHANDI")
	skuld = Price(skuld_value, "BTS/SKULD")

	print("values applied to bitasset price objects")

	wallet_password = "LOCAL_WALLET_PASSWORD"
	urthr.bitshares.wallet.unlock(wallet_password)
	verthandi.bitshares.wallet.unlock(wallet_password)
	skuld.bitshares.wallet.unlock(wallet_password)

	print("wallet unlocked")

	urthr.bitshares.publish_price_feed(
		"URTHR",
		urthr,
		cer=urthr*0.8, # Setting in line with Wackou's price feed scripts
		mssr=101,
		mcr=105,
		account="account_name"
	)

	verthandi.bitshares.publish_price_feed(
		"VERTHANDI",
		verthandi,
		cer=verthandi*0.8, # Setting in line with Wackou's price feed scripts
		mssr=101,
		mcr=105,
		account="account_name"
	)

	skuld.bitshares.publish_price_feed(
		"SKULD",
		skuld,
		cer=skuld*0.8, # Setting in line with Wackou's price feed scripts
		mssr=101,
		mcr=105,
		account="account_name"
	)
	print("completed feed")

if __name__ == "__main__":
	"""
	Script begins here
	"""
	print("Started")
	full_node_list = [
		"wss://eu.nodes.bitshares.ws", # Central Europe
		"wss://us.nodes.bitshares.ws", # U.S. West Coast
		"wss://sg.nodes.bitshares.ws", # Singapore
		"wss://bitshares.crypto.fans/ws", # Munich, Germany
		"wss://bit.btsabc.org/ws", # Hong Kong
		"wss://api.bts.blckchnd.com" # Falkenstein, Germany
		"wss://openledger.hk/ws", # Hong Kong
		"wss://bitshares.openledger.info/ws",
		"wss://bitshares-api.wancloud.io/ws", # China
		"wss://dex.rnglab.org", # Netherlands
		"wss://dexnode.net/ws", # Dallas, USA
		"wss://kc-us-dex.xeldal.com/ws", # Kansas City, USA
		"wss://la.dexnode.net/ws", # Los Angeles, USA
		"wss://citadel.li/node", # Iceland - Reykjavik
		"wss://bts.proxyhosts.info/wss", # Germany
		"wss://api.dex.trading/", # France - Paris
		"wss://api.open-asset.tech/ws" # Germany - Frankfurt
	]

	ws = BitSharesWebsocket(
	    full_node_list,
	    objects=["2.0.x", "2.1.x", "1.3.x"]
	)

	print("ws connection established")

	ws.on_block += publish_wyrd
	ws.run_forever()
