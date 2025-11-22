import streamlit as st
import random
import textwrap
import pandas as pd

st.set_page_config(
    page_title="Bopomofo Tutor",
    page_icon="🔡",
    layout="wide",
)

# ================================
#  注音資料（先放一批代表性符號，之後可以自己加）
# ================================

BOPOMOFO_DATA = [
    # 聲母（Initials）
    {
        "symbol": "ㄅ",
        "category": "聲母",
        "ipa": "p",
        "jp_roma_hint": "pa（無送気に近い）",
        "description_zh": "雙唇閉合的清不送氣破裂音，類似日文「pa」，但閉合更扎實。",
        "description_jp": "両唇を閉じて破裂させる無気音で、日本語の「pa」に近いが、ややしっかり閉じます。",
        "examples": [
            {"hanzi": "爸", "bopomofo": "ㄅㄚˋ", "pinyin": "bà"},
            {"hanzi": "杯", "bopomofo": "ㄅㄟ", "pinyin": "bēi"},
        ],
    },
    {
        "symbol": "ㄆ",
        "category": "聲母",
        "ipa": "pʰ",
        "jp_roma_hint": "pa（強い息を出す）",
        "description_zh": "雙唇閉合的清送氣破裂音，氣流明顯，像「pa！」強烈噴氣。",
        "description_jp": "両唇を閉じて破裂させる帯気音で、「pa！」と強く息を出すイメージです。",
        "examples": [
            {"hanzi": "怕", "bopomofo": "ㄆㄚˋ", "pinyin": "pà"},
            {"hanzi": "跑", "bopomofo": "ㄆㄠˇ", "pinyin": "pǎo"},
        ],
    },
    {
        "symbol": "ㄇ",
        "category": "聲母",
        "ipa": "m",
        "jp_roma_hint": "ma",
        "description_zh": "雙唇鼻音，和日文「ma」幾乎相同。",
        "description_jp": "両唇で作る鼻音で、日本語の「ma」とほぼ同じです。",
        "examples": [
            {"hanzi": "媽", "bopomofo": "ㄇㄚ", "pinyin": "mā"},
            {"hanzi": "米", "bopomofo": "ㄇㄧˇ", "pinyin": "mǐ"},
        ],
    },
    {
        "symbol": "ㄈ",
        "category": "聲母",
        "ipa": "f",
        "jp_roma_hint": "fu / fa",
        "description_zh": "上齒輕觸下唇的摩擦音，類似日文外來語的 f 音。",
        "description_jp": "上の歯を下唇に軽く当てて出す摩擦音で、外来語の f に近いです。",
        "examples": [
            {"hanzi": "發", "bopomofo": "ㄈㄚ", "pinyin": "fā"},
        ],
    },
    {
        "symbol": "ㄉ",
        "category": "聲母",
        "ipa": "t",
        "jp_roma_hint": "ta（無送気）",
        "description_zh": "舌尖抵上齒背的清不送氣破裂音，類似日文「ta」但位置略後。",
        "description_jp": "舌先を上の歯の裏に当てる無気音で、日本語の「ta」に近いが少し奥です。",
        "examples": [
            {"hanzi": "大", "bopomofo": "ㄉㄚˋ", "pinyin": "dà"},
        ],
    },
    {
        "symbol": "ㄊ",
        "category": "聲母",
        "ipa": "tʰ",
        "jp_roma_hint": "ta（強い息）",
        "description_zh": "清送氣破裂音，發音時有明顯氣流。",
        "description_jp": "帯気音の「ta」で、はっきりと息が出ます。",
        "examples": [
            {"hanzi": "他", "bopomofo": "ㄊㄚ", "pinyin": "tā"},
        ],
    },
    {
        "symbol": "ㄋ",
        "category": "聲母",
        "ipa": "n",
        "jp_roma_hint": "na",
        "description_zh": "舌尖鼻音，和日文「na」類似。",
        "description_jp": "舌先で作る鼻音で、日本語の「na」とほぼ同じです。",
        "examples": [
            {"hanzi": "你", "bopomofo": "ㄋㄧˇ", "pinyin": "nǐ"},
        ],
    },
    {
        "symbol": "ㄌ",
        "category": "聲母",
        "ipa": "l",
        "jp_roma_hint": "ra / la",
        "description_zh": "舌尖邊音，介於日文 r 與 l 之間。",
        "description_jp": "舌先を上につけて横から息を出す音で、日本語の r と l の中間のような感じです。",
        "examples": [
            {"hanzi": "來", "bopomofo": "ㄌㄞˊ", "pinyin": "lái"},
        ],
    },
    {
        "symbol": "ㄍ",
        "category": "聲母",
        "ipa": "k",
        "jp_roma_hint": "ka（無送気）",
        "description_zh": "舌根接近軟顎的清不送氣破裂音，類似日文「ka」。",
        "description_jp": "舌の後ろを上あごに当てる無気音で、日本語の「ka」に近いです。",
        "examples": [
            {"hanzi": "高", "bopomofo": "ㄍㄠ", "pinyin": "gāo"},
        ],
    },
    {
        "symbol": "ㄎ",
        "category": "聲母",
        "ipa": "kʰ",
        "jp_roma_hint": "ka（強い息）",
        "description_zh": "清送氣破裂音，比「ㄍ」多強烈氣流。",
        "description_jp": "同じく k ですが、はっきりと息を出す帯気音です。",
        "examples": [
            {"hanzi": "考", "bopomofo": "ㄎㄠˇ", "pinyin": "kǎo"},
        ],
    },
    {
        "symbol": "ㄏ",
        "category": "聲母",
        "ipa": "x",
        "jp_roma_hint": "h（強め）",
        "description_zh": "清軟顎擦音，比日文 h 更靠後、氣流更強。",
        "description_jp": "日本語の h よりやや奥で、息を強く出す摩擦音です。",
        "examples": [
            {"hanzi": "好", "bopomofo": "ㄏㄠˇ", "pinyin": "hǎo"},
        ],
    },
    {
        "symbol": "ㄐ",
        "category": "聲母",
        "ipa": "tɕ",
        "jp_roma_hint": "ji",
        "description_zh": "舌面前部接近硬顎，類似日文「ジ」但較扁。",
        "description_jp": "舌の前の方を上あごに近づける音で、日本語の「ji」に近いです。",
        "examples": [
            {"hanzi": "家", "bopomofo": "ㄐㄧㄚ", "pinyin": "jiā"},
        ],
    },
    {
        "symbol": "ㄑ",
        "category": "聲母",
        "ipa": "tɕʰ",
        "jp_roma_hint": "chi（強い息）",
        "description_zh": "與「ㄐ」位置相同，但送氣較強。",
        "description_jp": "「ji」と同じ位置で、より強く息を出す帯気音で、日本語の「chi」に近いです。",
        "examples": [
            {"hanzi": "七", "bopomofo": "ㄑㄧ", "pinyin": "qī"},
        ],
    },
    {
        "symbol": "ㄒ",
        "category": "聲母",
        "ipa": "ɕ",
        "jp_roma_hint": "shi",
        "description_zh": "舌面前部摩擦音，類似日文「シ」但舌位更扁更前。",
        "description_jp": "日本語の「shi」に近いが、舌をもう少し前にして平たくします。",
        "examples": [
            {"hanzi": "西", "bopomofo": "ㄒㄧ", "pinyin": "xī"},
        ],
    },
    {
        "symbol": "ㄓ",
        "category": "聲母",
        "ipa": "ʈʂ",
        "jp_roma_hint": "ji（舌を奥・軽く巻き舌）",
        "description_zh": "舌尖略向後捲起的塞擦音，日文中沒有完全對應的音。",
        "description_jp": "舌先をやや奥に入れて軽く巻き舌にする音で、日本語に完全な対応はありません。",
        "examples": [
            {"hanzi": "知", "bopomofo": "ㄓ", "pinyin": "zhī"},
        ],
    },
    {
        "symbol": "ㄔ",
        "category": "聲母",
        "ipa": "ʈʂʰ",
        "jp_roma_hint": "chi（舌を奥・強い息）",
        "description_zh": "捲舌送氣塞擦音，像很靠後的「chi」。",
        "description_jp": "舌先を奥にして巻き舌にし、強く息を出す音で、後ろ側の「chi」のイメージです。",
        "examples": [
            {"hanzi": "吃", "bopomofo": "ㄔ", "pinyin": "chī"},
        ],
    },
    {
        "symbol": "ㄕ",
        "category": "聲母",
        "ipa": "ʂ",
        "jp_roma_hint": "shi（舌を奥）",
        "description_zh": "捲舌摩擦音，舌位比「ㄒ」更後。",
        "description_jp": "舌先を少し奥にして出す「shi」に近い摩擦音です。",
        "examples": [
            {"hanzi": "師", "bopomofo": "ㄕ", "pinyin": "shī"},
        ],
    },
    {
        "symbol": "ㄖ",
        "category": "聲母",
        "ipa": "ʐ",
        "jp_roma_hint": "ri（濁った音）",
        "description_zh": "捲舌濁音，介於 r 與 z 之間。",
        "description_jp": "有声の巻き舌音で、日本語の「ri」より濁った感じです。",
        "examples": [
            {"hanzi": "日", "bopomofo": "ㄖˋ", "pinyin": "rì"},
        ],
    },
    {
        "symbol": "ㄗ",
        "category": "聲母",
        "ipa": "ts",
        "jp_roma_hint": "tsu 系",
        "description_zh": "舌尖塞擦音，類似日文「tsu」開頭。",
        "description_jp": "日本語の「tsu」の最初の部分に近い音です。",
        "examples": [
            {"hanzi": "資", "bopomofo": "ㄗ", "pinyin": "zī"},
        ],
    },
    {
        "symbol": "ㄘ",
        "category": "聲母",
        "ipa": "tsʰ",
        "jp_roma_hint": "tsu（強い息）",
        "description_zh": "送氣塞擦音，比「ㄗ」有明顯氣流。",
        "description_jp": "「tsu」と同じく ts 系ですが、強く息を出します。",
        "examples": [
            {"hanzi": "次", "bopomofo": "ㄘˋ", "pinyin": "cì"},
        ],
    },
    {
        "symbol": "ㄙ",
        "category": "聲母",
        "ipa": "s",
        "jp_roma_hint": "su",
        "description_zh": "舌尖接近上齒背的摩擦音，類似日文「su」。",
        "description_jp": "舌先を上の歯の近くに置いて出す摩擦音で、日本語の「su」に近いです。",
        "examples": [
            {"hanzi": "思", "bopomofo": "ㄙ", "pinyin": "sī"},
        ],
    },

    # 介音（Medials）
    {
        "symbol": "ㄧ",
        "category": "介音",
        "ipa": "i̯",
        "jp_roma_hint": "i / yi",
        "description_zh": "半元音，接近母音 i 的滑音，用於複合韻。",
        "description_jp": "母音 i に近い半母音で、複合韻の一部として使われます。",
        "examples": [
            {"hanzi": "一", "bopomofo": "ㄧ", "pinyin": "yī"},
        ],
    },
    {
        "symbol": "ㄨ",
        "category": "介音",
        "ipa": "u̯",
        "jp_roma_hint": "u / wu",
        "description_zh": "半元音，接近母音 u。",
        "description_jp": "母音 u に近い半母音です。",
        "examples": [
            {"hanzi": "屋", "bopomofo": "ㄨ", "pinyin": "wū"},
        ],
    },
    {
        "symbol": "ㄩ",
        "category": "介音",
        "ipa": "y̯",
        "jp_roma_hint": "yu（日本語にない ü）",
        "description_zh": "圓唇前高元音的滑音，日文沒有 ü 音。",
        "description_jp": "丸めた唇で前方で発音する ü 系の音で、日本語にはありません。",
        "examples": [
            {"hanzi": "魚", "bopomofo": "ㄩˊ", "pinyin": "yú"},
        ],
    },

    # 韻母（Finals：單韻母＋鼻音韻）
    {
        "symbol": "ㄚ",
        "category": "韻母",
        "ipa": "a",
        "jp_roma_hint": "a",
        "description_zh": "開口度大的 a 音。",
        "description_jp": "口を大きく開ける a の音です。",
        "examples": [
            {"hanzi": "八", "bopomofo": "ㄅㄚ", "pinyin": "bā"},
        ],
    },
    {
        "symbol": "ㄛ",
        "category": "韻母",
        "ipa": "o",
        "jp_roma_hint": "o",
        "description_zh": "類似日文 o，但唇形略不同。",
        "description_jp": "日本語の o に近いですが、やや唇の丸め方が異なります。",
        "examples": [
            {"hanzi": "我", "bopomofo": "ㄨㄛˇ", "pinyin": "wǒ"},
        ],
    },
    {
        "symbol": "ㄜ",
        "category": "韻母",
        "ipa": "ɤ",
        "jp_roma_hint": "（日本語にない）",
        "description_zh": "介於 e 與 o 之間的央元音，日文沒有對應。",
        "description_jp": "e と o の中間のような中央母音で、日本語にはありません。",
        "examples": [
            {"hanzi": "餓", "bopomofo": "ㄜˋ", "pinyin": "è"},
        ],
    },
    {
        "symbol": "ㄝ",
        "category": "韻母",
        "ipa": "e",
        "jp_roma_hint": "e",
        "description_zh": "前中元音，類似日文 e。",
        "description_jp": "日本語の e に近い前舌の母音です。",
        "examples": [
            {"hanzi": "爺", "bopomofo": "ㄧㄝˊ", "pinyin": "yé"},
        ],
    },
    {
        "symbol": "ㄞ",
        "category": "韻母",
        "ipa": "ai",
        "jp_roma_hint": "ai",
        "description_zh": "複合元音，a 滑向 i。",
        "description_jp": "a から i へ滑る二重母音です。",
        "examples": [
            {"hanzi": "來", "bopomofo": "ㄌㄞˊ", "pinyin": "lái"},
        ],
    },
    {
        "symbol": "ㄟ",
        "category": "韻母",
        "ipa": "ei",
        "jp_roma_hint": "ei",
        "description_zh": "複合元音，e 滑向 i。",
        "description_jp": "e から i に滑る二重母音で、日本語の「えい」に近いです。",
        "examples": [
            {"hanzi": "飛", "bopomofo": "ㄈㄟ", "pinyin": "fēi"},
        ],
    },
    {
        "symbol": "ㄠ",
        "category": "韻母",
        "ipa": "au",
        "jp_roma_hint": "ao",
        "description_zh": "a 滑向 u 的二重母音。",
        "description_jp": "a から u へ滑る二重母音です。",
        "examples": [
            {"hanzi": "高", "bopomofo": "ㄍㄠ", "pinyin": "gāo"},
        ],
    },
    {
        "symbol": "ㄡ",
        "category": "韻母",
        "ipa": "ou",
        "jp_roma_hint": "ou",
        "description_zh": "o 滑向 u 的二重母音。",
        "description_jp": "o から u へ滑る二重母音で、日本語の「おう」に近いです。",
        "examples": [
            {"hanzi": "狗", "bopomofo": "ㄍㄡˇ", "pinyin": "gǒu"},
        ],
    },
    {
        "symbol": "ㄢ",
        "category": "韻母",
        "ipa": "an",
        "jp_roma_hint": "an（鼻音強め）",
        "description_zh": "後鼻音 an，鼻音較重。",
        "description_jp": "語末の n をしっかり鼻で響かせる「an」です。",
        "examples": [
            {"hanzi": "安", "bopomofo": "ㄢ", "pinyin": "ān"},
        ],
    },
    {
        "symbol": "ㄣ",
        "category": "韻母",
        "ipa": "ən",
        "jp_roma_hint": "en",
        "description_zh": "央元音加鼻音 n。",
        "description_jp": "中央母音 + n の鼻音です。",
        "examples": [
            {"hanzi": "本", "bopomofo": "ㄅㄣˇ", "pinyin": "běn"},
        ],
    },
    {
        "symbol": "ㄤ",
        "category": "韻母",
        "ipa": "ɑŋ",
        "jp_roma_hint": "（ng 尾・日本語にない）",
        "description_zh": "後鼻音 ang，尾音 ng，日文沒有。",
        "description_jp": "語末の ng を伴う鼻音で、日本語にはありません。",
        "examples": [
            {"hanzi": "商", "bopomofo": "ㄕㄤ", "pinyin": "shāng"},
        ],
    },
    {
        "symbol": "ㄥ",
        "category": "韻母",
        "ipa": "əŋ",
        "jp_roma_hint": "（ng 尾）",
        "description_zh": "央元音加 ng 尾鼻音。",
        "description_jp": "中央母音 + ng の鼻音です。",
        "examples": [
            {"hanzi": "風", "bopomofo": "ㄈㄥ", "pinyin": "fēng"},
        ],
    },
    {
        "symbol": "ㄦ",
        "category": "韻母",
        "ipa": "ɚ",
        "jp_roma_hint": "（r 母音・日本語にない）",
        "description_zh": "兒化音的核心元音，帶 r 色彩的央元音。",
        "description_jp": "r 色のついた中央母音で、日本語には存在しない音です。",
        "examples": [
            {"hanzi": "耳", "bopomofo": "ㄦˇ", "pinyin": "ěr"},
        ],
    },
]

