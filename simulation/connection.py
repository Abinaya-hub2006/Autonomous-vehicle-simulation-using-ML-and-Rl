import os
import sys
import glob

# This code block handles finding the carla.egg file in the project structure
# It must be present to ensure the correct version of the API is loaded.
try:
    sys.path.append(glob.glob('./carla/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    print('Couldn\'t import Carla egg properly')

import carla
from simulation.settings import PORT, TIMEOUT, HOST

class ClientConnection:
    def __init__(self, town):
        self.client = None
        self.town = town

    def setup(self):
        # The client variable must be defined outside the try block if used later (handled in continuous_driver.py)
        
        try:
            # Connecting to the Server using parameters from settings.py
            self.client = carla.Client(HOST, PORT)
            self.client.set_timeout(TIMEOUT)
            
            # Load the specified town map
            self.world = self.client.load_world(self.town)
            self.world.set_weather(carla.WeatherParameters.CloudyNoon)
            
            return self.client, self.world

        except Exception as e:
            # If connection fails, print the error and call the error method
            print(
                'Failed to make a connection with the server: {}'.format(e))
            self.error()
            # Note: A return None, None is often assumed here by the caller function (continuous_driver.py)

    # An error method: prints out the details if the client failed to make a connection
    def error(self):
        # This method assumes self.client was successfully instantiated, but handles the case where it wasn't.
        # This logic is error-prone if connection completely fails, but is preserved from the original project code.
        try:
            print("\nClient version: {}".format(
                self.client.get_client_version()))
            print("Server version: {}\n".format(
                self.client.get_server_version()))

            if self.client.get_client_version != self.client.get_server_version:
                print(
                    "There is a Client and Server version mismatch! Please install or download the right versions.")
        except:
            # Catch secondary errors (like trying to access a NoneType client object)
            pass