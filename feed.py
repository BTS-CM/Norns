from pprint import pprint
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
	waveform = math.sin(((((current_timestamp - (hz_reference_timestamp + phase_offset))/period) % 1) * period) * ((2*math.pi)/period)) # Only change for an alternative HERTZ ABA.
	return 1 + ((amplitude * reference_asset_value) * waveform)


full_node_list = [
	"wss://eu.nodes.bitshares.works", #location: "Central Europe - BitShares Infrastructure Program"
	"wss://us.nodes.bitshares.works", #location: "U.S. West Coast - BitShares Infrastructure Program"
	"wss://sg.nodes.bitshares.works", #location: "Singapore - BitShares Infrastructure Program"
	"wss://bitshares.crypto.fans/ws", #location: "Munich, Germany"
	"wss://bit.btsabc.org/ws", #location: "Hong Kong"
	"wss://api.bts.blckchnd.com" #location: "Falkenstein, Germany"
	"wss://openledger.hk/ws", #location: "Hong Kong"
	"wss://bitshares-api.wancloud.io/ws", #location:  "China"
	"wss://dex.rnglab.org", #location: "Netherlands"
	"wss://dexnode.net/ws", #location: "Dallas, USA"
	"wss://kc-us-dex.xeldal.com/ws", #location: "Kansas City, USA"
	"wss://la.dexnode.net/ws", #location: "Los Angeles, USA"
]

ws = BitSharesWebsocket(
    full_node_list,
    objects=["2.0.x", "2.1.x", "1.3.x"]
)

def publish_wyrd(block_param):
	# Calculate the current value of Hertz in USD

	reference_timestamp = pendulum.parse("2015-10-13T14:12:24+00:00").timestamp() # Retrieving the Bitshares 2.0 genesis block timestamp
	current_timestamp = pendulum.now().timestamp()

	urthr_value = norn_feed(
		0.14, # amplitude
		reference_timestamp,
		current_timestamp,
		86400 * 28, # period
		0 # phase offset
		)

	verthandi_value = norn_feed(
		0.14, # amplitude
		reference_timestamp,
		current_timestamp,
		86400 * 28, # period
		86400 * 9.33 # phase offset
		)

	skuld_value = norn_feed(
		0.14, # amplitude
		reference_timestamp,
		current_timestamp,
		86400 * 28, # period
		86400 * 18.66 # phase offset
		)

	urthr = Price(urthr_value, "BTS/URTHR")
	verthandi = Price(verthandi_value, "BTS/VERTHANDI")
	skuld = Price(skuld_value, "BTS/SKULD")

	pprint(hertz.bitshares.publish_price_feed(
		"URTHR",
		urthr,
		cer=urthr*0.8, # Setting in line with Wackou's price feed scripts
		mssr=110,
		mcr=200,
		account="REPLACE_WITH_YOUR_USERNAME"
	))

	pprint(hertz.bitshares.publish_price_feed(
		"VERTHANDI",
		verthandi,
		cer=verthandi*0.8, # Setting in line with Wackou's price feed scripts
		mssr=110,
		mcr=200,
		account="REPLACE_WITH_YOUR_USERNAME"
	))

	pprint(hertz.bitshares.publish_price_feed(
		"SKULD",
		skuld,
		cer=skuld*0.8, # Setting in line with Wackou's price feed scripts
		mssr=110,
		mcr=200,
		account="REPLACE_WITH_YOUR_USERNAME"
	))

# Unlock the Bitshares wallet
hertz.bitshares.wallet.unlock("LOCAL_WALLET_PASSWORD")
ws.on_block += publish_wyrd
ws.run_forever()
