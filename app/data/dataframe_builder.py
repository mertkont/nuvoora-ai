# JSON to DataFrame conversions
from typing import Optional

# DataFrameBuilder class
class DataFrameBuilder:
    @staticmethod
    def build(api_data: dict, key: Optional[str] = None) -> dict:
        if not api_data:
            return {}
        if key:
            # Returns the data by a key
            data = api_data.get(key, [])
        else:
            # Returns the entire data structure as is
            data = api_data
        return data