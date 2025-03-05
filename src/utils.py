import numpy as np
from typing import List

def prepare_features(input_data: dict) -> List[float]:
    """Convert input dictionary to feature array in correct order"""
    feature_order = [
        'mdvp_fo', 'mdvp_fhi', 'mdvp_flo', 'mdvp_jitter_percent',
        'mdvp_jitter_abs', 'mdvp_rap', 'mdvp_ppq', 'jitter_ddp',
        'mdvp_shimmer', 'mdvp_shimmer_db', 'shimmer_apq3', 'shimmer_apq5',
        'mdvp_apq', 'shimmer_dda', 'nhr', 'hnr', 'rpde', 'dfa',
        'spread1', 'spread2', 'd2', 'ppe'
    ]
    
    return [input_data[feature] for feature in feature_order]