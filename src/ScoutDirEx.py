        # -*- coding: UTF-8 -*-
"""Easy to use object-oriented thread pool framework.

A thread pool is an object that maintains a pool of worker threads to perform
time consuming operations in parallel. It assigns jobs to the threads
by putting them in a work request queue, where they are picked up by the
next available thread. This then performs the requested operation in the
background and puts the results in another queue.

The thread pool object can then collect the results from all threads from
this queue as soon as they become available or after all threads have
finished their work. It's also possible, to define callbacks to handle
each result as it comes in.

The basic concept and some code was taken from the book "Python in a Nutshell,
2nd edition" by Alex Martelli, O'Reilly 2006, ISBN 0-596-10046-9, from section
14.5 "Threaded Program Architecture". I wrapped the main program logic in the
ThreadPool class, added the WorkRequest class and the callback system and
tweaked the code here and there. Kudos also to Florent Aide for the exception
handling mechanism.

Basic usage::

    >>> pool = ThreadPool(poolsize)
    >>> requests = makeRequests(some_callable, list_of_args, callback)
    >>> [pool.putRequest(req) for req in requests]
    >>> pool.wait()

See the end of the module code for a brief, annotated usage example.

Website : http://chrisarndt.de/projects/threadpool/

"""
__docformat__ = "restructuredtext en"

__all__ = [
    'makeRequests',
    'NoResultsPending',
    'NoWorkersAvailable',
    'ThreadPool',
    'WorkRequest',
    'WorkerThread'
]

__author__ = "Christopher Arndt"
__version__ = '1.2.7'
__revision__ = "$Revision: 1.1 $"
__date__ = "$Date: 2012/06/19 04:02:49 $"
__license__ = "MIT license"


# standard library modules
import sys,os
import threading
import queue
import traceback
import sqlite3

g_dicInitiaGenFile = {}
g_dicLatestFile = {}
g_strHaveGeneratedSqlte3Path = ""


# exceptions
class NoResultsPending(Exception):
    """All work requests have been processed."""
    pass

class NoWorkersAvailable(Exception):
    """No worker threads available to process remaining requests."""
    pass


# internal module helper functions
def _handle_thread_exception(request, exc_info):
    """Default exception handler callback function.

    This just prints the exception info via ``traceback.print_exception``.

    """
    traceback.print_exception(*exc_info)


# utility functions
def makeRequests(callable_, args_list, callback=None,
        exc_callback=_handle_thread_exception):
    """Create several work requests for same callable with different arguments.

    Convenience function for creating several work requests for the same
    callable where each invocation of the callable receives different values
    for its arguments.

    ``args_list`` contains the parameters for each invocation of callable.
    Each item in ``args_list`` should be either a 2-item tuple of the list of
    positional arguments and a dictionary of keyword arguments or a single,
    non-tuple argument.

    See docstring for ``WorkRequest`` for info on ``callback`` and
    ``exc_callback``.

    """
    requests = []
    for item in args_list:
        if isinstance(item, tuple):
            requests.append(
                WorkRequest(callable_, item[0], item[1], callback=callback,
                    exc_callback=exc_callback)
            )
        else:
            requests.append(
                WorkRequest(callable_, [item], None, callback=callback,
                    exc_callback=exc_callback)
            )
    return requests

# utility functions
def makeRequestsEx(callable_, args_list, callback=None,
        exc_callback=_handle_thread_exception):
    """Create several work requests for same callable with different arguments.

    Convenience function for creating several work requests for the same
    callable where each invocation of the callable receives different values
    for its arguments.

    ``args_list`` contains the parameters for each invocation of callable.
    Each item in ``args_list`` should be either a 2-item tuple of the list of
    positional arguments and a dictionary of keyword arguments or a single,
    non-tuple argument.

    See docstring for ``WorkRequest`` for info on ``callback`` and
    ``exc_callback``.
    """

    requests = []
    
    for key,value in args_list.items():
        #print(key,"",value)
        requests.append(WorkRequest(callable_, key, None, callback=callback,exc_callback=exc_callback))
                        
                        
    '''
    for item in args_list:
        if isinstance(item, tuple):
            requests.append(
                WorkRequest(callable_, item[0], item[1], callback=callback,
                    exc_callback=exc_callback)
            )
        else:
            requests.append(
                WorkRequest(callable_, [item], None, callback=callback,
                    exc_callback=exc_callback)
            )
    '''
        
    return requests



