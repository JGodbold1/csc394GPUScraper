import os
from website.parser import createAmazonTuple

def test_parsed_tuple():
    """Tests if the parser correctly return the desired tuple"""
    file = os.path.isfile('test_gpu.csv')
    assert file is True
    test_record = createAmazonTuple('test_gpu.csv')
    assert len(test_record) is not None
    
    