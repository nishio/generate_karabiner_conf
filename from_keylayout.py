from generate_karabiner_conf import build_karabiner_conf
from string import ascii_lowercase, ascii_uppercase
import json

KANA = [
    'ぁ', 'あ', 'ぃ', 'い', 'ぅ', 'う', 'ぇ', 'え', 'ぉ', 'お', 'ゔ',
    'か', 'が', 'き', 'ぎ', 'く', 'ぐ', 'け', 'げ', 'こ', 'ご',
    'さ', 'ざ', 'し', 'じ', 'す', 'ず', 'せ', 'ぜ', 'そ', 'ぞ',
    'た', 'だ', 'ち', 'ぢ', 'っ', 'つ', 'づ', 'て', 'で', 'と', 'ど', 'な', 'に', 'ぬ', 'ね', 'の',
    'は', 'ば', 'ぱ', 'ひ', 'び', 'ぴ', 'ふ', 'ぶ', 'ぷ', 'へ', 'べ', 'ぺ', 'ほ', 'ぼ', 'ぽ',
    'ま', 'み', 'む', 'め', 'も', 'ゃ', 'や', 'ゅ', 'ゆ', 'ょ', 'よ',
    'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん',
    '０', '１', '２', '３', '４', '５', '６', '７', '８', '９']
ROMA = [
    'xa', 'a', 'xi', 'i', 'xu', 'u', 'xe', 'e', 'xo', 'o', 'vu',
    'ka', 'ga', 'ki', 'gi', 'ku', 'gu', 'ke', 'ge', 'ko', 'go',
    'sa', 'za', 'shi', 'ji', 'su', 'zu', 'se', 'ze', 'so', 'zo',
    'ta', 'da', 'chi', 'di', 'xtu', 'tsu', 'du', 'te', 'de', 'to', 'do', 'na', 'ni', 'nu', 'ne', 'no',
    'ha', 'ba', 'pa', 'hi', 'bi', 'pi', 'fu', 'bu', 'pu', 'he', 'be', 'pe', 'ho', 'bo', 'po',
    'ma', 'mi', 'mu', 'me', 'mo', 'xya', 'ya', 'xyu', 'yu', 'xyo', 'yo',
    'ra', 'ri', 'ru', 're', 'ro', 'wa', 'wo', 'nn',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SIMPLE_MAP = dict(zip(KANA, ROMA))

SPECIAL_MAP = {
    '、': "comma",
    '。': "period",
    '「': "close_bracket",
    '」': "backslash",
    '『': "^close_bracket",
    '』': "^backslash",
    '・': "slash",
    '！': "^1",
    '（': "^8",
    '）': "^9",
    '？': "^slash",
    "ー": "hyphen",
    "：": "quote",
    "〜": "^equal_sign",
}
original_keymap = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '^', '¥',
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '@', '[',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', ':', ']',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '_']

keylayout = """
[["？！１", "・ ２", "〜 ３", "  ４", "  ５", "   ", "  ６", "  ７", " （８", " ）９", "  ０", "   ", "   "],
 ["ぁ  ", "えがか", "りだた", "ゃごこ", "れざさ", "  「", "ぱよら", "ぢにち", "ぐるく", "づまつ", "ぼぇほ",      "   "],
 ["を う", "あじし", "なでて", "ゅげけ", "もぜせ", "  」", "ばみは", "どおと", "ぎのき", "ぽょい", " っん", "  ："],
 ["ぅ ね", "ーびひ", "ろずす", "やぶふ", "ぃべへ", "   ", "ぷぬめ", "ぞゆそ", "ぺむ、", "ぴわ。", " ぉ・"]]
"""


def generate_from_keylayout():
    data = json.loads(keylayout)
    flatten = sum(data, [])
    print(flatten)

    simple_key_chains = []
    special = {}
    for i, v in enumerate(flatten):
        v += "   "
        base = v[2]
        left = v[0]
        right = v[1]
        orig = original_keymap[i]
        base = SIMPLE_MAP.get(base, "?")
        left = SIMPLE_MAP.get(left, "?")
        right = SIMPLE_MAP.get(right, "?")
        simple_key_chains.append(f"{orig} {base} {left} {right}")

        if base == "?":
            special[f"{orig}BASE"] = SPECIAL_MAP.get(v[2], "?")
        if left == "?":
            special[f"{orig}LEFT"] = SPECIAL_MAP.get(v[0], "?")
        if right == "?":
            special[f"{orig}RIGHT"] = SPECIAL_MAP.get(v[1], "?")

    path = "tmp"
    title = "tmp"
    desc = "tmp"
    json.dump(
        build_karabiner_conf(title, desc, special, simple_key_chains),
        open(
            "/Users/nishio/.config/karabiner/assets/complex_modifications/" +
            f"{path}.json", "w"), indent=2)


generate_from_keylayout()