# classes
class WorkerThread(threading.Thread):
    """Background thread connected to the requests/results queues.

    A worker thread sits in the background and picks up work requests from
    one queue and puts the results in another until it is dismissed.

    """

    def __init__(self, requests_queue, results_queue, poll_timeout=5, **kwds):
        """Set up thread in daemonic mode and start it immediatedly.

        ``requests_queue`` and ``results_queue`` are instances of
        ``queue.queue`` passed by the ``ThreadPool`` class when it creates a new
        worker thread.

        """
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(1)
        self._requests_queue = requests_queue
        self._results_queue = results_queue
        self._poll_timeout = poll_timeout
        self._dismissed = threading.Event()
        self.start()

    def run(self):
        """Repeatedly process the job queue until told to exit."""
        while True:
            if self._dismissed.isSet():
                # we are dismissed, break out of loop
                break
            # get next work request. If we don't get a new request from the
            # queue after self._poll_timout seconds, we jump to the start of
            # the while loop again, to give the thread a chance to exit.
            try:
                request = self._requests_queue.get(True, self._poll_timeout)
            except queue.Empty:
                continue
            else:
                if self._dismissed.isSet():
                    # we are dismissed, put back request in queue and exit loop
                    self._requests_queue.put(request)
                    break
                try:
#                    print((request.args,request.kwds))
                    param = (request.args,request.kwds)
                    result = request.callable(param)
                    self._results_queue.put((request, result))
                except:
                    print("except in callable class")
                    request.exception = True
                    self._results_queue.put((request, sys.exc_info()))

    def dismiss(self):
        """Sets a flag to tell the thread to exit when done with current job."""
        self._dismissed.set()


class WorkRequest:
    """A request to execute a callable for putting in the request queue later.

    See the module function ``makeRequests`` for the common case
    where you want to build several ``WorkRequest`` objects for the same
    callable but with different arguments for each call.

    """

    def __init__(self, callable_, args=None, kwds=None, requestID=None,
            callback=None, exc_callback=_handle_thread_exception):
        """Create a work request for a callable and attach callbacks.

        A work request consists of the a callable to be executed by a
        worker thread, a list of positional arguments, a dictionary
        of keyword arguments.

        A ``callback`` function can be specified, that is called when the
        results of the request are picked up from the result queue. It must
        accept two anonymous arguments, the ``WorkRequest`` object and the
        results of the callable, in that order. If you want to pass additional
        information to the callback, just stick it on the request object.

        You can also give custom callback for when an exception occurs with
        the ``exc_callback`` keyword parameter. It should also accept two
        anonymous arguments, the ``WorkRequest`` and a tuple with the exception
        details as returned by ``sys.exc_info()``. The default implementation
        of this callback just prints the exception info via
        ``traceback.print_exception``. If you want no exception handler
        callback, just pass in ``None``.

        ``requestID``, if given, must be hashable since it is used by
        ``ThreadPool`` object to store the results of that work request in a
        dictionary. It defaults to the return value of ``id(self)``.

        """
        if requestID is None:
            self.requestID = id(self)
        else:
            try:
                self.requestID = hash(requestID)
            except TypeError:
                raise TypeError("requestID must be hashable.")
        self.exception = False
        self.callback = callback
        self.exc_callback = exc_callback
        self.callable = callable_
        self.args = args or []
        self.kwds = kwds or {}
#        print(self.args,self.kwds)
    def __str__(self):
        return "<WorkRequest id=%s args=%r kwargs=%r exception=%s>" % \
            (self.requestID, self.args, self.kwds, self.exception)

