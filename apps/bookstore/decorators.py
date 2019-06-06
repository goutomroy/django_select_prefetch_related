from django.db import connection, reset_queries
import time
import functools


def query_debugger(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print("Function : ", func.__name__)
        print("Number of Queries :", end_queries - start_queries)
        print("Finished in : %.2fs" % (end - start))
        return result

    return wrapper
