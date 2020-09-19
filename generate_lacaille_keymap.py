"""
generate ObjectiveC code for:
  getKeyDataForOya(keycode, gOya)
"""
from string import ascii_lowercase, ascii_uppercase

KEYMAP = [
    "a", "s", "d", "f", "h", "g", "z", "x",
    "c", "v", "[Section]", "b", "q", "w", "e", "r",
    "y", "t", "1", "2", "3", "4", "6", "5",
    "^", "9", "7", "-", "8", "0", "[", "o",
    "u", "@", "i", "p", "↩", "l", "j", ":",
    "k", ";", "]", ",", "/", "n", "m", ".",
    "⇥", "␣", "`", "⌫", "⌤", "⎋", "[R⌘]", "⌘",
    "⇧", "⇪", "⌥", "⌃", "[R⇧]", "[R⌥]", "[R⌃]", "[fn]",
    "[F17]", "[K.]", "<42>", "[K*]", "<44>", "[K+]", "<46>", "⌧",
    "[VolumeUp]", "[VolumeDown]", "[Mute]", "[K/]", "[K⌤]", "<4d>", "[K-]", "[F18]",
    "[F19]", "[K=]", "[K0]", "[K1]", "[K2]", "[K3]", "[K4]", "[K5]",
    "[K6]", "[K7]", "[F20]", "[K8]", "[K9]", "¥", "_", "[K,]",
    "[F5]", "[F6]", "[F7]", "[F3]", "[F8]", "[F9]", "[Eisu]", "[F11]",
    "[Kana]", "[F13]", "[F16]", "[F14]", "<6c>", "[F10]", "<6e>", "[F12]",
    "<70>", "[F15]", "[Help]", "↖", "⇞", "⌦", "[F4]", "↘",
    "[F2]", "⇟", "[F1]", "←", "→", "↓", "↑", "<7f>",
]
KEYCODE_SHIFT = KEYMAP.index("⇧")
assert KEYCODE_SHIFT == 0x38

kVK_JIS_Yen = 93
kVK_JIS_Underscore = 94
JIS_KEY_LAYOUT = [
    [18, 19, 20, 21, 23, 22, 26, 28, 25, 29, 27, 24, kVK_JIS_Yen],
    [12, 13, 14, 15, 17, 16, 32, 34, 31, 35, 33, 30],
    [0, 1, 2, 3, 5, 4, 38, 40, 37, 41, 39, 42],
    [6, 7, 8, 9, 11, 45, 46, 43, 47, 44, kVK_JIS_Underscore],
]
FLAT_JIS_KEY_LAYOUT = sum(JIS_KEY_LAYOUT, [])
# MEMO: in Lacaille's ObjC code,
# `LAYOUT_KEY_COUNT = 50`,
# so `LAYOUT_KEY_COUNT - 1` is not 94, it is 49.
# Those differences is absorbed in *getKeyDataForOya
# ```
# (keycode < LAYOUT_KEY_COUNT - 2) ? [(ViewDataModel *)prefLayout[keycode] getKeyData:oya] :
# (keycode == kVK_JIS_Yen) ? [(ViewDataModel * )prefLayout[(LAYOUT_KEY_COUNT - 2)] getKeyData:oya] :
# (keycode == kVK_JIS_Underscore) ? [(ViewDataModel * )prefLayout[(LAYOUT_KEY_COUNT - 1)] getKeyData:oya] :
# [[NSData alloc] initWithBytes:(unsigned char[]){keycode} length: 1]);
# ```


def test_JIS_KEY_LAYOUT():
    """
    >> > test_JIS_KEY_LAYOUT()
    1234567890-^¥
    qwertyuiop@[
    asdfghjkl; :]
    zxcvbnm, ./_
    """
    for row in JIS_KEY_LAYOUT:
        print("".join(KEYMAP[x] for x in row))


SHIFTED_KEYS, BASE_KEYS = (
    "!#$%&'()=~`{}*+?<>|" + "\"" + ascii_uppercase,
    "13456789-^@[]:;/,.¥" + "2" + ascii_lowercase
)
SHIFT_MAP = dict(zip(BASE_KEYS, SHIFTED_KEYS))
REVERSE_SHIFT_MAP = dict(zip(SHIFTED_KEYS, BASE_KEYS))


def test_REVERSE_SHIFT_MAP(x):
    """
    >> > test_REVERSE_SHIFT_MAP("!")
    '1'
    """
    return REVERSE_SHIFT_MAP[x]


def strToKeyData(s):
    """
    >> > strToKeyData("u")
    [32]
    >> > strToKeyData("wo")
    [13, 31]
    >> > strToKeyData("[")
    [30]
    >> > strToKeyData("{")
    [56, 30]
    """
    buf = []
    if s in CUSTOM_SPECIAL_MAP:
        s = CUSTOM_SPECIAL_MAP[s]
    if s in KANA_MAP:
        s = KANA_MAP[s]
    for c in s:
        if c in REVERSE_SHIFT_MAP:
            c = REVERSE_SHIFT_MAP[c]
            buf.append(KEYCODE_SHIFT)
            buf.append(KEYMAP.index(c))
        else:
            buf.append(KEYMAP.index(c))
    return buf


