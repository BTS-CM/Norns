# Abstract

The Norns are a set of three Algorithm Based Assets issued on the Bitshares Decentralized Exchange. They use Bitshares as collateral, reference an oscillating quantity of Bitshares, are 120 degrees offset from one another and have an approximate amplitude of 5.303% over a 28 day period.

# Background

The BitShares Blockchain is an industrial-grade decentralized platform built for high-performance financial smart contracts. It represents the first decentralized autonomous community that lets its core token holder decide on its future direction and products by means of on-chain voting. The core token is BTS and it is used to realize the built-in SmartCoins, which are of interested to us in this article.

Smartcoins on the Bitshares platform are decentralized [Market Pegged Assets](https://how.bitshares.works/en/master/bts_holders/tokens/mpa.html), they're typically pegged to an external asset's value (such as USD, CNY, EUR) and have provable backing collateral on the blockchain (typically 170%+ BTS collateral). Multiple feed producers (witnesses, committee or private feed publishers) provide a set of price feeds, from which the Bitshares platform establishes the MPA's settlement value as the median of this set of feeds.

[Hertz](https://bitsharescan.com/asset/HERTZ) was the first oscillating Algorithm Based Asset (ABA) created on the Bitshares platform. It has an amplitude of 14%, a period of 28 days and has a base reference asset value of $1.00, resulting in a price feed range of $0.86 to $1.14. Despite multiple successful oscillations, its' supply has failed to grow past 4 figures potentially due to users lack of confidence in the external USD asset peg or due to the recent global settlement of bitUSD on the Bitshares platform.

With lessons learned from Hertz, the external USD asset peg was abandoned so as to appeal to a global audience and to reduce the risk of global settlement occurring. Rather than simply mimicking Hertz without the external asset peg, a three phase offset set of ABAs was proposed to investigate the resulting market behaviors between the three assets throughout their oscillations.

# About the Norns

Urthr, Verthandi and Skuld are named after the Norns from Norse mythology. They were chosen over other [triple dieties](https://en.wikipedia.org/wiki/Triple_deity) because their meaning lines up closely with the planned three phase oscillating price feed pattern.

Urthr, named after [Urðr](https://en.wikipedia.org/wiki/Ur%C3%B0r) (fate/past) is the first phase offset ABA.

Verthandi, named after [Verðandi](https://en.wikipedia.org/wiki/Ver%C3%B0andi) (present) is the second phase offset ABA.

Skuld, named after [Skuld](https://en.wikipedia.org/wiki/Skuld) (future/debt) is the third phase offset ABA.

All three mythological entities use the character "[ð](https://en.wikipedia.org/wiki/Eth)" however this character isn't supported by the Bitshares platform so the modern English language equivalent of "th" was chosen over "d" to substitute "ð".

## Why an amplitude of 5.303030303% ?

In the UK, a maximum of 0.8% per day 'interest' is enforced on loans; whilst the Norns potentially do not fall under jurisdiction of such regulations, the decision was made to pre-emptively adhere to these UK regulations so that no amplitude migration would be potentially required in the future. An amplitude of 5.303030303% results in just under 0.8% per day increase from trough to peak.

Peak value: `1 + (5.303030303/100)` = 1.05303030303
Trough value: `1 - (5.303030303/100)` = 0.94696969697
Daily rate: `(((Peak/Trough)-1)/14)*100` = 0.8

## 13 months in a year?

To ensure that the sine waves were forever uniform and more predictable, a 28 day period was chosen for both Hertz and the Norns. This calendar system is similar to the [International Fixed Calendar](https://en.wikipedia.org/wiki/International_Fixed_Calendar) system, however the initial time reference for the sine waves is the Bitshares genesis timestamp as opposed to the beginning of the year. Given that the Norns are three-phase offset from one another, only one would have been able to start on the 1st.

This calendar system has advantages over the western [Gregorian calendar](https://en.wikipedia.org/wiki/Gregorian_calendar) system as the sine waves are identical every 28 days as opposed to having different periods each month with the Gregorian calendar system.

The 13th 'month' is called "Sol", it resides between June and July.

## Permissions, Flags & Trustworthiness

To improve trustworthiness, the following unnecessary centralized asset-owner permissions have been permanently surrendered:

* “Require holders to be white-listed”: There will never be a white-list for holders.
* “Issuer may transfer asset back to himself”: The issuer can never transfer the asset back to themselves.
* “Issuer must approve all transfers”: Transfers will never require approval.
* “Disable confidential transactions”: Confidential transactions (whenever implemented) will always be allowed.
* "Disable force settlement": I'm unable to disable force settlement, if you don't want force settlement you should use an UIA.
* "Charge market fee" - There are no market fees.
* "Allow issuer to force a global settlement" - It's impossible for the 'issuer' (account with asset owner permissions) to force a global settlement.

The following flags remain:

* "Witness fed asset" - Currently set to disabled & using a private price feed publisher list so that the 'hertz-feed' account is able to publish feeds without being a witness.

## Visualization

The following Norn price feed visualization was produced in the '[Simulator.xlsx](https://github.com/BTS-CM/Norns/blob/master/Simulator.xlsx)' spreadsheet, it can be used to experiment with different variables and for producing future values.

<img src="https://i.imgur.com/XUiMWtl.png" alt="Norn chart" />

## Price feeds

* [Parallel feed](https://github.com/BTS-CM/Norns/blob/master/parallel_feed.py)
* [Zapata's bitshares-pricefeed fork](https://github.com/Zapata/bitshares-pricefeed/blob/develop/bitshares_pricefeed/sources/norm.py)

# Conclusion

The Norns are unique assets which will ideally operate forever on the Bitshares platform without any centralized influence. Once 7 price feed publishers begin providing feeds it will become active for trading on the Bitshares platform. Hopefully this will be more successful than Hertz and will attract new users to Bitshares and possibly inspire similar ABAs to be created in the future.
