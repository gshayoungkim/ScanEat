from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import requests
import urllib.parse
import re
from html.parser import HTMLParser
from datetime import datetime


load_dotenv()


app = Flask(__name__)


# ★ Supabase 설정 ★
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# API 키
SERVICE_KEY = os.getenv('SERVICE_KEY')
FOODQR_ACCESS_KEY = os.getenv('FOODQR_ACCESS_KEY')
FOOD_SAFETY_API_KEY = os.getenv('FOOD_SAFETY_API_KEY')  # C005 API용 키


# API URL
HACCP_API_URL = 'https://apis.data.go.kr/B553748/CertImgListServiceV3/getCertImgListServiceV3'
FOOD_QR_API_URL = 'https://foodqr.kr/openapi/service/qr1007/F007'
BARCODE_LINK_API_URL = 'http://openapi.foodsafetykorea.go.kr/api'  # C005 바코드연계제품정보


# 카테고리별 원재료 매핑
INGREDIENTS_TO_CHECK = {
    '소고기': {
        'english': 'Beef',
        'keywords': ['소고기', '쇠고기', '우육', '비프', '등심', '안심', '채끝', '양지', '사태', '우둔', '설도', '갈비', '육우']
    },
    '돼지고기': {
        'english': 'Pork',
        'keywords': ['돼지고기', '돼지', '포크', '베이컨', '햄', '삼겹살', '목살', '라드']
    },
    '닭고기': {
        'english': 'Chicken',
        'keywords': ['닭', '닭고기', '치킨', '가금류', '닭가슴살', '닭다리', '닭봉']
    },
    '우유': {
        'english': 'Milk & Dairy',
        'keywords': ['우유', '유제품', '치즈', '버터', '생크림', '연유', '유당', '유청', '카제인', '분유', '유크림', '우유알레르기']
    },
    '계란': {
        'english': 'Egg',
        'keywords': ['계란', '달걀', '알류', '난백', '난황', '전란', '계란흰자', '계란노른자']
    },
    '메밀': {
        'english': 'Buckwheat',
        'keywords': ['메밀', '메밀가루', '메밀국수', '소바', '메밀묵']
    },
    '밀': {
        'english': 'Wheat',
        'keywords': ['밀', '밀가루', '글루텐', '밀글루텐', '밀배아']
    },
    '대두': {
        'english': 'Soybean',
        'keywords': ['대두', '콩', '두유', '두부', '된장', '간장', '콩제품', '소이', '서리태']
    },
    '땅콩': {
        'english': 'Peanut',
        'keywords': ['땅콩', '피넛', '땅콩버터', '땅콩유']
    },
    '호두': {
        'english': 'Walnut',
        'keywords': ['호두', '월넛', '호두유']
    },
    '잣': {
        'english': 'Korean Pine Nut',
        'keywords': ['잣', '솔씨']
    },
    '고등어': {
        'english': 'Mackerel',
        'keywords': ['고등어', '고등어알', '고등어젓']
    },
    '생선류': {
        'english': 'Fish',
        'keywords': ['생선', '어류', '참치', '연어', '멸치', '어분', '생선까나리', '어유']
    },
    '게': {
        'english': 'Crab',
        'keywords': ['게', '크랩', '게살', '게다리']
    },
    '새우': {
        'english': 'Shrimp',
        'keywords': ['새우', '새우류', '랍스터', '새우젓', '새우액젓', '왕새우']
    },
    '오징어': {
        'english': 'Squid',
        'keywords': ['오징어', '오징어채', '오징어젓', '오징어먹물']
    },
    '조개류': {
        'english': 'Shellfish',
        'keywords': ['조개류', '굴', '전복', '홍합', '바지락', '조개', '굴젓', '전복손질']
    },
    '복숭아': {
        'english': 'Peach',
        'keywords': ['복숭아', '복숭아주스', '복숭아시럽']
    },
    '토마토': {
        'english': 'Tomato',
        'keywords': ['토마토', '토마토소스', '토마토페이스트', '토마토케첩']
    },
    '아황산류': {
        'english': 'Sulfites',
        'keywords': ['아황산류', '아황산염', '아황산', '이산화황', '황산염', '차아황산']
    },
    '젤라틴': {
        'english': 'Gelatin',
        'keywords': ['젤라틴', '젤라틴']
    }
}


