 
import sched, time

# run it first time
print "Starting Getting data from webs..."
execfile("Vicino_on_the_lake.py")

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print "Getting data from webs..."
    execfile("Vicino_on_the_lake.py")
    s.enter(3600, 1, do_something, (sc,))

s.enter(3600, 1, do_something, (s,))
s.run()    
                                                                                                                                