def load_dataset(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def clean_data(data):
    # Implement data cleaning steps here
    return data.dropna()

def normalize_data(data):
    # Implement normalization steps here
    return (data - data.min()) / (data.max() - data.min())

def split_data(data, test_size=0.2):
    from sklearn.model_selection import train_test_split
    return train_test_split(data, test_size=test_size)