# Sample
original_keymap = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '^', '¥',
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '@', '[',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', ':', ']',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '_']
assert len(original_keymap) == 48
assert FLAT_JIS_KEY_LAYOUT == [KEYMAP.index(c) for c in original_keymap]
shifted_keymap = [SHIFT_MAP.get(c, c) for c in original_keymap]
assert (shifted_keymap == [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '0', '=', '~', '|',
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '`', '{',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '+', '*', '}',
    'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', '_'])

# My keymap definition
keymap_for_BASE = [
    '1', '2', '3', '4', '5', '', '6', '7', '8', '9', '0', '-', '^',
    'q', 'w', 'e', 'r', 't', '!', 'y', 'u', 'i', 'o', 'p', '@',
    'a', 's', 'd', 'f', 'g', '-', 'h', 'j', 'k', 'l', ';', ':',
    'z', 'x', 'c', 'v', 'b', '@', 'n', 'm', ',', '.', '/']
keymap_for_LSHIFT = [
    '', '', '', '', '', '', '', '', '', '', '', '', '',
    '1', '2', '3', '4', '5', '|', '6', '7', '8', '9', '0', '',
    '¥', '/', '=', '{', '}', '', '(', ')', '␣', '"', '', '',
    '?', '-', '+', '[', ']', '^', '*', '_', '', '', '#']
keymap_for_RSHIFT = [
    '!', '"', '#', '$', '%', '', '&', "'", '(', ')', '0', '=', '~',
    'Q', 'W', 'E', 'R', 'T', '&', 'Y', 'U', 'I', 'O', 'P', '`',
    'A', 'S', 'D', 'F', 'G', '_', 'H', 'J', 'K', 'L', '+', '*',
    'Z', 'X', 'C', 'V', 'B', '$', 'N', 'M', '<', '>', '?']
'', '』'
keymap_for_KANA_BASE = [
    '１', '２', '３', '４', '５', '', '６', '７', '８', '９', '０', '', '',
    '␣', 'か', 'た', 'こ', 'さ', '「', 'ら', 'ち', 'く', 'つ', 'ほ', '',
    'う', 'し', 'て', 'け', 'せ', '」', 'は', 'と', 'き', 'い', 'ん', '：',
    'ね', 'ひ', 'す', 'ふ', 'へ', '', 'め', 'そ', '、', '。', '・']
keymap_for_KANA_LSHIFT = [
    '？', '・', '〜', '', '', '', '', '', '', '', '', '', '',
    'ぁ', 'え', 'り', 'ゃ', 'れ', '', 'ぱ', 'ぢ', 'ぐ', 'づ', 'ぼ', '',
    'を', 'あ', 'な', 'ゅ', 'も', '', 'ば', 'ど', 'ぎ', 'ぽ', '', '',
    'ぅ', 'ー', 'ろ', 'や', 'ぃ', '', 'ぷ', 'ぞ', 'ぺ', 'ぴ', '']
keymap_for_KANA_RSHIFT = [
    '！', '', '', '', '', '', '', '', '（', '）', '', '', '',
    '', 'が', 'だ', 'ご', 'ざ', '『', 'よ', 'に', 'る', 'ま', 'ぇ', '',
    'ゔ', 'じ', 'で', 'げ', 'ぜ', '』', 'み', 'お', 'の', 'ょ', 'っ', '',
    '', 'び', 'ず', 'ぶ', 'べ', '', 'ぬ', 'ゆ', 'む', 'わ', 'ぉ']

KANA = [
    '、', '。', '「', '」', '『', '』', '〜',
    'ぁ', 'あ', 'ぃ', 'い', 'ぅ', 'う', 'ぇ', 'え', 'ぉ', 'お', 'ゔ',
    'か', 'が', 'き', 'ぎ', 'く', 'ぐ', 'け', 'げ', 'こ', 'ご',
    'さ', 'ざ', 'し', 'じ', 'す', 'ず', 'せ', 'ぜ', 'そ', 'ぞ',
    'た', 'だ', 'ち', 'ぢ', 'っ', 'つ', 'づ', 'て', 'で', 'と', 'ど', 'な', 'に', 'ぬ', 'ね', 'の',
    'は', 'ば', 'ぱ', 'ひ', 'び', 'ぴ', 'ふ', 'ぶ', 'ぷ', 'へ', 'べ', 'ぺ', 'ほ', 'ぼ', 'ぽ',
    'ま', 'み', 'む', 'め', 'も', 'ゃ', 'や', 'ゅ', 'ゆ', 'ょ', 'よ',
    'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん',
    '・', 'ー', '！', '（', '）', '０', '１', '２', '３', '４', '５', '６', '７', '８', '９', '：', '？']