class ThreadPool:
    """A thread pool, distributing work requests and collecting results.

    See the module docstring for more information.

    """

    def __init__(self, num_workers, q_size=0, resq_size=0, poll_timeout=5):
        """Set up the thread pool and start num_workers worker threads.

        ``num_workers`` is the number of worker threads to start initially.

        If ``q_size > 0`` the size of the work *request queue* is limited and
        the thread pool blocks when the queue is full and it tries to put
        more work requests in it (see ``putRequest`` method), unless you also
        use a positive ``timeout`` value for ``putRequest``.

        If ``resq_size > 0`` the size of the *results queue* is limited and the
        worker threads will block when the queue is full and they try to put
        new results in it.

        .. warning:
            If you set both ``q_size`` and ``resq_size`` to ``!= 0`` there is
            the possibilty of a deadlock, when the results queue is not pulled
            regularly and too many jobs are put in the work requests queue.
            To prevent this, always set ``timeout > 0`` when calling
            ``ThreadPool.putRequest()`` and catch ``queue.Full`` exceptions.

        """
        self._requests_queue = queue.Queue(q_size)
        self._results_queue = queue.Queue(resq_size)
        self.workers = []
        self.dismissedWorkers = []
        self.workRequests = {}
        self.createWorkers(num_workers, poll_timeout)

    def createWorkers(self, num_workers, poll_timeout=5):
        """Add num_workers worker threads to the pool.

        ``poll_timout`` sets the interval in seconds (int or float) for how
        ofte threads should check whether they are dismissed, while waiting for
        requests.

        """
        for i in range(num_workers):
            self.workers.append(WorkerThread(self._requests_queue,
                self._results_queue, poll_timeout=poll_timeout))

    def dismissWorkers(self, num_workers, do_join=False):
        """Tell num_workers worker threads to quit after their current task."""
        dismiss_list = []
        for i in range(min(num_workers, len(self.workers))):
            worker = self.workers.pop()
            worker.dismiss()
            dismiss_list.append(worker)

        if do_join:
            for worker in dismiss_list:
                worker.join()
        else:
            self.dismissedWorkers.extend(dismiss_list)

    def joinAllDismissedWorkers(self):
        """Perform Thread.join() on all worker threads that have been dismissed.
        """
        for worker in self.dismissedWorkers:
            worker.join()
        self.dismissedWorkers = []

    def putRequest(self, request, block=True, timeout=None):
        """Put work request into work queue and save its id for later."""
        assert isinstance(request, WorkRequest)
        # don't reuse old work requests
        assert not getattr(request, 'exception', None)
        self._requests_queue.put(request, block, timeout)
        self.workRequests[request.requestID] = request

    def poll(self, block=False):
        """Process any new results in the queue."""
        while True:
            # still results pending?
            if not self.workRequests:
                raise NoResultsPending
            # are there still workers to process remaining requests?
            elif block and not self.workers:
                raise NoWorkersAvailable
            try:
                # get back next results
                request, result = self._results_queue.get(block=block)
                # has an exception occured?
                if request.exception and request.exc_callback:
                    request.exc_callback(request, result)
                # hand results to callback, if any
                if request.callback and not \
                       (request.exception and request.exc_callback):
                    request.callback(request, result)
                del self.workRequests[request.requestID]
            except queue.Empty:
                break

    def wait(self):
        """Wait for results, blocking until all have arrived."""
        while 1:
            try:
                self.poll(True)
            except NoResultsPending:
                break


def InitiaMicaps(totalDir):
    
    global g_dicInitiaGenFile
    global g_dicLatestFile
    
    if not os.path.exists(totalDir):
        return
    
    elements = os.listdir(totalDir)
    for element in elements:
        elementDir = totalDir + "/" + element
        if not os.path.isdir(elementDir):
            continue
        
        timeLatest =  datetime(2003, 11, 25)
        fileLatest = ""
        levels = os.listdir(elementDir)
        for level in levels:
            levelPath = elementDir + "/" + level
            if os.path.isfile(levelPath) :
               time.sleep(10)
               fileLatest = GetLatestFileRegular(elementDir)
               break
                #print(levelPath)
            else:
               g_dicInitiaGenFile[levelPath] = ""
               #break
        if fileLatest != "":
            g_dicLatestFile[elementDir] = fileLatest
            
def GetLatestFile(dir):
    
        if not os.path.isdir(dir):
            return
        
        
        timeLatest =  datetime(2003, 11, 25)
        fileLatest = ""
        levels = os.listdir(dir)
        for level in levels:
            curFile = dir + "/" + level
            if os.path.isfile(curFile) :
                timecurr = time.localtime(os.stat(curFile).st_ctime)
                datetimeCurFile =  datetime(timecurr.tm_year,timecurr.tm_mon,timecurr.tm_mday,timecurr.tm_hour,timecurr.tm_min,timecurr.tm_sec)
                if datetimeCurFile > timeLatest:
                    timeLatest = datetimeCurFile;
                    fileLatest = curFile
                elif datetimeCurFile == timeLatest:
                    if(fileLatest < curFile):
                        fileLatest = curFile
        return fileLatest

