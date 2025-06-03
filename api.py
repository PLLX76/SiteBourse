import cloudscraper
from datetime import datetime, timedelta
import requests # Required for requests.exceptions.RequestException

scraper = cloudscraper.create_scraper()

def get_iframe_code(url, period):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
        "Referer": url,
    }

    cookies = {
        "__RequestVerificationToken": "4i9Si8sK96eKzw8Bt4NytN56pj9_Ght9zW0zrjgOKUcQuDoHVLpjuKaVGIbmqHpUtPInvVoDEeth1ve0vh8hP5Uy6rQMFcP2UmrRUsN5m2k1",
        "ak_bmsc": "3D09EA1964A5ECE25414F5D55693012A~000000000000000000000000000000~YAAQoY8QAiGIRdWWAQAA+L2SLBt3qnZV6mzQ3xBpWEuNcgyJJGIczrvt85gZSB/DSpmJR0E9Wdr7gm8JtwEq0GtZxTMVIFfgWsXMJ3KYpf4CvYPhou1YizskmQyxqDmeQDLv0fxd9ThKkHJLtLFNKKP8mYsEJaswAz0K+4m4pHOF+MzaOoILMBx/qHjKb4d3F+LTtLpZORww6qMsqqRKfPmQOWTkzdEfBo54A5GUsj5SKkjfRyv2OCXftl5tVQoWLCMAErLst/8dBju7WDccVx/0lwlNgjrkzGbJrxYYioQyXqCrbVR4c2h6TgXopKpNI6mo6bpmVnZ7XTMkSeLrD/os3P6OfCoe+5/73mC3KPo4ydMYPqn7IEDyyk7/gPluHOBcrXuK9R4LTDL8aRWtMl2Hhu44FQJut+NO2pzpSWXBIHI=",
        "ansid": "vpysth45uhuicqekry5zpc4h",
        "bm_sv": "04961908732B24C3B67941690E45AA9D~YAAQlY8QAriA1tKWAQAARk7KLBulFq5SILbd4cpjJFQjzdIxvv2n7+EmftDjSovqswoC5DDsFSng4MH2jafZnADdKT0/lO6y48ZAA4pmcYE/0HKSzOaVQ9sGIZibteUTfGBdVZedDCDmBFAfQ5sz3BBdVolThOhNgczNJQJLkF0CLNEGdBs3BPKuQ3k2gRsBGH5m5NrjL5SuqJ4jGdzJm36aT2QFI82BsC7PhfmqgiXVkU7Tpd3iZl2gYCZpRkUUdz89dA==~1",
        "didomi_token": "eyJ1c2VyX2lkIjoiMTk3MmIxNzItMTM4Ni02MmRiLWFiNjktZTJkZmJkYTE1MTUxIiwiY3JlYXRlZCI6IjIwMjUtMDYtMDFUMTA6NDM6NDUuNTkyWiIsInVwZGF0ZWQiOiIyMDI1LTA2LTAxVDEwOjQzOjUyLjcwOFoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwidHdpdHRlciJdfX0=",
        "euconsent-v2": "CQSU_AAQSU_AAAHABBENBsFsAP_gAAAAAAAAJoBB9G5X...",
        "GCLB": "\"bb321dc9e153090f\"",
        "tabs-mini-graph": "3"
    }

    data = {
        "__RequestVerificationToken": "bnRaNDM6EBGTH51WHxGpD7uvpd4Ed4M-hc9wE2kWs1Xi6k2WiLXVdFr5x9bFdFTmC-9W7hfKKgrhs53XjfhqKgmZNlGGV9g7k2Og8C3oE281",
        "ftp": "candle",
        "ftv": "column",
        "flgd": "0",
        "code": "FR",
        "Period": str(period),
        "DateStart": "",
        "DateEnd": "",
        "AM1": "50",
        "AM2": "200",
        "AM3": "100",
        "Action1": "",
        "Action2": "",
        "Action3": "",
        "Index1": "",
        "Index2": "",
    }

    try:
        response = scraper.post(url, headers=headers, cookies=cookies, data=data)
        # if "FR0003500008" in url:
        #     with  open("cac_boursier_response.html", "w", encoding="utf-8") as f:
        #         f.write(response.text)
        # elif "XC0009694271" in url:
        #     with  open("nasdaq_boursier_response.html", "w", encoding="utf-8") as f:
        #         f.write(response.text)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4XX or 5XX)
        
        # Extract the iframe src URL
        iframe_src_parts = response.text.split('<iframe id="chartBig" src="')
        if len(iframe_src_parts) > 1:
            iframe_url_val = iframe_src_parts[1].split('"')[0]
            # Ensure it's a full URL, typically starts with // or http(s)
            if iframe_url_val.startswith("//"):
                full_iframe_url = "https:" + iframe_url_val
            elif iframe_url_val.startswith("http"):
                full_iframe_url = iframe_url_val
            else:
                print(f"Error: iframe src has unexpected format: {iframe_url_val} for URL {url}")
                return None
            return full_iframe_url # Return the full URL
        else:
            print(f"Error: '<iframe id=\"chartBig\" src=' not found or malformed in response for {url}. Response text: {response.text[:500]}...")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for Boursier URL {url}: {e}")
        return None
    except IndexError:
        print(f"Error parsing iframe URL from Boursier response for {url}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching Boursier data for {url}: {e}")
        return None

