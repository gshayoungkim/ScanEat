'use client';

import { useState } from 'react';

export default function About() {
  const [language, setLanguage] = useState<'en' | 'ko'>('en');

  const content = {
    en: {
      title: 'About Us',
      ourStory: {
        heading: 'Our Story',
        text: 'This project was born from observing international friends repeatedly struggle with the same inconvenience: flipping over food packaging at convenience stores and supermarkets to check ingredient labels. Whether due to religious beliefs, food allergies, or lifestyle choices, they needed a faster, easier way to identify safe foods while visiting Korea.'
      },
      whatWeDo: {
        heading: 'What We Do',
        intro: 'We provide an easy-to-use ingredient detection service for international tourists and residents in Korea. Simply enter a product\'s report number or barcode, and our service instantly analyzes the ingredients to identify potential allergens or forbidden ingredients.',
        items: [
          'Quick Lookup - Enter product number or barcode from packaging',
          'Instant Analysis - Automatically scan complex ingredient lists',
          'Smart Detection - Identify beef, pork, milk, peanuts, eggs, fish, shellfish, and more',
          'Bilingual Support - Results in both Korean and English for easy understanding'
        ]
      },
      whyItMatters: {
        heading: 'Why It Matters',
        intro: 'International visitors to Korea have diverse dietary requirements for various reasons:',
        items: [
          'Religious Observance - Muslims (no pork), Hindus (no beef), Jews, and others with faith-based dietary laws',
          'Food Allergies - Severe reactions to milk, peanuts, eggs, fish, shellfish, and other common allergens',
          'Lifestyle Choices - Vegans (no animal products), vegetarians, and those with ethical dietary preferences'
        ],
        closing: 'Our goal is to ensure that every visitor can enjoy Korean food with confidence and peace of mind.'
      },
      howItWorks: {
        heading: 'How It Works',
        items: [
          'Find a product at a Korean grocery store or convenience store',
          'Enter the product report number or barcode shown on the packaging',
          'Our service automatically retrieves and analyzes the ingredient list',
          'Instantly see which allergens or forbidden ingredients are present',
          'Make an informed decision with confidence'
        ]
      },
      ourMission: {
        heading: 'Our Mission',
        text: 'To empower international visitors to Korea with the information they need to make safe, confident food choices—removing barriers and making Korean food experiences more enjoyable and stress-free for everyone.'
      },
      whoWeServe: {
        heading: 'Who We Serve',
        items: [
          '🌏 International Tourists - visiting Korea for the first time',
          '🛂 Foreign Residents - living and working in Korea',
          '🌙 Religious Visitors - with faith-based dietary restrictions',
          '⚠️ People with Allergies - requiring immediate ingredient information',
          '🌱 Vegan & Vegetarian Travelers - seeking plant-based options'
        ]
      },
      faq: {
        heading: 'Frequently Asked Questions',
        items: [
          {
            q: 'Q: Is the information accurate?',
            a: 'A: Our data is based on the official Korea Food and Drug Administration (KFDA) database, ensuring reliability. However, manufacturers may change ingredients, so we recommend checking recent updates when available.'
          },
          {
            q: 'Q: Does every Korean product show up in your database?',
            a: 'A: We cover registered processed foods in the KFDA database, with continuous expansion. Most commonly purchased items are included.'
          },
          {
            q: 'Q: Can I use this service on my phone?',
            a: 'A: Yes! Our service is fully mobile-optimized. You can easily look up products while shopping.'
          },
          {
            q: 'Q: Is it free to use?',
            a: 'A: Yes, our ingredient detector is completely free for everyone.'
          }
        ]
      },
      getStarted: {
        heading: 'Get Started',
        text: 'Ready to make your Korean food experience safer and more enjoyable? Head to our Ingredient Detector tool and start searching. Whether you\'re shopping at a convenience store or visiting a local market, we\'re here to help.',
        buttonText: 'Try the Detector Now'
      }
    },
    ko: {
      title: '저희 소개',
      ourStory: {
        heading: '우리의 시작',
        text: '매번 편의점이나 마트에서 포장지를 뒤집어 원재료명을 확인해야 했던 외국인 친구들의 불편함에서 이 프로젝트가 시작되었습니다. 특히 종교적 이유나 알러지, 비건 라이프스타일 때문에 특정 식재료를 피해야 하는 분들이 한국에 방문했을 때 매번 같은 수고를 반복하는 모습을 보았습니다.'
      },
      whatWeDo: {
        heading: '우리의 서비스',
        intro: '한국을 방문한 외국인 관광객과 거주자를 위한 원재료 검출 서비스를 제공합니다. 상품의 품목보고번호 또는 바코드를 입력하면, 우리의 서비스가 자동으로 원재료를 분석하여 잠재적인 알러지 유발물질이나 금기 성분을 찾아냅니다.',
        items: [
          '빠른 조회 - 포장지에 있는 품목보고번호 또는 바코드 입력',
          '즉시 분석 - 복잡한 원재료명을 자동으로 스캔',
          '스마트 감지 - 소고기, 돼지고기, 우유, 땅콩, 계란, 생선, 갑각류 등 감지',
          '이중언어 지원 - 한국어와 영어로 결과 제공'
        ]
      },
      whyItMatters: {
        heading: '중요성',
        intro: '한국을 방문하는 외국인들은 다양한 이유로 특정 식재료를 피해야 합니다:',
        items: [
          '종교적 신앙 - 무슬림(돼지고기 금지), 힌두교도(소고기 금지), 유대교도 등',
          '음식 알러지 - 우유, 땅콩, 계란, 생선, 갑각류 등으로 인한 심각한 반응',
          '라이프스타일 - 비건(모든 동물성 식품 제외), 채식주의자 등'
        ],
        closing: '우리의 목표는 모든 방문객이 한국 음식을 안심하고 즐길 수 있도록 돕는 것입니다.'
      },
      howItWorks: {
        heading: '사용 방법',
        items: [
          '한국 편의점이나 마트에서 상품 찾기',
          '포장지에 표시된 품목보고번호 또는 바코드 입력',
          '우리 서비스가 자동으로 원재료명을 검색하고 분석',
          '알러지 유발물질이나 금기 성분 확인',
          '안심하고 구매 결정'
        ]
      },
      ourMission: {
        heading: '우리의 목표',
        text: '한국을 방문한 외국인들이 안전하고 자신감 있게 음식을 선택할 수 있도록 필요한 정보를 제공하여, 장벽을 제거하고 모두가 즐거운 한국 음식 경험을 할 수 있도록 돕는 것입니다.'
      },
      whoWeServe: {
        heading: '우리의 고객',
        items: [
          '🌏 국제 관광객 - 처음 한국을 방문하는 분들',
          '🛂 외국인 거주자 - 한국에서 생활하고 일하는 분들',
          '🌙 종교 신자 - 종교적 식이 제한이 있는 분들',
          '⚠️ 알러지 있는 분들 - 긴급한 원재료 정보가 필요한 분들',
          '🌱 비건 및 채식주의 여행객 - 식물성 식품을 찾는 분들'
        ]
      },
      faq: {
        heading: '자주 묻는 질문',
        items: [
          {
            q: 'Q: 정보의 정확성은 보장되나요?',
            a: 'A: 우리의 데이터는 공식 식품의약품안전처(KFDA) 데이터베이스를 기반으로 제공되므로 신뢰할 수 있습니다. 다만 제조사에서 원재료를 변경할 수 있으므로, 최신 정보 확인을 권장합니다.'
          },
          {
            q: 'Q: 모든 한국 식품이 검색되나요?',
            a: 'A: 우리는 식품의약품안전처에 등록된 가공식품을 다루고 있으며, 지속적으로 확대 중입니다. 대부분의 일반적으로 구매하는 제품이 포함되어 있습니다.'
          },
          {
            q: 'Q: 휴대폰에서도 사용할 수 있나요?',
            a: 'A: 네! 우리의 서비스는 모바일에 최적화되어 있습니다. 쇼핑 중에도 쉽게 상품을 검색할 수 있습니다.'
          },
          {
            q: 'Q: 정말 무료로 사용할 수 있나요?',
            a: 'A: 네, 원재료 검출 서비스는 누구나 완전히 무료로 사용할 수 있습니다.'
          }
        ]
      },
      getStarted: {
        heading: '시작하기',
        text: '한국 음식 경험을 더 안전하고 즐겁게 만들 준비가 되셨나요? 우리의 원재료 검출 도구로 이동하여 검색을 시작하세요. 편의점에서 쇼핑하든, 지역 시장을 방문하든 우리가 도와드립니다.',
        buttonText: '지금 검출기 사용해보기'
      }
    }
  };

  const current = content[language];

  return (
    <main style={{ maxWidth: 720, margin: '40px auto', padding: 16 }}>
      {/* 탭 버튼 */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 24, borderBottom: '2px solid #e0e0e0' }}>
        <button
          onClick={() => setLanguage('en')}
          style={{
            padding: '12px 24px',
            background: language === 'en' ? '#007cc7' : 'transparent',
            color: language === 'en' ? 'white' : '#333',
            border: 'none',
            cursor: 'pointer',
            fontSize: 16,
            fontWeight: language === 'en' ? 'bold' : 'normal',
            borderBottom: language === 'en' ? '3px solid #007cc7' : 'none'
          }}
        >
          English
        </button>
        <button
          onClick={() => setLanguage('ko')}
          style={{
            padding: '12px 24px',
            background: language === 'ko' ? '#007cc7' : 'transparent',
            color: language === 'ko' ? 'white' : '#333',
            border: 'none',
            cursor: 'pointer',
            fontSize: 16,
            fontWeight: language === 'ko' ? 'bold' : 'normal',
            borderBottom: language === 'ko' ? '3px solid #007cc7' : 'none'
          }}
        >
          한국어
        </button>
      </div>

      <h1>{current.title}</h1>
      
      {/* Our Story / 우리의 시작 */}
      <section style={{ marginTop: 24 }}>
        <h2>{current.ourStory.heading}</h2>
        <p style={{ lineHeight: 1.6, fontSize: 16 }}>
          {current.ourStory.text}
        </p>
      </section>

      {/* What We Do / 우리의 서비스 */}
      <section style={{ marginTop: 24 }}>
        <h2>{current.whatWeDo.heading}</h2>
        <p style={{ lineHeight: 1.6, fontSize: 16 }}>
          {current.whatWeDo.intro}
        </p>
        <ul style={{ paddingLeft: 20, lineHeight: 1.8 }}>
          {current.whatWeDo.items.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </section>

      {/* Why It Matters / 중요성 */}
      <section style={{ marginTop: 24 }}>
        <h2>{current.whyItMatters.heading}</h2>
        <p style={{ lineHeight: 1.6, fontSize: 16 }}>
          {current.whyItMatters.intro}
        </p>
        <ul style={{ paddingLeft: 20, lineHeight: 1.8 }}>
          {current.whyItMatters.items.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
        <p style={{ lineHeight: 1.6, fontSize: 16, marginTop: 12 }}>
          {current.whyItMatters.closing}
        </p>
      </section>

      {/* How It Works / 사용 방법 */}
      <section style={{ marginTop: 24 }}>
        <h2>{current.howItWorks.heading}</h2>
        <ol style={{ paddingLeft: 20, lineHeight: 1.8 }}>
          {current.howItWorks.items.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ol>
      </section>

      {/* Our Mission / 우리의 목표 */}
      <section style={{ marginTop: 24 }}>
        <h2>{current.ourMission.heading}</h2>
        <p style={{ lineHeight: 1.6, fontSize: 16 }}>
          {current.ourMission.text}
        </p>
      </section>

      {/* Who We Serve / 우리의 고객 */}
      <section style={{ marginTop: 24 }}>
        <h2>{current.whoWeServe.heading}</h2>
        <ul style={{ paddingLeft: 20, lineHeight: 1.8 }}>
          {current.whoWeServe.items.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </section>

      {/* FAQ / 자주 묻는 질문 */}
      <section style={{ marginTop: 24, padding: 16, background: '#f0f0f0', borderRadius: 8 }}>
        <h2>{current.faq.heading}</h2>
        {current.faq.items.map((faqItem, idx) => (
          <div key={idx} style={{ marginTop: 12 }}>
            <p><strong>{faqItem.q}</strong></p>
            <p style={{ color: '#555' }}>{faqItem.a}</p>
          </div>
        ))}
      </section>

      {/* Get Started / 시작하기 */}
      <section style={{ marginTop: 24, padding: 16, background: '#e8f4f8', borderRadius: 8 }}>
        <h2>{current.getStarted.heading}</h2>
        <p style={{ lineHeight: 1.6, fontSize: 16 }}>
          {current.getStarted.text}
        </p>
        <div style={{ marginTop: 12 }}>
          <a href="/ingredient-detector" style={{ 
            display: 'inline-block',
            padding: '10px 20px',
            background: '#007cc7',
            color: 'white',
            textDecoration: 'none',
            borderRadius: 4,
            fontWeight: 'bold'
          }}>
            {current.getStarted.buttonText}
          </a>
        </div>
      </section>
    </main>
  );
}