SYMBOL_LIST = [d["symbol"] for d in BOPOMOFO_DATA]


def get_symbol_data(symbol: str):
    for item in BOPOMOFO_DATA:
        if item["symbol"] == symbol:
            return item
    return None


# ================================
#  頁面結構
# ================================

st.sidebar.title("Bopomofo Tutor 🔡")

page = st.sidebar.radio(
    "選擇頁面 / ページを選択：",
    (
        "📖 認識這個 AI 服務",
        "🔤 注音學習卡片",
        "📋 注音符號總覽",
        "📝 小測驗（選擇題）",
    ),
)


# ========= 頁面 1：說明 AI Service ========= #

if page == "📖 認識這個 AI 服務":
    st.title("Bopomofo Tutor 注音學習 AI 服務 🔡")
    st.markdown(
        """
### ✍️ Bopomofo Tutor 是什麼？

這是一個讓台灣與日本學生都能輕鬆學習注音的互動式工具。  
提供 **注音卡片、符號總表、小測驗** 等功能，幫助學習者快速掌握注音的發音方式與符號差異。

---

### ✍️ Bopomofo Tutor とは？

台湾人と日本人の学習者が、注音（ボポモフォ）を楽しく学べるインタラクティブなツールです。  
**注音カード・記号一覧・クイズ** を通して、発音の特徴や日本語との違いをわかりやすく理解できます。
 

"""
    )

    # 🔔 使用者操作提示（中日雙語）
    st.info(
       
        """
---

### 🔍 使用提示 / ご案内

左側的選單可以切換不同功能頁面：  
- 注音學習卡片  
- 注音符號總覽  
- 小測驗：注音 × 日文羅馬字  

左のサイドバーから、学習ページを選んで進めることができます。
- ボポモフォ学習カード  
- ボポモフォ一覧  
- ミニクイズ：注音 × 日本語ローマ字
"""
    )
