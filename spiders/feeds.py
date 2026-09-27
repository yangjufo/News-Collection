# -*- coding: utf-8 -*-
"""
Configuration of RSS / Atom and news feed sources for News-Collection.
Supports both Chinese and English sources mapped to website categories:
Technology, Sports, Money, Hot, Entertainment.
"""

CATEGORY_PLACEHOLDER_IMAGES = {
    'Technology': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop',
    'Sports': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&auto=format&fit=crop',
    'Money': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&auto=format&fit=crop',
    'Hot': 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600&auto=format&fit=crop',
    'Entertainment': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&auto=format&fit=crop',
}

FEED_SOURCES = {
    'Technology': [
        # English
        {
            'name': 'TechCrunch',
            'url': 'https://techcrunch.com/feed/',
            'lang': 'en',
            'category': 'Technology'
        },
        {
            'name': 'Ars Technica',
            'url': 'https://feeds.arstechnica.com/arstechnica/index',
            'lang': 'en',
            'category': 'Technology'
        },
        {
            'name': 'The Verge',
            'url': 'https://www.theverge.com/rss/index.xml',
            'lang': 'en',
            'category': 'Technology'
        },
        # Chinese
        {
            'name': '36氪',
            'url': 'https://36kr.com/feed',
            'lang': 'zh',
            'category': 'Technology'
        },
        {
            'name': '新浪科技',
            'url': 'http://rss.sina.com.cn/tech/roll.xml',
            'lang': 'zh',
            'category': 'Technology'
        },
    ],
    'Sports': [
        # English
        {
            'name': 'BBC Sport',
            'url': 'http://feeds.bbci.co.uk/sport/rss.xml',
            'lang': 'en',
            'category': 'Sports'
        },
        {
            'name': 'ESPN News',
            'url': 'https://www.espn.com/espn/rss/news',
            'lang': 'en',
            'category': 'Sports'
        },
        # Chinese
        {
            'name': '新浪体育',
            'url': 'http://rss.sina.com.cn/sports/global/index.xml',
            'lang': 'zh',
            'category': 'Sports'
        },
    ],
    'Money': [
        # English
        {
            'name': 'Yahoo Finance',
            'url': 'https://finance.yahoo.com/news/rssindex',
            'lang': 'en',
            'category': 'Money'
        },
        {
            'name': 'CNBC Finance',
            'url': 'https://search.cnbc.com/rs/search/view.html?partnerId=2000&keywords=finance&sort=date',
            'lang': 'en',
            'category': 'Money'
        },
        # Chinese
        {
            'name': '新浪财经',
            'url': 'http://rss.sina.com.cn/roll/finance/hot_roll.xml',
            'lang': 'zh',
            'category': 'Money'
        },
    ],
    'Hot': [
        # English
        {
            'name': 'BBC World',
            'url': 'http://feeds.bbci.co.uk/news/world/rss.xml',
            'lang': 'en',
            'category': 'Hot'
        },
        {
            'name': 'NPR World News',
            'url': 'https://feeds.npr.org/1004/rss.xml',
            'lang': 'en',
            'category': 'Hot'
        },
        # Chinese
        {
            'name': '新浪要闻',
            'url': 'http://rss.sina.com.cn/news/allnews/index.xml',
            'lang': 'zh',
            'category': 'Hot'
        },
    ],
    'Entertainment': [
        # English
        {
            'name': 'EW Entertainment',
            'url': 'https://ew.com/feed/',
            'lang': 'en',
            'category': 'Entertainment'
        },
        {
            'name': 'BBC Arts & Entertainment',
            'url': 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
            'lang': 'en',
            'category': 'Entertainment'
        },
        # Chinese
        {
            'name': '新浪娱乐',
            'url': 'http://rss.sina.com.cn/ent/hot_roll.xml',
            'lang': 'zh',
            'category': 'Entertainment'
        },
    ]
}


