def create_config(**kwargs):
    print("Original kwargs:", kwargs)

    # Create a copy using unpacking
    config1 = {**kwargs}
    print("Using {**kwargs}:", config1)

    # Create a copy using dict()
    config2 = dict(kwargs)
    print("Using dict(kwargs):", config2)

    # Create a copy using copy()
    config3 = kwargs.copy()
    print("Using kwargs.copy():", config3)

    # Merge with default config
    default_config = {'debug': False, 'port': 8000, 'mode': 'production'}
    merged_config = {**default_config, **kwargs}
    print("Merged with defaults:", merged_config)

# Test it
create_config(debug=True, port=5000, extra='enabled')
