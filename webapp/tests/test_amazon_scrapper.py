import website.amazonscrapper as AWSC
import os

def test_get_url():
    search_term = 'test'
    url = AWSC.get_url(search_term)
    assert 'test' in url

def test_scrapper():
    search_term = '3060'
    path = 'test_gpu.csv'
    AWSC.runSearch(search_term, path)
    assert os.path.exists('test_gpu.csv') == True

def test_parser_record():
    path = 'test_gpu.csv'
    