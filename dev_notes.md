# similar apps
- ATracker by wonderapps AB (on playstore/web)
- Timelog by CodeGamma Technologies (on playstore/web)

# todo list
- minutes and hours conversion should not be handled inside of goal_manager's core functions, change that.
- do the cleanup below.

# cleanup: what actions to take
- adding annotations, error raises, type handling, etc.
- IMPORTANT: in every single instance of calling a core engine function, put the call under a try except statement
==since we're catching exceptions now!!!
- fix indentation for hard to read annotated parameters
==figured out from the nighttime readings,
pythonic readability > arbitrary line length guilt,
readiblity trumps minimalism.

# cleanup progress
- central_registry done
- goal_manager done
- user_interface in progress