def get_just_etf(url, period:int):
    headers = {
        "Accept": "application/json, text/plain, */*"
    }
    code = url.split('?isin=')[1].split('&')[0].split('#')[0]
    today_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    if period == 0: # Corrected: period is an int
        period_date = (datetime.now() - timedelta(days=16)).strftime('%Y-%m-%d')
    else:
        period_date = (datetime.now() - timedelta(days=int(period)*30 + 1)).strftime('%Y-%m-%d')
    new_url = f'https://www.justetf.com/api/etfs/{code}/performance-chart?locale=fr&currency=EUR&valuesType=MARKET_VALUE&reduceData=false&includeDividends=false&features=DIVIDENDS&dateFrom={period_date}&dateTo={today_date}'
    try:
        response = scraper.get(new_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed for JustETF URL {new_url}: {e}")
        return None
    except ValueError as e: # Handles JSON decoding errors
        print(f"Failed to decode JSON from JustETF URL {new_url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching JustETF data for {new_url}: {e}")
        return None

EPOCH_DATE = datetime(1970, 1, 1)
    
def get_boursorama(url, period_val:int):
    headers = {
        "Accept": "application/json, text/plain, */*"
    }
    # url exemple : https://www.boursorama.com/bourse/indices/cours/2cSXXP/
    code = url.split('/')[-2]

    length_days = 0
    if period_val == 0: # 15 days
        length_days = 15
    elif period_val == 1: # 1 month
        length_days = 30
    elif period_val == 3: # 3 months
        length_days = 90
    elif period_val == 6: # 6 months
        length_days = 180
    elif period_val == 12: # 1 year (approx 260 trading days, Boursorama API might handle this)
        length_days = 260 
    elif period_val == 24: # 2 years
        length_days = 520
    elif period_val == 36: # 3 years
        length_days = 780
    elif period_val == 60: # 5 years
        length_days = 1300 # Approx 5 * 260
    else: # Default or unknown
        length_days = 30 # Default to 1 month

    # Boursorama API 'period' param: 0 for daily, 1 for weekly, etc. We want daily.
    boursorama_api_granularity_param = 0
    new_url = f"https://www.boursorama.com/bourse/action/graph/ws/GetTicksEOD?symbol={code}&length={length_days}&period={boursorama_api_granularity_param}&guid="
    
    try:
        response = scraper.get(new_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        parsed_series = []
        if data and 'd' in data and 'QuoteTab' in data['d']:
            for quote_item in data['d']['QuoteTab']:
                # quote_item is an object like: {"d": 20241, "o": ..., "c": ..., ...}
                # 'c' is the closing price.
                # 'd' is the number of days since 1970-01-01.
                if isinstance(quote_item, dict) and 'c' in quote_item and 'd' in quote_item:
                    closing_price = quote_item['c']
                    days_since_epoch = quote_item['d']
                    actual_date = EPOCH_DATE + timedelta(days=days_since_epoch)
                    # Convert to milliseconds timestamp for consistency with frontend expectations
                    timestamp_ms = int(actual_date.timestamp() * 1000)
                    parsed_series.append({
                        "date": timestamp_ms,
                        "value": {"raw": closing_price}
                    })
                else:
                    print(f"Warning: Unexpected item format in Boursorama QuoteTab: {quote_item}")
            return {
                "series": parsed_series,
                "name": f"Boursorama {code}"
            }
        else:
            print(f"Error: Unexpected data format from Boursorama API for {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for Boursorama URL {new_url}: {e}")
        return None
    except ValueError as e: # Handles JSON decoding errors
        print(f"Failed to decode JSON from Boursorama URL {new_url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching Boursorama data for {new_url}: {e}")
        return None
        
if __name__ == "__main__":    
    # url = "https://www.boursier.com/indices/graphiques/cac-40-FR0003500008,FR.html"
    # get_iframe_code(url, '1')
    # Test Boursorama
    boursorama_url = "https://www.boursorama.com/bourse/indices/cours/2cSXXP/"
    print(get_boursorama(boursorama_url, 1)) # Test for 1 month
    # print(get_boursorama(boursorama_url, 0)) # Test for 15 days
