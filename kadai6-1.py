import requests

# -------------------------------------------------------------
# 【e-Stat APIの基本設定】
# -------------------------------------------------------------

# e-Stat APIのアプリケーションID（あなたのIDを使用）
APP_ID = "78f5348aa40bf91923497c2028074eab89e60563"

# データ取得用のAPIエンドポイント
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

# -------------------------------------------------------------
# 【取得するデータの種類】
# - 家計調査（総世帯）用途分類（総数）
# - 用途別に支出金額などの統計が分類されたデータ
# - statsDataId = "0002070001" を使用（例）
# -------------------------------------------------------------

params = {
    "appId": APP_ID,                  # 必須：アプリケーションID
    "statsDataId": "0002070001",     # 統計表ID（家計調査・用途分類（総数））
    "cdArea": "00000",               # 全国（地域コード）
    # ※cdCat01 などカテゴリコードを指定すれば特定の分類を絞れる
    "metaGetFlg": "Y",               # メタ情報を取得（統計表の属性情報など）
    "cntGetFlg": "N",                # 件数取得フラグ（Nで取得しない）
    "explanationGetFlg": "Y",        # 統計表の説明情報を取得
    "annotationGetFlg": "Y",         # 注釈情報を取得
    "sectionHeaderFlg": "1",         # セクション見出し行を出力に含める
    "replaceSpChars": "0",           # 特殊文字の置換設定（0でそのまま）
    "lang": "J",                      # 出力言語：J = 日本語
    "startPosition" : 1000           #データの1000番目から取得
}

# -------------------------------------------------------------
# 【API実行とレスポンス取得】
# -------------------------------------------------------------

response = requests.get(API_URL, params=params)

# JSON形式でレスポンスを取得
data = response.json()

# -------------------------------------------------------------
# 【結果の表示】
# - 統計名、タイトル、対象期間、項目の一部を表示
# -------------------------------------------------------------

try:
    stat_name = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["TABLE_INF"]["STATISTICS_NAME"]
    title = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["TABLE_INF"]["TITLE"]["$"]
    cycle = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["TABLE_INF"]["CYCLE"]
    survey_date = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["TABLE_INF"]["SURVEY_DATE"]

    print("統計名：", stat_name)
    print("表題 ：", title)
    print("周期 ：", cycle)
    print("調査日：", survey_date)
    print()

    # 実際の値（例：VALUE）の中から先頭3件を表示
    values = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
    for value in values[:3]:
        print(f"時期: {value['@time']}, 値: {value.get('$', 'N/A')}")

except KeyError as e:
    print("データの解析中にエラーが発生しました:", e)
    print("APIレスポンス:", data)
