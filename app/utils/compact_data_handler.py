# Compresses long/data-heavy content
import json
import base64
import zlib
import numpy as np
import pandas as pd
from typing import Dict, List

class CompactDataHandler:
    """
    A super-compact representation of large data sets.

    Ultra-optimized for data embedding scenarios in LLM prompts.
    """

    def __init__(self):
        self.compression_level = 9  # Maximum compression level
        self.encoding_format = 'utf-8'
        self.field_abbreviations = {}  # Abbreviations

    def generate_field_abbreviations(self, data_dict: Dict[str, List]) -> Dict[str, str]:
        """Abbreviations for the data fields"""
        abbreviations = {}
        seen = set()

        for field_name in data_dict.keys():
            # Start with one-charactered abbreviations
            if len(field_name) > 0:
                abbr = field_name[0].lower()
                counter = 0
                while abbr in seen:
                    counter += 1
                    # Use the next letter of the alphabet, or use a number
                    if counter < 26:
                        abbr = chr(97 + counter)  # Start with a
                    else:
                        abbr = f"{field_name[0].lower()}{counter - 25}"
                seen.add(abbr)
                abbreviations[field_name] = abbr

        return abbreviations

    def compress_binary(self, data: bytes) -> str:
        """Ultra-compress binary data and encode with base64"""
        compressed = zlib.compress(data, level=self.compression_level)
        return base64.b64encode(compressed).decode(self.encoding_format)

    def decompress_binary(self, encoded_data: str) -> bytes:
        """Decode Base64 encoded and compressed data"""
        decoded = base64.b64decode(encoded_data.encode(self.encoding_format))
        return zlib.decompress(decoded)

    def create_compact_json(self, data_dict: Dict[str, List]) -> str:
        """Converts data dictionary to ultra-compact JSON format"""
        self.field_abbreviations = self.generate_field_abbreviations(data_dict)

        # Convert data to minimal data structure, not matrices
        # Use flat structure instead of nested structure
        df = pd.DataFrame(data_dict)

        # Detect numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Create compact data - do not use nested structure
        data_array = []
        for _, row in df.iterrows():
            compact_row = {}
            for col in df.columns:
                abbr = self.field_abbreviations[col]
                # Round numeric values
                if col in numeric_cols:
                    compact_row[abbr] = round(float(row[col]), 2) if not pd.isna(row[col]) else None

                else:
                    compact_row[abbr] = row[col] if not pd.isna(row[col]) else None

            data_array.append(compact_row)

        # Minimize Legends value
        result = {
            "l": {v: k for k, v in self.field_abbreviations.items()},  # legend -> l
            "d": data_array  # data -> d
        }

        return json.dumps(result, separators=(',', ':'))

    def compress_json(self, data_dict: Dict[str, List]) -> str:
        """Ultra-compresses JSON data and encodes it with base64"""
        json_str = self.create_compact_json(data_dict)
        # Use base64 only - we had problems with base85
        return self.compress_binary(json_str.encode(self.encoding_format))

    def summarize_data(self, data_dict: Dict[str, List], sample_size: int = 2) -> Dict:
        """Extracts minimal summary statistics of the dataset"""
        df = pd.DataFrame(data_dict)
        total_rows = len(df)

        # Determine numeric and categorical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

        # Minimal summary
        summary = {
            "r": total_rows,  # rows -> r
            "c": len(df.columns),  # columns -> c
            "t": {col: str(df[col].dtype)[0] for col in df.columns}  # types -> t
        }

        # For numeric columns only min, max, mean
        if numeric_cols:
            summary["n"] = {}  # numeric -> n
            for col in numeric_cols:
                summary["n"][col] = {
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                    "avg": float(df[col].mean())
                }

        # Only unique value count for categorical columns
        if categorical_cols:
            summary["k"] = {}  # categorical -> k
            for col in categorical_cols:
                summary["k"][col] = df[col].nunique()

        # Minimal example - only first 2 lines
        if total_rows > 0 and sample_size > 0:
            samples = df.head(min(sample_size, total_rows)).to_dict('records')
            summary["s"] = samples  # samples -> s

        return summary

    def create_layered_representation(self, data_dict: Dict[str, List],
                                      include_full: bool = False) -> Dict:
        """Creates ultra-compact layered data representation"""
        # Minimal summary only
        representation = self.summarize_data(data_dict, sample_size=1)  # Only one sample

        # Optional full data (compressed)
        if include_full:
            representation["f"] = self.compress_json(data_dict)  # full -> f

        return representation

    def prepare_for_prompt(self, data_dict: Dict[str, List],
                           max_tokens: int = 500) -> str:
        """Prepares ultra-compact data representation for LLM prompt"""
        # Use only compressed format
        return self.compress_json(data_dict)

    def encode_for_embedding(self, data_dict: Dict[str, List]) -> Dict:
        """Prepares minimal data for embedding operations"""
        # Basic statistics only
        df = pd.DataFrame(data_dict)

        features = {
            "rows": len(df),
            "cols": len(df.columns)
        }

        # Only average values for numeric columns
        for col in df.select_dtypes(include=[np.number]).columns:
            features[f"{col}_avg"] = float(df[col].mean())

        return features


# Test
if __name__ == "__main__":
    # Sample data
    sample_data = {
        "user_id": [1, 2, 3, 4, 5],
        "age": [25, 34, 47, 29, 50],
        "income": [5000, 7500, 12000, 6000, 15000],
        "category": ["A", "B", "A", "C", "B"],
        "is_active": [True, False, True, True, False]
    }

    handler = CompactDataHandler()

    # 1. Normal compact JSON
    compact_json = handler.create_compact_json(sample_data)
    print(f"Compact JSON size: {len(compact_json)} character")

    # 2. Compressed format
    compressed = handler.compress_json(sample_data)
    print(f"Compressed format size: {len(compressed)} character")

    # 3. Prepare for the prompt - only the compressed data
    prompt = handler.prepare_for_prompt(sample_data)
    print(f"Prompt size: {len(prompt)} character")
    print(f"Content: {prompt}")

    # Decompression test - do we open the data?
    print("\nData Validation Test:")
    try:
        # Use base64 code directly
        compressed_data = prompt

        decoded = base64.b64decode(compressed_data.encode('utf-8'))
        decompressed = zlib.decompress(decoded).decode('utf-8')
        data = json.loads(decompressed)

        # Do legend and data true?
        print(f"Legend keys: {list(data['l'].keys())}")
        print(f"Data keys: {list(data['d'][0].keys()) if isinstance(data['d'], list) else 'N/A'}")
        print(f"First user: {data['d'][0] if isinstance(data['d'], list) else 'N/A'}")
        print(f"Data successfully decompressed!")
    except Exception as e:
        print(f"Error: {e}")