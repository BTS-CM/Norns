from bitshares.asset import Asset
from bitshares import BitShares
from bitsharesapi.websocket import BitSharesWebsocket # For on_block
from bitshares.price import Price
import math # For sine wave calculations
from multiprocessing import Pool, Manager # For parallel computation
import pendulum # For timestamps

manager = Manager() # Inter pool process data manager
past_values = manager.dict() # Init the dict object which is passed to each pool process
past_values['URTHR'] = 0.0 # Initial value, overwritten after first publish
past_values['VERTHANDI'] = 0.0 # Initial value, overwritten after first publish
past_values['SKULD'] = 0.0 # Initial value, overwritten after first publish

def norn_feed(amplitude, reference_timestamp, current_timestamp, period, phase_offset):
	"""
	Given the reference timestamp, the current timestamp, the period (in days), the phase, and the amplitude (> 0 && < 1), output the current sine wave value.
	"""
	waveform = math.sin(((((current_timestamp - (reference_timestamp + phase_offset))/period) % 1) * period) * ((2*math.pi)/period)) # Only change for an alternative HERTZ ABA.
	return 1 + (amplitude * waveform)

def multi_feed(target_name, phase_offset, past_value):
	"""
	Publish multiple feeds in parallel
	"""
	reference_timestamp = pendulum.parse("2015-10-13T14:12:24+00:00").timestamp() # Retrieving the Bitshares 2.0 genesis block timestamp
	current_timestamp = pendulum.now().timestamp()

	asset_value = norn_feed(
		0.12612612612, # amplitude
		reference_timestamp,
		current_timestamp,
		86400 * 28, # period
		phase_offset # phase offset
		)

	previously_published_value = past_value[target_name]

	min_price_feed_difference = 0.00001 # Default set to the lowest decimal place, increase to reduce frequency of publishing feeds

	if (math.fabs(asset_value - previously_published_value) > min_price_feed_difference):
		past_value[target_name] = asset_value # Overwrite the target_name asset's 'past value' for comparison next block
		wallet_password = "LOCAL_WALLET_PASSWORD" # Replace with your price feed wallet's password
		target_pair = "BTS/"+str(target_name)
		target = Price(asset_value, target_pair)
		target.bitshares.wallet.unlock(wallet_password) # Unlock the wallet immediately prior to publishing feed

		target.bitshares.publish_price_feed(
		  target_name,
		  target,
		  cer=target*0.8, # Setting in line with Wackou's price feed scripts
		  mssr=110, # Min short squeeze ratio of 110%
		  mcr=200, # Min 200% backing collateral
		  account="account_name" # Replace with your BTS price feed account name
		)
		print("Published " + target_name)
	else:
		# The price hasn't changed enough to warrant publishing a feed
		print("Skipped block " + target_name)

def publish_wyrd(block_param):
	"""
	Triggers every 3 seconds.
	Calculates then attempts to publish the feeds for Urthr, Verthandi and Skuld in parallel.
	Avoids publishing feeds unneccessarily.
	"""
	print("Attempting to publish")

	with Pool(3) as p:
		# Parallelizes the feed production
		p.starmap(multi_feed, [("URTHR",0,past_values), ("VERTHANDI",806112,past_values), ("SKULD",1612224,past_values)])

	print("---------")

if __name__ == "__main__":
	"""
	Script starts here. Change the node list to
	"""
	print("Started")
	full_node_list = [
		"wss://eu.nodes.bitshares.works", #location: "Central Europe - BitShares Infrastructure Program"
		"wss://bitshares.crypto.fans/ws", #location: "Munich, Germany"
		"wss://api.bts.blckchnd.com" #location: "Falkenstein, Germany"
		"wss://dex.rnglab.org", #location: "Netherlands"
	]

	ws = BitSharesWebsocket(
		full_node_list,
		objects=["2.0.x", "2.1.x", "1.3.x"]
	)

	print("ws connection established")

	ws.on_block += publish_wyrd
	ws.run_forever()
