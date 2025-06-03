from flask import Flask,redirect,url_for,render_template,request, jsonify
from api import get_iframe_code, get_just_etf, get_boursorama
import re

app=Flask(__name__)

links = [
    "https://www.justetf.com/fr/etf-profile.html?isin=IE00B4L5Y983#apercu",
    "https://www.justetf.com/fr/etf-profile.html?isin=IE0002Y8CX98#apercu",
    "https://www.justetf.com/fr/etf-profile.html?isin=IE000YYE6WK5#apercu",
    "https://www.justetf.com/fr/etf-profile.html?isin=LU0908500753#apercu",
    "https://www.boursier.com/indices/graphiques/cac-40-FR0003500008,FR.html",
    # "https://www.boursier.com/indices/cours/nasdaq-composite-XC0009694271,US.html"
    "https://www.boursier.com/indices/graphiques/nasdaq-composite-XC0009694271,US.html",
    "https://www.boursorama.com/bourse/indices/cours/2cSXXP/"
]

# Simple in-memory cache
api_cache = {}

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route("/api/period/<int:period_val>")
def api_endpoint(period_val: int):
    results = []
    str_period = str(period_val) # For boursier.com API which expects string period
    print(f"Requesting data for period: {period_val}")

    for link in links:
        cache_key = (link, period_val)
        
        if cache_key in api_cache:
            print(f"Cache HIT for {link} with period {period_val}")
            results.append(api_cache[cache_key])
            continue
        
        print(f"Cache MISS for {link} with period {period_val}")
        current_item_data = None

        try:
            if 'justetf' in link:
                etf_data = get_just_etf(link, period_val) # period_val is int
                isin_code = link.split('?isin=')[1].split('&')[0].split('#')[0]
                if etf_data and isinstance(etf_data, dict):
                    etf_data['isin'] = isin_code
                    etf_data['name'] = f"ETF {isin_code}"
                    etf_data['type'] = "justetf"
                    current_item_data = etf_data
                else:
                    current_item_data = {
                        "type": "justetf",
                        "isin": isin_code,
                        "name": f"ETF {isin_code} (Erreur de chargement)",
                        "error": etf_data if isinstance(etf_data, str) else "Failed to load data from JustETF",
                        "series": []
                    }
            elif 'boursier' in link:
                s1_param = "ERROR"
                match = re.search(r'([A-Z0-9]+,[A-Z]{2})\.html$', link)
                if match:
                    s1_param = match.group(1)
                else:
                    print(f"Warning: Could not extract s1_param from boursier link: {link}")

                filename_no_ext = link.split('/')[-1].replace('.html', '')
                name_candidate = filename_no_ext
                if s1_param != "ERROR":
                    name_candidate = name_candidate.replace(f'-{s1_param}', '').replace(s1_param, '')
                
                display_name = name_candidate.replace('-', ' ').title().strip()
                
                iframe_url_from_api = get_iframe_code(link, str_period)
                if iframe_url_from_api:
                    current_item_data = {
                        "type": "boursier",
                        "iframe_url": iframe_url_from_api,
                        "name": display_name if display_name else "Boursier Chart",
                        "original_link": link
                    }
                else:
                    current_item_data = {
                        "type": "boursier", "iframe_url": None,
                        "name": f"{display_name if display_name else 'Boursier Chart'} (Erreur de chargement)",
                        "original_link": link, "error": "Failed to load iframe URL from Boursier"
                    }
            elif 'boursorama.com/bourse/indices/cours/' in link:
                code_from_link_match = re.search(r'/cours/([^/]+)/?$', link)
                default_chart_name = f"Boursorama {code_from_link_match.group(1)}" if code_from_link_match else "Boursorama Index"

                boursorama_data = get_boursorama(link, period_val)
                if boursorama_data and isinstance(boursorama_data, dict) and 'series' in boursorama_data:
                    current_item_data = {
                        "type": "boursorama",
                        "name": boursorama_data.get("name", default_chart_name),
                        "series": boursorama_data["series"],
                        "original_link": link
                    }
                else:
                    current_item_data = {
                        "type": "boursorama",
                        "name": f"{default_chart_name} (Erreur de chargement)",
                        "error": boursorama_data if isinstance(boursorama_data, str) else "Failed to load data from Boursorama",
                        "series": [],
                        "original_link": link
                    }
            
            if current_item_data:
                api_cache[cache_key] = current_item_data
                results.append(current_item_data)
            else:
                # Should not happen if all link types are handled
                print(f"Warning: No data was processed for link {link}")
        except Exception as e:
            print(f"Error processing link {link}: {e}")
            # Add a generic error item to results and cache it
            error_item = {"type": "error", "name": f"Erreur de traitement pour {link}", "error": str(e), "original_link": link}
            api_cache[cache_key] = error_item
            results.append(error_item)

    return jsonify(results)
    
if __name__ == '__main__':
    app.run(port=5000,debug=False)