# ========= 頁面 2：注音學習卡片 ========= #

elif page == "🔤 注音學習卡片":
    st.title("🔤 注音學習卡片 / ボポモフォ学習カード")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        category_filter = st.selectbox(
            "選擇類別 / カテゴリを選択：",
            ["全部", "聲母", "介音", "韻母"],
        )

        if category_filter == "全部":
            candidate_symbols = SYMBOL_LIST
        else:
            candidate_symbols = [
                d["symbol"] for d in BOPOMOFO_DATA if d["category"] == category_filter
            ]

        selected_symbol = st.selectbox(
            "選擇注音符號 / 学びたい注音を選んでください：",
            candidate_symbols,
        )

        data = get_symbol_data(selected_symbol)

        st.markdown(
            f"""
### 注音符號：**{data['symbol']}**
- 類別 / カテゴリ：`{data['category']}`  
- IPA：`{data['ipa']}`  
- 日文羅馬字近似：`{data['jp_roma_hint']}`
"""
        )

    with col_right:
        st.subheader("發音說明 / 発音の説明")

        st.markdown("**中文說明（繁體）**")
        st.write(textwrap.fill(data["description_zh"], 40))

        st.markdown("**日本語での説明**")
        st.write(textwrap.fill(data["description_jp"], 40))

        st.markdown("---")
        st.subheader("例詞 / 例語")

        for ex in data.get("examples", []):
            st.markdown(
                f"- **{ex['hanzi']}**　`{ex['bopomofo']}`　*pinyin: {ex['pinyin']}*"
            )

        if not data.get("examples"):
            st.info("這個符號目前尚未設定例詞，可在資料表中補上。")


