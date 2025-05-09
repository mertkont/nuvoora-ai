# Data provisioning, loading, and preprocessing
import asyncio
import threading
from functools import wraps
from app.data.data_creator import initialize_data
from app.core.config import USER_TOKEN

# Global variables - accessible from all the other modules
global_data = None
_initialized = False
_lock = threading.Lock()

def run_async(func):
    """
    Function that transforms an asynchronous function into a synchronous function.

    It can also work with uvicorn statreload.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Control if the thread is the main thread
        if threading.current_thread() is threading.main_thread():
            # Ana thread'de çalışıyoruz, güvenli bir şekilde event loop oluşturabiliriz
            # We are working with the main thread, continue
            try:
                loop = asyncio.get_event_loop()

            except RuntimeError:
                # No event loop, create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_running():
                # If loop is working, create a new thread
                result = []
                error = []
                done = threading.Event()

                def run_in_thread():
                    nonlocal result, error
                    try:
                        temp_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(temp_loop)
                        result.append(temp_loop.run_until_complete(func(*args, **kwargs)))

                    except Exception as e:
                        error.append(e)

                    finally:
                        done.set()

                thread = threading.Thread(target=run_in_thread)
                thread.start()
                done.wait()  # Wait for the results

                if error:
                    raise error[0]

                return result[0]

            else:
                # Loop exists, but not working
                return loop.run_until_complete(func(*args, **kwargs))

        else:
            # We are working with subthread, we can create a new loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(func(*args, **kwargs))

    return wrapper

class DataFetcher:
    def __init__(self, user_token=None):
        self.user_token = user_token

    async def get_user_data(self):
        """
        Asynchronized function that returns the data sets based on the user token.
        """
        global global_data, _initialized

        # Thread-safe initialization
        with _lock:
            if not _initialized:
                if not self.user_token:
                    raise ValueError("Access token is required to fetch data.")

                # Data load process with token
                global_data = await initialize_data(self.user_token)
                _initialized = True

        return global_data

    @run_async
    async def get_user_data_sync(self, token):
        """
        Decorator function that gets the data based on the user token.

        It gets the token from the parameter and calls the get_user_data function.
        """
        self.user_token = token  # We are getting the token from here
        return await self.get_user_data()

# Singleton sample
default_fetcher = DataFetcher()

def get_data(token):
    """
    A basic function for external access.

    Can be used for external access with token.
    """
    global global_data, _initialized

    # If data was not load
    if not _initialized:
        # Gather data by token
        global_data = default_fetcher.get_user_data_sync(token)
        _initialized = True

    return global_data

# Gather data with this testing script
if __name__ == "__main__":
    print(get_data(USER_TOKEN))