def get_mock_articles(category=None, count=10):
    """
    Returns realistic bilingual mock articles for offline development or testing.
    """
    from datetime import datetime, timedelta
    import random

    now = datetime.utcnow()

    samples = {
        'Technology': [
            (
                'Next-Generation Quantum Chips Enter Commercial Pilot Testing',
                'Researchers achieve quantum coherence at scalable temperatures, paving the way for next-decade computing.',
                'TechCrunch',
                'https://techcrunch.com/sample/quantum-chips-2026',
                'https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&auto=format&fit=crop'
            ),
            (
                '人工智能大模型在生物制药领域取得重大突破',
                '最新蛋白质结构预测模型助力新药研发周期缩短60%，多家跨国医药企业宣布深度合作。',
                '36氪',
                'https://36kr.com/p/sample-ai-bio-pharma-2026',
                'https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=600&auto=format&fit=crop'
            ),
            (
                'Open Source Autonomous Agent Frameworks See Rapid Enterprise Adoption',
                'Developers are building collaborative multi-agent ecosystems to handle end-to-end software operations.',
                'The Verge',
                'https://theverge.com/sample/autonomous-agents-rise',
                'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&auto=format&fit=crop'
            ),
            (
                'RISC-V 架构芯片在数据中心与边缘计算场景爆发式增长',
                '开放指令集生态加速完善，国内外主流芯片厂商加速推出高性能服务器芯片。',
                '新浪科技',
                'https://tech.sina.com.cn/sample/riscv-data-center',
                'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600&auto=format&fit=crop'
            ),
        ],
        'Sports': [
            (
                'Champions League Thriller: Extra-Time Header Seals Dramatic Victory',
                'A ninety-fourth minute corner kick delivered an unforgettable European night for football supporters.',
                'BBC Sport',
                'https://bbc.com/sport/sample/champions-league-thriller',
                'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=600&auto=format&fit=crop'
            ),
            (
                '世乒赛决赛巅峰对决，中国队包揽男女单打冠军',
                '激战七局展现顶级技术与心理博弈，现场观众共同见证历史时刻。',
                '新浪体育',
                'https://sports.sina.com.cn/sample/table-tennis-championship',
                'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&auto=format&fit=crop'
            ),
            (
                'Marathon World Record Shattered Under Perfect Racing Conditions',
                'Paced by cutting-edge aerodynamic drafting, the elite runner shaved 28 seconds off the world best.',
                'ESPN News',
                'https://espn.com/sample/marathon-record-broken',
                'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&auto=format&fit=crop'
            ),
        ],
        'Money': [
            (
                'Global Central Banks Signal Coordinated Shift in Interest Rate Policies',
                'Inflation cooling down towards target ranges encourages economic policymakers to evaluate strategic easing.',
                'Yahoo Finance',
                'https://finance.yahoo.com/sample/central-banks-rate-cut',
                'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&auto=format&fit=crop'
            ),
            (
                '新能源汽车出口持续攀升，供应链全球化布局提速',
                '海外交付量同比增长近45%，绿色产业投资与跨国建厂迎来新机遇。',
                '新浪财经',
                'https://finance.sina.com.cn/sample/ev-exports-growth',
                'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=600&auto=format&fit=crop'
            ),
            (
                'Tech Stocks Rally as Cloud and Enterprise Infrastructure Revenues Surge',
                'Quarterly earnings exceed Wall Street consensus with enterprise modernization driving capital expenditures.',
                'CNBC Finance',
                'https://cnbc.com/sample/cloud-infrastructure-rally',
                'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=600&auto=format&fit=crop'
            ),
        ],
        'Hot': [
            (
                'International Climate Summit Announces Landmark Clean Energy Pact',
                'Delegates from over 90 nations finalize treaty to accelerate renewable grid infrastructure and energy storage.',
                'BBC World',
                'https://bbc.com/news/sample/climate-summit-clean-energy',
                'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600&auto=format&fit=crop'
            ),
            (
                '全国高铁网络突破五万公里，多条跨区域大动脉正式开通',
                '便捷互联重塑一小时经济圈，为沿线城市高质量发展注入强劲新动力。',
                '新浪要闻',
                'https://news.sina.com.cn/sample/high-speed-railway-milestone',
                'https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=600&auto=format&fit=crop'
            ),
            (
                'Deep-Sea Submersible Explores Uncharted Mariana Trench Biosphere',
                'Marine oceanographers document previously unclassified organisms thriving under extreme hydrothermal pressures.',
                'NPR World News',
                'https://npr.org/sample/deep-sea-exploration',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=600&auto=format&fit=crop'
            ),
        ],
        'Entertainment': [
            (
                'Sci-Fi Epic Smashes Opening Weekend Global Box Office Records',
                'Combining breathtaking visual effects and philosophical storytelling, the director scores another cinematic masterwork.',
                'EW Entertainment',
                'https://ew.com/sample/scifi-epic-box-office',
                'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&auto=format&fit=crop'
            ),
            (
                '年度金曲音乐盛典盛大落幕，原创独立乐团斩获多项大奖',
                '多风格音乐融合展现蓬勃创造力，线上直播观看人次创新高。',
                '新浪娱乐',
                'https://ent.sina.com.cn/sample/golden-melody-awards',
                'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=600&auto=format&fit=crop'
            ),
            (
                'Acclaimed Indie Video Game Wins Coveted Game of the Year Honors',
                'Developed by a small studio, the hand-animated narrative adventure captured critics and players worldwide.',
                'BBC Arts',
                'https://bbc.com/sample/indie-game-of-the-year',
                'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600&auto=format&fit=crop'
            ),
        ]
    }

    target_categories = [category] if (
        category and category in samples) else list(samples.keys())
    results = []

    for cat in target_categories:
        cat_samples = samples[cat]
        for idx, (title, abstract, website, url, img) in enumerate(cat_samples[:count]):
            offset = random.randint(10, 720)
            item = {
                'title': title,
                'abstract': abstract,
                'content': abstract,
                'web_site': website,
                'url': f'{url}-{idx}',
                'image': img,
                'category': cat,
                'publish_time': now - timedelta(minutes=offset)
            }
            results.append(item)

    return results
