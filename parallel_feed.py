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

past_timestamps = manager.dict() # Init the dict object which is passed to each pool process
past_timestamps['URTHR'] = pendulum.parse("2015-10-13T14:12:24+00:00").timestamp() # Initial value, overwritten after first publish
past_timestamps['VERTHANDI'] = pendulum.parse("2015-10-13T14:12:24+00:00").timestamp() # Initial value, overwritten after first publish
past_timestamps['SKULD'] = pendulum.parse("2015-10-13T14:12:24+00:00").timestamp() # Initial value, overwritten after first publish

min_price_feed_difference = 0.00001 # Default set to the lowest decimal place, increase to reduce frequency of publishing feeds
static_avg_diff_per_second = 0.00000008764076117682 # Static value - check simulator spreadsheet for rough calculations
time_between_feeds = min_price_feed_difference/static_avg_diff_per_second # Seconds until the price changes the configured min difference

def norn_feed(amplitude, reference_timestamp, current_timestamp, period, phase_offset):
	"""
	Given the reference timestamp, the current timestamp, the period (in days), the phase, and the amplitude (> 0 && < 1), output the current sine wave value.
	"""
	waveform = math.sin(((((current_timestamp - (reference_timestamp + phase_offset))/period) % 1) * period) * ((2*math.pi)/period)) # Only change for an alternative HERTZ ABA.
	return 1 + (amplitude * waveform)

def multi_feed(target_name, phase_offset, past_value, past_timestamp):
	"""
	Publish multiple feeds in parallel
	"""
	reference_timestamp = pendulum.parse("2015-10-13T14:12:24+00:00").timestamp() # Retrieving the Bitshares 2.0 genesis block timestamp
	current_timestamp = pendulum.now().timestamp()
	last_published_timestamp = past_timestamps[target_name]
	publish_time_diff = (pendulum.from_timestamp(last_published_timestamp)).diff(pendulum.now()).in_seconds()

	if (publish_time_diff >= time_between_feeds):
		# Enough time has passed to begin feeding again
		asset_value = norn_feed(
			0.05303030303, # amplitude
			reference_timestamp,
			current_timestamp,
			86400 * 28, # period
			phase_offset # phase offset
			)

		previously_published_value = past_value[target_name]

		if (math.fabs(asset_value - previously_published_value) > min_price_feed_difference):
			past_value[target_name] = asset_value # Overwrite the target_name asset's 'past value' for comparison next block
			past_timestamps[target_name] = current_timestamp # Overwriting the target_name asset's 'past timestamp' for comparison next block

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
	else:
		# Not enough time has passed to justify publishing a price feed change!
		# So let's skip & save compute resources!
		print("Skipped publishing {}. Next attempt in approximately {} seconds".format(target_name, int(time_between_feeds - publish_time_diff)))

def publish_wyrd(block_param):
	"""
	Triggers every 3 seconds.
	Calculates then attempts to publish the feeds for Urthr, Verthandi and Skuld in parallel.
	Avoids publishing feeds unneccessarily.
	"""
	print("Attempting to publish")

	with Pool(3) as p:
		# Parallelizes the feed production
		p.starmap(multi_feed, [("URTHR",0,past_values,past_timestamps), ("VERTHANDI",806112,past_values,past_timestamps), ("SKULD",1612224,past_values,past_timestamps)])

	print("---------") # Divider

if __name__ == "__main__":
	"""
	Script starts here.
	Change the node list at your own discretion
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