def GetLatestFileRegular(dir):
    
        if not os.path.isdir(dir):
            return
        

        timeLatest =  datetime(2003, 11, 25)
        fileLatest = ""
        levels = os.listdir(dir)
        levels.sort()
        if len(levels) > 0:
            return [levels[len(levels)-1]]
        else:
            return "" 
        
        for level in levels:
            curFile = dir + "/" + level
            if os.path.isfile(curFile) :
                timecurr = time.localtime(os.stat(curFile).st_ctime)
                datetimeCurFile =  datetime(timecurr.tm_year,timecurr.tm_mon,timecurr.tm_mday,timecurr.tm_hour,timecurr.tm_min,timecurr.tm_sec)
                if datetimeCurFile > timeLatest:
                    timeLatest = datetimeCurFile;
                    fileLatest = curFile
                elif datetimeCurFile == timeLatest:
                    if(fileLatest < curFile):
                        fileLatest = curFile
        return fileLatest

################
# USAGE EXAMPLE
################

if __name__ == '__main__':
    
    import random
    import time
    from datetime import datetime
    
    beginTm = datetime.now()
    totalDir = "X:\\data\\newecmwf_grib"
    InitiaMicaps(totalDir)
    list = [("X:\\data\\newecmwf_grib\\height\\850",1),("X:\data\newecmwf_grib\height\8925",2),("file3",3),("file4",4)]
    print(g_dicLatestFile)

    dictTest = {"X:\\data\\newecmwf_grib\\height\\850":"","X:\\data\\newecmwf_grib\\height\\925":"" ,"X:\\data\\newecmwf_grib\\height\\500":"" }
    #g_dicInitiaGenFile = dictTest
    
    # the work the threads will have to do (rather trivial in our example)
    def do_something(data):
        assert isinstance(data, tuple)
        print("in function do_something: ",data)
        time.sleep(random.randint(1,5))
        result = round(random.random() * data, 5)
        # just to show off, we throw an exception once in a while
        if result > 5:
            raise RuntimeError("Something extraordinary happened!")
        return result
    
    def do_somethingEx(data):
        global g_dicInitiaGenFile
        print("in function do_somethingEx: ",data[0])
        #print(len(os.listdir(data[0])))
        time.sleep(10)
        g_dicInitiaGenFile[data[0]] = GetLatestFileRegular(data[0]) 
        
    # this will be called each time a result is available
    def print_result(request, result):
        print("**** Result from request #%s: %r" % (request.requestID, result))

    # this will be called when an exception occurs within a thread
    # this example exception handler does little more than the default handler
    def handle_exception(request, exc_info):
        if not isinstance(exc_info, tuple):
            # Something is seriously wrong...
            print(request)
            print(exc_info)
            raise SystemExit
        print("**** Exception occured in request #%s: %s" % \
          (request.requestID, exc_info))    

    # assemble the arguments for each job to a list...
    data = [random.randint(1,10) for i in range(20)]
    # ... and build a WorkRequest object for each item in data
#    print(data)
    #requests = makeRequests(do_something, list, print_result, handle_exception)
    requests = makeRequestsEx(do_somethingEx, g_dicInitiaGenFile, print_result, handle_exception)
    # to use the default exception handler, uncomment next line and comment out
    # the preceding one.
    #requests = makeRequests(do_something, data, print_result)

    # we create a pool of 3 worker threads
    print("Creating thread pool with 3 worker threads.")
    main = ThreadPool(3)

    # then we put the work requests in the queue...
    for req in requests:
        main.putRequest(req)
        print("Work request #%s added." % req.requestID)
    # or shorter:
    # [main.putRequest(req) for req in requests]

    # ...and wait for the results to arrive in the result queue
    # by using ThreadPool.wait(). This would block until results for
    # all work requests have arrived:
    # main.wait()

    # instead we can poll for results while doing something else:
    i = 0
    while True:
        try:
            time.sleep(0.5)
            main.poll()
            print("Main thread working...")
            print("(active worker threads: %i)" % (threading.activeCount()-1, ))
            if i == 10:
                print("**** Adding 3 more worker threads...")
                main.createWorkers(3)
            if i == 20:
                print("**** Dismissing 2 worker threads...")
                main.dismissWorkers(2)
            i += 1
        except KeyboardInterrupt:
            print("**** Interrupted!")
            break
        except NoResultsPending:
            print("**** No pending results.")
            break
    if main.dismissedWorkers:
        print("Joining all dismissed worker threads...")
        main.joinAllDismissedWorkers()
    endTm = datetime.now()
    print(beginTm,"   ",endTm)
    print(g_dicInitiaGenFile)