print(f"\n{'='*60}")
print("Environment Check:")
print(f"SERVICE_KEY: {'✓ SET' if SERVICE_KEY else '✗ NOT SET'}")
print(f"FOODQR_ACCESS_KEY: {'✓ SET' if FOODQR_ACCESS_KEY else '✗ NOT SET'}")
print(f"FOOD_SAFETY_API_KEY: {'✓ SET' if FOOD_SAFETY_API_KEY else '✗ NOT SET'}")
print(f"SUPABASE_URL: {'✓ SET' if SUPABASE_URL else '✗ NOT SET'}")
print(f"SUPABASE_KEY: {'✓ SET' if SUPABASE_KEY else '✗ NOT SET'}")
print(f"{'='*60}\n")


class HTMLStripper(HTMLParser):
    """HTML 태그 제거"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []


    def handle_data(self, d):
        self.text.append(d)


    def get_data(self):
        return ''.join(self.text)


def strip_html(html_text):
    """HTML 태그 제거 함수"""
    if not html_text:
        return ''
    
    stripper = HTMLStripper()
    try:
        stripper.feed(html_text)
        return stripper.get_data().replace('\n', '').replace('  ', ' ').strip()
    except:
        text = re.sub(r'<[^>]+>', '', html_text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()


def find_ingredients(raw_materials):
    """원재료명에서 해당하는 모든 원재료 검출"""
    found_ingredients = {}
    
    for category, data in INGREDIENTS_TO_CHECK.items():
        detected_keywords = []
        
        for keyword in data['keywords']:
            if keyword in raw_materials:
                detected_keywords.append(keyword)
        
        if detected_keywords:
            found_ingredients[category] = {
                'english': data['english'],
                'detected': detected_keywords
            }
    
    return found_ingredients


def search_custom_database(search_value):
    """Supabase에서 검색"""
    try:
        response = (
            supabase.table('custom_products')
            .select('*')
            .eq('barcode', search_value)
            .execute()
        )
        
        if not response.data or len(response.data) == 0:
            response = (
                supabase.table('custom_products')
                .select('*')
                .eq('imrpt_no', search_value)
                .execute()
            )
        
        if response.data and len(response.data) > 0:
            product = response.data[0]
            print(f"[Supabase] ✓ Found: {product['product_name']}")
            return {
                'source': 'Custom Database',
                'product': {
                    'prdctNm': product['product_name'],
                    'prvwCn': product['raw_materials']
                }
            }
        return None
        
    except Exception as e:
        print(f"[Supabase Error] {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def search_barcode_link_api(barcode):
    """
    ★ C005 바코드연계제품정보 API로 바코드 → 품목보고번호 매핑 ★
    """
    try:
        if not FOOD_SAFETY_API_KEY:
            print("[C005] API Key not set")
            return None
        
        # ✅ 올바른 URL 구성: 파라미터를 경로에 포함
        # 형식: /api/{인증키}/C005/{dataType}/{startIdx}/{endIdx}/BAR_CD={바코드값}
        url = f"{BARCODE_LINK_API_URL}/{FOOD_SAFETY_API_KEY}/C005/json/1/100/BAR_CD={barcode}"
        
        print(f"[C005] Searching barcode: {barcode}")
        print(f"[C005] Request URL: {url}")
        
        # params 없이 직접 URL로 요청
        response = requests.get(url, timeout=15)
        
        print(f"[C005] Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"[C005] Failed with status {response.status_code}")
            print(f"[C005] Response: {response.text[:500]}")
            return None
        
        result = response.json()
        print(f"[C005] Response: {result}")
        
        # 응답 구조: {"C005": {"total_count": "1", "row": [...], "RESULT": {...}}}
        if result.get('C005'):
            c005_data = result['C005']
            
            # 에러 코드 체크
            result_info = c005_data.get('RESULT', {})
            result_code = result_info.get('CODE')
            result_msg = result_info.get('MSG')
            
            print(f"[C005] Result Code: {result_code}")
            print(f"[C005] Result Message: {result_msg}")
            
            # INFO-000: 정상 처리
            # INFO-200: 해당하는 데이터가 없습니다
            if result_code == 'INFO-200':
                print("[C005] No data found for this barcode")
                return None
            
            if result_code and result_code != 'INFO-000':
                print(f"[C005] API Error: {result_code} - {result_msg}")
                return None
            
            rows = c005_data.get('row', [])
            total_count = c005_data.get('total_count', '0')
            
            print(f"[C005] Total count: {total_count}")
            
            if rows and len(rows) > 0:
                # 첫 번째 결과 사용
                product = rows[0]
                report_no = product.get('PRDLST_REPORT_NO')
                product_name = product.get('PRDLST_NM', 'Unknown')
                
                print(f"[C005] ✓ Found mapping: {barcode} → {report_no}")
                print(f"[C005] Product: {product_name}")
                
                return {
                    'product_report_no': report_no,
                    'product_name': product_name,
                    'barcode': barcode,
                    'manufacturer': product.get('BSSH_NM', ''),
                    'product_type': product.get('PRDLST_DCNM', ''),
                    'report_date': product.get('PRMS_DT', ''),
                    'address': product.get('SITE_ADDR', '')
                }
        
        print("[C005] No data found in response")
        return None
        
    except requests.exceptions.Timeout:
        print("[C005] Request timeout")
        return None
    except Exception as e:
        print(f"[C005] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def search_haccp_api(search_value):
    """HACCP API에서 검색"""
    try:
        params = {
            'serviceKey': urllib.parse.unquote(SERVICE_KEY),
            'prdlstReportNo': search_value,
            'returnType': 'json',
            'numOfRows': 100,
            'pageNo': 1
        }
        
        print(f"[HACCP] Searching with product number: {search_value}")
        response = requests.get(HACCP_API_URL, params=params, timeout=15)
        
        print(f"[HACCP] Status Code: {response.status_code}")
        
        if response.status_code != 200:
            return None
        
        result = response.json()
        
        if result.get('body') and result['body'].get('items'):
            items = result['body']['items']
            
            if isinstance(items, dict):
                items = [items]
            
            first_item = items[0]
            
            if 'item' in first_item:
                product = first_item['item']
            else:
                product = first_item
            
            print(f"[HACCP] ✓ Found product: {product.get('prdlstNm', 'Unknown')}")
            
            return {
                'source': 'HACCP',
                'product': product
            }
        
        return None
        
    except Exception as e:
        print(f"[HACCP] Error: {str(e)}")
        return None


def search_foodqr_api(search_value):
    """Food QR API에서 검색"""
    
    search_params_list = [
        {
            'name': 'product report number (imrptNo)',
            'params': {
                'accessKey': FOODQR_ACCESS_KEY,
                'numOfRows': 10,
                'pageNo': 1,
                '_type': 'json',
                'imrptNo': search_value
            }
        },
        {
            'name': 'barcode (brcdNo)',
            'params': {
                'accessKey': FOODQR_ACCESS_KEY,
                'numOfRows': 10,
                'pageNo': 1,
                '_type': 'json',
                'brcdNo': search_value
            }
        }
    ]
    
    for search_info in search_params_list:
        try:
            search_name = search_info['name']
            params = search_info['params']
            
            print(f"[FoodQR] Searching with {search_name}: {search_value}")
            
            response = requests.get(FOOD_QR_API_URL, params=params, timeout=15)
            
            print(f"[FoodQR] Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[FoodQR] Failed with {response.status_code}")
                continue
            
            result = response.json()
            
            if result.get('response'):
                response_obj = result['response']
                
                if response_obj.get('body'):
                    body = response_obj['body']
                    
                    if body.get('items'):
                        items = body['items']
                        
                        if isinstance(items, dict):
                            if items.get('item'):
                                product = items['item']
                                
                                print(f"[FoodQR] ✓ Found using {search_name}")
                                
                                return {
                                    'source': 'FoodQR',
                                    'searchMethod': search_name,
                                    'product': product
                                }
                        
                        elif isinstance(items, list) and len(items) > 0:
                            product = items[0]
                            
                            if isinstance(product, dict) and product.get('item'):
                                product = product['item']
                            
                            print(f"[FoodQR] ✓ Found using {search_name}")
                            
                            return {
                                'source': 'FoodQR',
                                'searchMethod': search_name,
                                'product': product
                            }
            
            print(f"[FoodQR] No items found with {search_name}")
            
        except Exception as e:
            print(f"[FoodQR] Error with {search_name}: {str(e)}")
            continue
    
    print(f"[FoodQR] ✗ All search methods failed")
    return None


def extract_product_info_foodqr(product):
    """Food QR API 응답에서 제품 정보 추출"""
    
    product_name = product.get('prdctNm', 'Unknown Product')
    
    raw_html = product.get('prvwCn', '')
    
    raw_materials = strip_html(raw_html) if raw_html else ''
    
    print(f"[FoodQR Extract] Product Name: {product_name}")
    print(f"[FoodQR Extract] Raw Materials length: {len(raw_materials) if raw_materials else 0}")
    
    return product_name, raw_materials


@app.route('/test', methods=['GET'])
def test():
    """API 연결 테스트"""
    return jsonify({
        'status': 'ok',
        'SERVICE_KEY_set': SERVICE_KEY is not None,
        'FOODQR_ACCESS_KEY_set': FOODQR_ACCESS_KEY is not None,
        'FOOD_SAFETY_API_KEY_set': FOOD_SAFETY_API_KEY is not None,
        'SUPABASE_set': SUPABASE_URL is not None and SUPABASE_KEY is not None
    })


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_product():
    data = request.get_json()
    search_value = data.get('searchValue', '').strip()
    
    print(f"\n{'='*60}")
    print(f"Search request: {search_value}")
    print(f"{'='*60}")
    
    if not search_value:
        return jsonify({'error': 'Please enter a product number or barcode'}), 400
    
    try:
        # 1차: Supabase 검색 (가장 빠름!)
        print("[Search] Step 1: Searching Supabase...")
        supabase_result = search_custom_database(search_value)
        
        if supabase_result:
            product = supabase_result['product']
            product_name = product.get('prdctNm', 'Unknown')
            raw_materials = product.get('prvwCn', '')
            
            if raw_materials:
                found_ingredients = find_ingredients(raw_materials)
                return jsonify({
                    'productName': product_name,
                    'source': supabase_result['source'],
                    'rawMaterials': raw_materials,
                    'foundIngredients': found_ingredients
                })
        
        # 2차: HACCP API 검색
        print("[Search] Step 2: Searching HACCP API...")
        haccp_result = search_haccp_api(search_value)
        
        if haccp_result:
            product = haccp_result['product']
            product_name = product.get('prdlstNm', 'Unknown Product')
            raw_materials = product.get('rawmtrl', '')
            
            if not raw_materials:
                return jsonify({
                    'productName': product_name,
                    'source': 'HACCP',
                    'foundIngredients': {},
                    'rawMaterials': 'No ingredient information available.',
                })
            
            found_ingredients = find_ingredients(raw_materials)
            return jsonify({
                'productName': product_name,
                'source': 'HACCP',
                'rawMaterials': raw_materials,
                'foundIngredients': found_ingredients
            })
        
        # 3차: Food QR API 검색
        print("[Search] Step 3: Searching Food QR API...")
        foodqr_result = search_foodqr_api(search_value)
        
        if foodqr_result:
            product = foodqr_result['product']
            search_method = foodqr_result.get('searchMethod', 'unknown')
            product_name, raw_materials = extract_product_info_foodqr(product)
            
            if not raw_materials:
                return jsonify({
                    'productName': product_name,
                    'source': f'Food QR (e-Label) - {search_method}',
                    'foundIngredients': {},
                    'rawMaterials': 'No ingredient information available.',
                })
            
            found_ingredients = find_ingredients(raw_materials)
            return jsonify({
                'productName': product_name,
                'source': f'Food QR (e-Label) - {search_method}',
                'rawMaterials': raw_materials,
                'foundIngredients': found_ingredients
            })
        
        # ★ 4차: 88로 시작하는 바코드인 경우 C005 API로 품목번호 찾기 ★
        if search_value.startswith('88'):
            print("[Search] Step 4: Barcode detected (88 prefix) - trying C005 API...")
            
            barcode_mapping = search_barcode_link_api(search_value)
            
            if barcode_mapping:
                product_report_no = barcode_mapping['product_report_no']
                print(f"[Search] Step 5: Retrying with product report number: {product_report_no}")
                
                # 5차: 찾은 품목보고번호로 HACCP 재검색
                print("[Search] Step 5-1: Retrying HACCP with mapped product number...")
                haccp_retry = search_haccp_api(product_report_no)
                
                if haccp_retry:
                    product = haccp_retry['product']
                    product_name = product.get('prdlstNm', barcode_mapping['product_name'])
                    raw_materials = product.get('rawmtrl', '')
                    
                    if raw_materials:
                        found_ingredients = find_ingredients(raw_materials)
                        return jsonify({
                            'productName': product_name,
                            'source': 'HACCP (via C005 Barcode Mapping)',
                            'rawMaterials': raw_materials,
                            'foundIngredients': found_ingredients,
                            'mappingInfo': f"Barcode {search_value} → Product No. {product_report_no}"
                        })
                
                # 6차: FoodQR 재검색
                print("[Search] Step 5-2: Retrying FoodQR with mapped product number...")
                foodqr_retry = search_foodqr_api(product_report_no)
                
                if foodqr_retry:
                    product = foodqr_retry['product']
                    product_name, raw_materials = extract_product_info_foodqr(product)
                    
                    if raw_materials:
                        found_ingredients = find_ingredients(raw_materials)
                        return jsonify({
                            'productName': product_name,
                            'source': 'FoodQR (via C005 Barcode Mapping)',
                            'rawMaterials': raw_materials,
                            'foundIngredients': found_ingredients,
                            'mappingInfo': f"Barcode {search_value} → Product No. {product_report_no}"
                        })
                
                # C005에서 제품명은 찾았지만 원재료 정보가 없는 경우
                return jsonify({
                    'productName': barcode_mapping['product_name'],
                    'source': 'C005 Barcode Link API (Basic Info Only)',
                    'foundIngredients': {},
                    'rawMaterials': 'Product found via barcode, but detailed ingredient information is not available.',
                    'manufacturer': barcode_mapping['manufacturer'],
                    'productType': barcode_mapping['product_type']
                })
        
        print("[Search] All sources returned no results")
        return jsonify({'error': 'Product not found in any database.'}), 404
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'API request timeout. Please try again.'}), 504
    except Exception as e:
        print(f"[Search Error] {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error'}), 500


@app.route('/add-product', methods=['POST'])
def add_product():
    """Supabase에 제품 추가"""
    data = request.get_json()
    
    try:
        product_name = data.get('productName', '').strip()
        barcode = data.get('barcode', '').strip()
        imrpt_no = data.get('imrptNo', '').strip()
        raw_materials = data.get('rawMaterials', '').strip()
        
        if not product_name or not raw_materials:
            return jsonify({'error': 'Product name and raw materials required'}), 400
        
        if not barcode and not imrpt_no:
            return jsonify({'error': 'Barcode or imrptNo required'}), 400
        
        response = supabase.table('custom_products').insert({
            'barcode': barcode if barcode else None,
            'imrpt_no': imrpt_no if imrpt_no else None,
            'product_name': product_name,
            'raw_materials': raw_materials
        }).execute()
        
        print(f"[Supabase] Product added: {product_name}")
        
        return jsonify({
            'status': 'success',
            'message': f'✓ "{product_name}" added successfully!'
        }), 201
        
    except Exception as e:
        print(f"[Supabase Error] {str(e)}")
        return jsonify({'error': f'Failed to add product: {str(e)}'}), 500


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/request-product', methods=['POST'])
def request_product():
    """사용자가 요청한 제품 저장"""
    data = request.get_json()
    
    try:
        product_name = data.get('productName', '').strip()
        product_code = data.get('productCode', '').strip()
        barcode = data.get('barcode', '').strip()
        
        if not product_name:
            return jsonify({'error': '상품명은 필수입니다.'}), 400
        
        # Supabase에 저장
        response = supabase.table('product_requests').insert({
            'product_name': product_name,
            'product_code': product_code if product_code else None,
            'barcode': barcode if barcode else None
        }).execute()
        
        return jsonify({
            'status': 'success',
            'message': '상품 요청이 접수되었습니다. 감사합니다!'
        }), 201
        
    except Exception as e:
        print(f"[Product Request Error] {str(e)}")
        return jsonify({'error': 'Failed to save request'}), 500


@app.route('/product-requests', methods=['GET'])
def product_requests_page():
    """게시판 페이지"""
    return render_template('product_requests.html')

@app.route('/api/product-requests', methods=['GET'])
def get_product_requests():
    """요청 목록 조회"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        response = supabase.table('product_requests')\
            .select('*')\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=port)
