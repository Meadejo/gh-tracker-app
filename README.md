# gh-tracker-app
(Eventually) a full-service campaign management application for the board game Gloomhaven.

This is my current state code. I'm at least mostly confident that this is everything you need to run it in its current state, outside of items called out below.
* Python3
* PyQt5

Issues I know exist:
* Comment lines are sparse. (I started with a lot more, but found myself deleting the majority of it as I constantly refactored. I had intended on adding comments after I reached something resembling a final state, but I'm still working on reaching that state.)
* Inconsistencies exist. Sometimes I started doing things one way, found it was better to do them another, moved forward with the 'better' method, but did not retroactively correct the previous instances.
* Many broken/static/incomplete functions. A lot of the functions had to exist so that I could connect them/reference them/etc, but I wasn't sure exactly how the function was going to work yet, so it's mostly blank.

Random Notes:
* Everything in here I learned by spending a lot of time on stackoverflow and then bashing at it via trial and error. I'm sure a lot of things are probably a little... "Backwards."
* This is my third "ground up" rewrite of the code. In this instance, I started out trying to lean more heavily on object classes. I *may* have gone overboard with it and/or gone in the wrong direction with it.
* I'm always happy to hear any feedback from anybody at any level of expertise. I want to learn, I love what I've been able to do so far, and there's only so much I can learn by just reading about what others have done.
