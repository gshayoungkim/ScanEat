import requests
import json

# 테스트 설정
API_KEY = "d8bf16a03fec4b4d8acf"
BARCODE = "8801019602498"

# C005 API 테스트
def test_c005_api():
    # 방법 1: 바코드로 검색
    url = f"http://openapi.foodsafetykorea.go.kr/api/{API_KEY}/C005/json/1/100/BAR_CD={BARCODE}"
    
    print(f"Request URL: {url}")
    print("="*80)
    
    try:
        response = requests.get(url, timeout=15)
        print(f"Status Code: {response.status_code}")
        print("="*80)
        
        if response.status_code == 200:
            result = response.json()
            print("Response JSON:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 결과 파싱
            if result.get('C005'):
                c005 = result['C005']
                
                # 결과 코드 확인
                if c005.get('RESULT'):
                    print("\n" + "="*80)
                    print(f"Result Code: {c005['RESULT'].get('CODE')}")
                    print(f"Result Message: {c005['RESULT'].get('MSG')}")
                
                # 데이터 확인
                rows = c005.get('row', [])
                total = c005.get('total_count', '0')
                
                print(f"Total Count: {total}")
                
                if rows:
                    print("\n" + "="*80)
                    print("Found Products:")
                    for idx, row in enumerate(rows, 1):
                        print(f"\n[Product {idx}]")
                        print(f"  제품명: {row.get('PRDLST_NM')}")
                        print(f"  품목보고번호: {row.get('PRDLST_REPORT_NO')}")
                        print(f"  제조사: {row.get('BSSH_NM')}")
                        print(f"  식품유형: {row.get('PRDLST_DCNM')}")
                        print(f"  바코드: {row.get('BAR_CD')}")
                else:
                    print("\n해당 바코드의 제품을 찾을 수 없습니다.")
                    print("(2018년 이후 제품은 데이터가 없을 수 있습니다)")
        else:
            print(f"Error Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_c005_api()