ROMA = [
    ',', '.', '[', ']', '{', '}', '~', 'xa', 'a', 'xi', 'i', 'xu', 'u', 'xe', 'e', 'xo', 'o', 'vu',
    'ka', 'ga', 'ki', 'gi', 'ku', 'gu', 'ke', 'ge', 'ko', 'go',
    'sa', 'za', 'shi', 'ji', 'su', 'zu', 'se', 'ze', 'so', 'zo',
    'ta', 'da', 'chi', 'di', 'xtu', 'tsu', 'du', 'te', 'de', 'to', 'do', 'na', 'ni', 'nu', 'ne', 'no',
    'ha', 'ba', 'pa', 'hi', 'bi', 'pi', 'fu', 'bu', 'pu', 'he', 'be', 'pe', 'ho', 'bo', 'po',
    'ma', 'mi', 'mu', 'me', 'mo', 'xya', 'ya', 'xyu', 'yu', 'xyo', 'yo',
    'ra', 'ri', 'ru', 're', 'ro', 'wa', 'wo', 'nn',
    '/', '-', '!', '(', ')',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ':', '?']
KANA_MAP = dict(zip(KANA, ROMA))


def to_roma(kana):
    """
    >> > to_roma("うさぎ")
    'usagi'
    """
    return "".join(KANA_MAP[c] for c in kana)


CUSTOM_SPECIAL_MAP = {
    "🤔": "nenexa"
}
LAYOUT_KEY_COUNT = 50


def generate_keymap_data(keymap, as_string=False, as_int=True):
    assert len(keymap) == len(original_keymap)

    if as_string:
        DEFAULT = "0xFF, 0xFF, 0xFF"
    else:
        DEFAULT = [255, 255, 255]
    output = [DEFAULT] * LAYOUT_KEY_COUNT
    if "\\" in keymap:
        raise RuntimeError("use `¥` instead of `\\`")
    if " " in keymap:
        raise RuntimeError("use `␣` instead of ` `")

    for keycode in sorted(FLAT_JIS_KEY_LAYOUT):
        position = original_keymap.index(KEYMAP[keycode])
        newkey = keymap[position]
        newkey = strToKeyData(newkey)
        if as_string:
            newkey = ", ".join(f"0x{x:02X}" for x in newkey)
        if as_int:
            newkey = list(map(int, newkey))
        if keycode == kVK_JIS_Yen:
            index = LAYOUT_KEY_COUNT - 2
        elif keycode == kVK_JIS_Underscore:
            index = LAYOUT_KEY_COUNT - 1
        else:
            index = keycode

        output[index] = newkey
    return output


def generate_objc(keymap, name="FOO"):
    output = generate_keymap_data(keymap, as_string=True, as_int=False)
    output = ", ".join(output)
    print(f"unsigned char keymap_{name}[] = {{{output}}};")


if 0:
    generate_objc(keymap_for_BASE, "ASCII_BASE")
    generate_objc(keymap_for_LSHIFT, "ASCII_LSHIFT")
    generate_objc(keymap_for_RSHIFT, "ASCII_RSHIFT")
    generate_objc(keymap_for_KANA_BASE, "KANA_BASE")
    generate_objc(keymap_for_KANA_LSHIFT, "KANA_LSHIFT")
    generate_objc(keymap_for_KANA_RSHIFT, "KANA_RSHIFT")


def generate_json():
    output = {}
    output["ASCII_BASE"] = generate_keymap_data(keymap_for_BASE)
    output["ASCII_LSHIFT"] = generate_keymap_data(keymap_for_LSHIFT)
    output["ASCII_RSHIFT"] = generate_keymap_data(keymap_for_RSHIFT)
    output["KANA_BASE"] = generate_keymap_data(keymap_for_KANA_BASE)
    output["KANA_LSHIFT"] = generate_keymap_data(keymap_for_KANA_LSHIFT)
    output["KANA_RSHIFT"] = generate_keymap_data(keymap_for_KANA_RSHIFT)
    import json
    json.dump(output, open("/Users/nishio/Dropbox/lacaille.json", "w"), indent=2)


def generate_keylayout(base, lshift, rshift):
    def get(xs, i):
        if xs[i]:
            return xs[i]
        return " "

    def getTri(i):
        return get(lshift, i) + get(rshift, i) + get(base, i)

    row1 = [getTri(i) for i in range(13)]
    row2 = [getTri(i) for i in range(13, 25)]
    row3 = [getTri(i) for i in range(25, 37)]
    row4 = [getTri(i) for i in range(37, 48)]
    return [row1, row2, row3, row4]


def print_json(x):
    import json
    print(json.dumps(x, ensure_ascii=False))


def keylayout_to_keymap(keylayout):
    print([(x + "   ")[2] for x in keylayout])
    print([(x + "   ")[0] for x in keylayout])
    print([(x + "   ")[1] for x in keylayout])


def test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    test()
    generate_json()
    print_json(
        generate_keylayout(
            keymap_for_BASE,
            keymap_for_LSHIFT,
            keymap_for_RSHIFT))
    print_json(
        generate_keylayout(
            keymap_for_KANA_BASE,
            keymap_for_KANA_LSHIFT,
            keymap_for_KANA_RSHIFT))
