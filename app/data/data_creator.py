# Data creation operations
import aiohttp
import asyncio
from typing import Dict, Any
from app.core.config import USER_TOKEN
from app.data.dataframe_builder import DataFrameBuilder

# Class for API data
class ApiDataManager:
    def __init__(self, access_token: str):
        self.api_datam: Dict[str, Any] = {}
        self.base_url = "http://localhost:xxxx"  # The base URL connects to the data server
        self.access_token = access_token
        self.endpoints = [
            # Get your data from API like that (change request types and URLs)
            # {
            #     "name": "tires",
            #     "url": f"{self.base_url}/getalltires",
            #     "headers": {
            #         "Content-Type": "application/json",
            #     }
            # },
            # {
            #     "name": "cars",
            #     "url": f"{self.base_url}/getallcars",
            #     "headers": {
            #         "Content-Type": "application/json",
            #     }
            # },
        ]

    async def send_api_request(self, session, endpoint):
        try:
            async with session.get(endpoint["url"], headers=endpoint["headers"], json={}) as response:
                if response.status == 200:
                    # If success, save the response to api_datam variable
                    api_data = await response.json()
                    self.api_datam[endpoint["name"]] = DataFrameBuilder.build(api_data)
                    print(f"{endpoint['name']} data successfully gathered.")

                else:
                    print(f"{endpoint['name']} API request is unsuccessful. Error code: {response.status}")

        except Exception as e:
            print(f"{endpoint['name']} an error occurred during the API process: {str(e)}")

    async def fetch_all_data(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.send_api_request(session, endpoint) for endpoint in self.endpoints]
            await asyncio.gather(*tasks)

    def get_data(self):
        """Returns API data"""
        return self.api_datam

# Start gathering data process
async def initialize_data(access_token: str):
    data_manager = ApiDataManager(access_token=access_token)
    await data_manager.fetch_all_data()
    return data_manager.get_data()

# Run this script for directly gathering data
if __name__ == "__main__":
    asyncio.run(initialize_data(USER_TOKEN))
