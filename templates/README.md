Make a tier of surveys dedicated to gathering templates early.

some things to set:
* don't observe the same area in the same night
* u and g only when moon is down
* need an area threshold so we get a big blob
* maybe an hour angle limit as well
* limit to 1st year
* exclude area that has been observed 3+ times
    * This might let in some random twilight observations, so possible further refinement



Parameters that could be varied:
* how large an hour angle range to allow (3.5, 2.5, 1.5)
* how long should we try to do a template gather blob? (default 33 min, but that's pretty random) (15, 33, 60, 90)
* how much area to demand before actually doing a template gather? (50, 100, 200, 400)



Initial results seem be be very modest. We can get the nights without templates down by around 25 days in some, but not all, filters. 

Looks like in the baseline, we get u and g a bit faster. Probably a case where dark time can get used to get templates for other filters, but that ends up impacting u and g a bit, so the overall effect is sort of a wash.

----

Bumped up to v 4.2.1, I think there was a small change from refactoring DDFs that make things not identical to v4.2

Final message, if one wants templates in a certain area, or in a certain filter, that could be prioritized. But just "get full sky templates earlier" isn't really feasible because there is nothing one can make a trade off with to do it much faster than the baseline strategy.

