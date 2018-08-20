# -*- coding: utf-8 -*-
import json
LEFT_THUMB_SHIFT = "spacebar"
RIGHT_THUMB_SHIFT = "lang1"
ROMAJI_SECOND_SHIFT = "lang1"
conditions_ja = json.load(open("conditions_ja.json"))

simple_key_chains = open("SIMPLE_KEY_CHAINS.txt").read().strip().split("\n")

def build_karabiner_conf():
    return dict(
        title="Generative Orz",
        rules=[dict(
                description="Program-generated Thumb-shift Keyboard Layout for Karabiner",
                manipulators=build_manipulators()
        )]
    )

def load_special():
    global special
    lines = open("SPECIAL.txt").read().strip().split("\n")
    special = dict(line.split("\t") for line in lines)
load_special()

def build_special_to(base, mod):
    target = special[base + mod]
    if target == "?":
        return None
    ret = []
    for kc in target.split():
        if kc[0] == "#":
            # comment
            continue
        if kc[0] == "^":
            d = dict(
                key_code=kc[1:],
                repeat=False,
                modifiers=["left_shift"]
            )
        else:
            d = dict(
                key_code=kc,
                repeat=False,
            )
        ret.append(d)
    return ret

def build_to(chars, base, mod):
    if chars == "?":
        return build_special_to(base, mod)
    ret = []
    for c in chars:
        d = dict(
            key_code=c,
            repeat=False
        )
        ret.append(d)
    return ret

# 日本語JISキーボードでキートップに書かれている文字からキーコードへの対応づけ
CHAR_TO_KEYCODE = open("CHAR_TO_KEYCODE.txt").read().strip().split("\n")
CHAR_TO_KEYCODE = {x[0]:x[2:] for x in CHAR_TO_KEYCODE}
def char_to_keycode(c):
    return CHAR_TO_KEYCODE.get(c, c)

def build_manipulators():
    ret = []
    for v in simple_key_chains:
        if not v: continue
        print(v)
        v = v.split()
        base, j_base, j_left, j_right = v
        kc_base = char_to_keycode(base)

        # base
        frm = build_simultaneous(kc_base)
        to = build_to(j_base, base, "BASE")
        if to:
            ret.append(build_manipulator(frm, to))

        # left
        frm = build_simultaneous(kc_base, LEFT_THUMB_SHIFT)
        to = build_to(j_left, base, "LEFT")
        if to:
            ret.append(build_manipulator(frm, to))

        # right
        frm = build_simultaneous(kc_base, RIGHT_THUMB_SHIFT)
        to = build_to(j_right, base, "RIGHT")
        if to:
            ret.append(build_manipulator(frm, to))

    return ret


def build_manipulator(frm, to, typ="basic", conditions=conditions_ja):
    return {
        "from": frm,
        "to": to,
        "type": typ,
        "conditions": conditions
    }

def build_simultaneous(*args):
    return dict(
        simultaneous=[
            dict(key_code=x)
            for x in args
        ]
    )


json.dump(build_karabiner_conf(), open("orz.json", "w"), indent=2)


