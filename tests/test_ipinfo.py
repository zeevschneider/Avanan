import pytest
import requests
import re

benchmark_url = 'https://geolocation-db.com/json/161.185.160.93'
api_base_url = 'https://ipinfo.io/161.185.160.93'


@pytest.fixture(scope='function')
def get_requests_benchmark():
    try:
        response = requests.get(benchmark_url).json()
    except Exception:
        raise "Could mot receive data on {url}"

    return response


# Verify country code in the api general request is identical to the one in benchmark url
def test_verify_country_code_all_doc(get_requests_benchmark):
    response = requests.get(f"{api_base_url}/geo").json()
    assert response['country'] == get_requests_benchmark['country_code']


# Verify country code in the api /country endpoint is identical to the one in benchmark url
def test_verify_country_code_all_doc(get_requests_benchmark):
    response = requests.get(f"{api_base_url}/country")
    assert response.text.strip() == get_requests_benchmark['country_code']


# Verify postal code in /postal endpoint response
def test_verify_postal():
    response = requests.get(f"{api_base_url}/postal")
    assert response.text.strip() == '10004'


# Test non existing endpoint
def test_non_existing_endpoint():
    non_existing_endpoint = "end_point"
    expected_result = '{"status":400,"error":{"title":"Wrongmoduleorfieldtype","message":"Nomoduleorfieldoftype' \
                      '\'end_point\'exists.Pleasecheckourdocumentationhttps://ipinfo.io/developers."}}'
    response = requests.get(f"{api_base_url}/{non_existing_endpoint}")

    treated_response = re.sub(r"[\n\t\s]*", "", response.text)

    assert treated_response == expected_result