# ========= 頁面 3：注音符號總覽 ========= #

elif page == "📋 注音符號總覽":
    st.title("📋 注音符號總覽 / ボポモフォ一覧")

    st.markdown(
        """
這裡整理了注音符號的基本資訊（符號、類別、IPA、日文羅馬字提示）。  
可用於課堂展示或作為教材附錄。

ここでは、注音符号の基本情報（記号・カテゴリー・IPA・日本語ローマ字のヒント）をまとめています。
授業での提示や教材付録としてご利用いただけます。
"""
    )

    df = pd.DataFrame(
        [
            {
                "注音": d["symbol"],
                "類別": d["category"],
                "IPA": d["ipa"],
                "日文羅馬字提示": d["jp_roma_hint"],
            }
            for d in BOPOMOFO_DATA
        ]
    )

    # ⭐ index 從 0 改成 1 開始
    df.index = df.index + 1

    st.dataframe(df, use_container_width=True)



# ========= 頁面 4：小測驗（選擇題） ========= #

elif page == "📝 小測驗（選擇題）":

    st.title(
        """
📝 小測驗：注音 × 日文羅馬字 / ミニクイズ：注音 × 日本語ローマ字

"""
    )

    # ========= 建立 Quiz 狀態 ========= #
    def make_question():
        q = random.choice(BOPOMOFO_DATA)
        correct = q["jp_roma_hint"]

        distractors = [
            d["jp_roma_hint"] for d in BOPOMOFO_DATA if d["symbol"] != q["symbol"]
        ]
        random.shuffle(distractors)

        options = [correct] + distractors[:3]
        random.shuffle(options)

        return {
            "symbol": q["symbol"],
            "correct": correct,
            "options": options,
            "q_data": q,
            "submitted": False,
            "answer": None,
        }

    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = make_question()

    state = st.session_state.quiz_state

    # 題目（中日文合併）
    st.subheader(
        f"題目：這個注音符號是 **{state['symbol']}**。 / この注音符号は「{state['symbol']}」です。"
    )

    # 選擇題
    # 說明（分行）
    answer = st.radio( 
        "它的日文羅馬字近似是？ / その日本語ローマ字の近い音はどれですか？",
        state["options"], 
        key=f"quiz_radio_{state['symbol']}",
    )

    # 按鈕（送出＋下一題）
    col1, col2 = st.columns(2)
    with col1:
        submit = st.button("✅ 送出答案 / 答えを送信")
    with col2:
        next_q = st.button("➡ 下一題 / 次の問題へ")

    # 送出答案：更新 state，不換題
    if submit:
        state["submitted"] = True
        state["answer"] = answer

    # 換題
    if next_q:
        st.session_state.quiz_state = make_question()
        st.rerun()

    # 判定結果
    if state["submitted"]:
        if state["answer"] == state["correct"]:
            st.success("🎉 正確！/ 正解です！")
        else:
            st.error("❌ 再想想看 / もう一度考えてみてください")

        with st.expander("📘 詳細解說 / 詳しい説明"):
            q = state["q_data"]
            st.markdown(
                f"""
- 注音：**{q['symbol']}**
- 類別：{q['category']}
- IPA：`{q['ipa']}`
- 正確答案：`{q['jp_roma_hint']}`

**中文說明：**  
{q['description_zh']}

**日本語の説明：**  
{q['description_jp']}
"""
            )
