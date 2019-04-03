
A directory for working on various cadence forcing strategies

## cadence1

Try not being so strict about the sky brightness around full moon. Rather than filter-specific 5-sigma depth, use the r-band 5-sigma depth for all filters except u. This should let g-band execute in brighter time. But may also have y-band in dark time. 

This seems to have accomplished it's main goal of spreading the g-band observations more. Could potentially expermient with lowering the weight on the basis function maintaining the same filter (there seem to be days of all y-band or all z-band, might be good to break them up).  

This system could also be combined with rolling cadence or rolling-day emphasis. Might also be interesting to do only z and y in twilight.

