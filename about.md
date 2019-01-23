# Abstract

The Norns are a set of three Algorithm Based Assets issued on the Bitshares Decentralized Exchange. They use Bitshares as collateral, reference an oscillating quantity of Bitshares, are 120 degrees offset from one another and have an approximate amplitude of 12.612% over a 28 day period.

# Background

Bitshares (BTS) is a decentralized exchange (DEX) which operates on a Graphene toolkit based blockchain, we're interested in the smartcoin functionality available on the BTS DEX.

Smartcoins on the BTS DEX are decentralized [Market Pegged Assets](https://how.bitshares.works/en/master/bts_holders/tokens/mpa.html), they're typically pegged to an external asset's value (such as USD, CNY, EUR) and have provable backing collateral on the blockchain (typically 170%+ BTS collateral). Multiple feed producers (witnesses, committee or private feed publishers) provide a set of price feeds, from which the BTS DEX establishes the MPA's settlement value as the median of this set of feeds.

[Hertz](https://bitsharescan.com/asset/HERTZ) was the first oscillating Algorithm Based Asset (ABA) created on the BTS DEX. It has an amplitude of 14%, a period of 28 days and has a base reference asset value of $1.00, resulting in a price feed range of $0.86 to $1.14. Despite multiple successful oscillations, its' supply has failed to grow past 4 figures potentially due to users lack of confidence in the external USD asset peg or due to the recent global settlement of bitUSD on the BTS DEX.

With lessons learned from Hertz, the external USD asset peg was abandoned so as to appeal to a global audience and to reduce the risk of global settlement occuring. Rather than simply mimicking Hertz without the external asset peg, a three phase offset set of ABAs was proposed to investigate the resulting market behaviour associated with

# About the Norns

Urthr, Verthandi and Skuld are named after the Norns from Norse mythology. They were chosen over other [triple dieties](https://en.wikipedia.org/wiki/Triple_deity) because their meaning lines up closely with the planned three phase oscillating price feed pattern.

Urthr, named after [Urðr](https://en.wikipedia.org/wiki/Ur%C3%B0r) (fate/past) is the first phase offset ABA.

Verthandi, named after [Verðandi](https://en.wikipedia.org/wiki/Ver%C3%B0andi) (present) is the second phase offset ABA.

Skuld, named after [Skuld](https://en.wikipedia.org/wiki/Skuld) (future/debt) is the third phase offset ABA.

All three mythological entities use the character "[ð](https://en.wikipedia.org/wiki/Eth)" however this character isn't supported by the BTS DEX so the modern English language equivalent of "th" was chosen over "d" to substitute "ð".

## Why an amplitude of 12.612612612% ?

In the UK, a maximum of 0.8% per day 'interest' is enforced on loans; whilst the Norns potentially do not fall under jurisdiction of such regulations, the decision was made to pre-emptively adhere to these UK regulations so that no amplitude migration would be potentially required in the future. An amplitude of 12.612612612% results in just under 0.8% per day increase from trough to peak.

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

The following flags remain:

* "Charge market fee" - There are no market fees imposed, this may be surrendered in the future however it could be a source of market making revenue in the future and will remain available until a future date.
* "Allow issuer to force a global settlement" - This is [currently impossible to disable](https://github.com/bitshares/bitshares-ui/issues/2043). Once it's possible, it'll be disabled.
* "Witness fed asset" - Currently a private price feed publisher list is configured so that the 'hertz-feed; account is able to publish feeds without being a witness. In the future if I have to step aside this will be enabled.

## Visualization

The following Norn price feed visualization was produced in the '[Simulator.xlsx](https://github.com/BTS-CM/Norns/blob/master/Simulator.xlsx)' spreadsheet, it can be used to experiment with different variables and for producing future

<img src="https://i.imgur.com/Ut4mJMf.png" alt="Norn chart" />

# Conclusion

The Norns are an unique asset which will ideally operate forever on the BTS DEX without any centralized influence. Once 7 price feed publishers begin providing feeds it will become active for trading on the BTS DEX. Hopefully this will be more successful than Hertz and will attract new users to Bitshares and possibly inspire similar ABAs to be created in the future.