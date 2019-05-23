
Runs adding on some very short exposure time observations

I think for this, I'm going to add a detailer that checks if N short exposures have been taken in the last year. If not, it will add them in to be taken. 

Note, this is a rather simple implementation, so I think the short exposures are getting counted towards the total number of observations in a filter. This is probably fine since it's such a small number and is a constant on each filter anyway.

XXX--still debugging. Looks like maybe things are getting flushed and I need to pump up the flushby time?