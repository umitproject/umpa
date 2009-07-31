"""A generally useful event scheduler class.

Each instance of this class manages its own queue.
No multi-threading is implied; you are supposed to hack that
yourself, or use a single instance per application.

Each instance is parametrized with two functions, one that is
supposed to return the current time, one that is supposed to
implement a delay.  You can implement real-time scheduling by
substituting time and sleep from built-in module time, or you can
implement simulated time by writing your own functions.  This can
also be used to integrate scheduling with STDWIN events; the delay
function is allowed to modify the queue.  Time can be expressed as
integers or floating point numbers, as long as it is consistent.

Events are specified by tuples (time, priority, action, argument).
As in UNIX, lower priority numbers mean higher priority; in this
way the queue can be maintained as a priority queue.  Execution of the
event means calling the action function, passing it the argument
sequence in "argument" (remember that in Python, multiple function
arguments are be packed in a sequence).
The action function may be an instance method so it
has another way to reference private data (besides global variables).
"""

# XXX The timefunc and delayfunc should have been defined as methods
# XXX so you can define new kinds of schedulers using subclassing
# XXX instead of having to define a module or class just to hold
# XXX the global state of your particular time and delay functions.

import heapq

__all__ = ["scheduler"]

class Event(object):
    attrs = 'time priority action argument'.split()
    __slots__ = '_values', '_cancelled'
    def __init__(self, time, priority, action, argument):
        self._values = (time, priority, action, argument)
        self._cancelled = False

    def __eq__(self, other):
        return self._values == other._values

    def __lt__(self, other):
        return self._values < other._values

    def __iter__(self):
        for i in self._values:
            yield i

    def __getattr__(self, key):
        if key == '_cancelled':
            return self._cancelled
        return self._values[self.attrs.index(key)]

    def _get_cancelled(self):
        return self._cancelled

    def _set_cancelled(self, value):
        if not value:
            if self._cancelled:
                raise Exception("You can't un-cancel an event.")
            return
        self._cancelled = True

    cancelled = property(_get_cancelled, _set_cancelled)
    del _get_cancelled, _set_cancelled

    def __repr__(self):
        return '%s(%s, %s, %s, %s)'%(self.__class__.__name__, self.time, self.priority, self.action, self.argument)

def LocalSynchronize(method):
    def Call(self, *args, **kwargs):
        # slight performance improvement over using FakeLock all the time for all
        # method calls
        if self.lock is FakeLock:
            return method(self, *args, **kwargs)
        else:
            with self.lock:
                return method(self, *args, **kwargs)
    Call.__name__ = method.__name__
    return Call

class FakeLock(object):
    def __enter__(self):
        return
    def __exit__(self, type, value, traceback):
        return
    def __call__(self):
        return self
FakeLock = FakeLock()

class scheduler(object):
    def __init__(self, timefunc, delayfunc, locked=False):
        """Initialize a new instance, passing the time and delay
        functions.

        If the optional locked argument (defaulting to false) is true, this
        scheduler will use a threading.RLock() instance to guarantee internal
        consistancy.

        """
        self._queue = []
        self.timefunc = timefunc
        self.delayfunc = delayfunc
        self.cancelled = 0
        if not locked:
            self.lock = FakeLock
        else:
            import threading
            self.lock = threading.RLock()

    @LocalSynchronize
    def enterabs(self, time, priority, action, argument):
        """Enter a new event in the queue at an absolute time.

        Returns an ID for the event which can be used to remove it,
        if necessary.

        """
        event = Event(time, priority, action, argument)
        heapq.heappush(self._queue, event)
        return event # The ID

    @LocalSynchronize
    def enter(self, delay, priority, action, argument):
        """A variant that specifies the time as a relative time.

        This is actually the more commonly used interface.

        """
        time = self.timefunc() + delay
        return self.enterabs(time, priority, action, argument)

    @LocalSynchronize
    def peek(self):
        """Will return  the first item in the queue in a properly synchronized
        manner.

        An empty queue will raise an IndexError.

        """
        return self._queue[0]

    @LocalSynchronize
    def cancel(self, event):
        """Remove an event from the queue.

        This must be presented the ID as returned by enter().

        """
        self.cancelled += 1
        event.cancelled = True
        if self._ok_clear():
            self._clear_cancelled()

    @LocalSynchronize
    def empty(self):
        """Check whether the queue is empty."""
        return not self._queue

    def _ok_clear(self):
        """Clear cancelled events when the queue is at least 128 events and more
        than half of the events are cancelled, or clear regardless of the event
        count when cancelled events are at least 7/8 of all events in the queue.

        """
        lq = len(self._queue)
        return (lq > 128 and self.cancelled > (lq>>1)) or (self.cancelled<<3 > lq*7)

    @LocalSynchronize
    def _clear_cancelled(self):
        """Clears all cancelled events and re-heapifies the schedule.

        Note the following:

        >>> a = sched.queue
        >>> sched._clear_cancelled()
        >>> b = sched.queue

        After the above is executed, a and b may not be the same!

        """
        self._queue[:] = [i for i in self._queue if not i.cancelled]
        heapq.heapify(self._queue)
        self.cancelled = 0

    def run(self, now=None):
        """Execute events until the queue is empty.

        When there is a positive delay until the first event, the
        delay function is called and the event is left in the queue;
        otherwise, the event is removed from the queue and executed
        (its action function is called, passing it the argument).  If
        the delay function returns prematurely, it is simply
        restarted.

        It is legal for both the delay function and the action
        function to to modify the queue or to raise an exception;
        exceptions are not caught but the scheduler's state remains
        well-defined so run() may be called again.

        A questionable hack is added to allow other threads to run:
        just after an event is executed, a delay of 0 is executed, to
        avoid monopolizing the CPU when other threads are also
        runnable.

        """
        # localize variable access to minimize overhead
        # and to improve thread safety
        q = self._queue
        delayfunc = self.delayfunc
        timefunc = self.timefunc
        pop = heapq.heappop
        push = heapq.heappush
        peek = self.peek
        lock = self.lock
        if self._ok_clear():
            self._clear_cancelled()
        while q and ((now is None) or (q[0].time <= now)):
            time, priority, action, argument = checked_event = q[0]
            _now = timefunc()
            if _now < time:
                delayfunc(time - _now)
            else:
                with lock:
                    event = pop(q)
                # Verify that the event was not removed or altered
                # by another thread after we last looked at q[0].
                if event is checked_event:
                    if event.cancelled:
                        with lock:
                            self.cancelled -= 1
                    else:
                        action(*argument)
                        delayfunc(0)   # Let other threads run
                else:
                    with lock:
                        push(q, event)

    def __len__(self):
        # Use max in order to fix a potential race condition
        return max(len(self._queue) - self.cancelled, 0)

    @LocalSynchronize
    def getqueue(self, now=None, copy=True, auto_clear=True):
        """An ordered list of upcoming events.

        Events are Event objects with fields for:
            time, priority, action, arguments

        """
        # Use heapq to sort the queue rather than using 'sorted(self._queue)'.
        # With heapq, two events scheduled at the same time will show in
        # the actual order they would be retrieved.
        if copy:
            events = self._queue[:]
        else:
            events = self._queue
            if auto_clear and self._ok_clear():
                self._clear_cancelled()
        out = []
        pop = heapq.heappop
        while events and ((now is None) or (events[0].time <= now)):
            event = pop(events)
            if not event.cancelled:
                out.append(event)
            elif not copy: # the event was cancelled, and this is not a copy
                self.cancelled -= 1
        return out

    @property
    @LocalSynchronize
    def queue(self):
        return self.getqueue()
