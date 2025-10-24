import itertools
import pandas as pd


# 🔧 유틸리티 --------------------------------------------------------

def aspect_exists(df, p1, p2, aspect_list):
    """두 포인트 간 Aspect 존재 여부"""
    mask1 = (df["From"] == p1) & (df["To"] == p2)
    mask2 = (df["From"] == p2) & (df["To"] == p1)
    return any(df.loc[mask1 | mask2, "Aspect"].isin(aspect_list))


def is_mixed_pattern(combo, person_map):
    """A/B가 모두 포함된 조합만 허용"""
    persons = {person_map[p[0]] for p in combo if p[0] in person_map}
    return len(persons) > 1


def build_person_map(df):
    """라벨 맨 앞의 A_ / B_ 기준으로 인물 분류"""
    labels = list(set(df["From"]).union(df["To"]))
    person_map = {}
    for lbl in labels:
        if lbl.startswith("A_"):
            person_map[lbl[0]] = "A"
        elif lbl.startswith("B_"):
            person_map[lbl[0]] = "B"
        else:
            person_map[lbl[0]] = "?"
    return {lbl: ("A" if lbl.startswith("A_") else "B") for lbl in labels}


# 🜂 도형 탐지 로직 --------------------------------------------------

def detect_grand_trine(df, person_map):
    """한 점이 두 개의 Trine을 가지는 구조"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Trine"])
            and aspect_exists(df, p1, p3, ["Trine"])
            and is_mixed_pattern(combo, person_map)
        ):
            patterns.append(combo)
    return patterns


def detect_kite(df, person_map):
    """Grand Trine + Opposite 연결"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 4):
        p1, p2, p3, p4 = combo
        trines = sum([
            aspect_exists(df, p1, p2, ["Trine"]),
            aspect_exists(df, p1, p3, ["Trine"]),
            aspect_exists(df, p2, p3, ["Trine"]),
        ])
        opp = any(aspect_exists(df, p, p4, ["Opposition"]) for p in [p1, p2, p3])
        if trines >= 2 and opp and is_mixed_pattern(combo, person_map):
            patterns.append(combo)
    return patterns


def detect_yod(df, person_map):
    """두 개의 Quincunx + Sextile"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Quincunx"])
            and aspect_exists(df, p1, p3, ["Quincunx"])
            and aspect_exists(df, p2, p3, ["Sextile"])
            and is_mixed_pattern(combo, person_map)
        ):
            patterns.append(combo)
    return patterns


def detect_thors_hammer(df, person_map):
    """두 개의 Sesquiquadrate + Square"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Sesquiquadrate"])
            and aspect_exists(df, p1, p3, ["Sesquiquadrate"])
            and aspect_exists(df, p2, p3, ["Square"])
            and is_mixed_pattern(combo, person_map)
        ):
            patterns.append(combo)
    return patterns


def detect_tsquare(df, person_map):
    """Opposition + 두 Square"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Opposition"])
            and aspect_exists(df, p1, p3, ["Square"])
            and aspect_exists(df, p2, p3, ["Square"])
            and is_mixed_pattern(combo, person_map)
        ):
            patterns.append(combo)
    return patterns


def detect_mystic_rectangle(df, person_map):
    """Opposition 2개 + Sextile 2개"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 4):
        opps = 0
        sexts = 0
        for p1, p2 in itertools.combinations(combo, 2):
            if aspect_exists(df, p1, p2, ["Opposition"]):
                opps += 1
            if aspect_exists(df, p1, p2, ["Sextile"]):
                sexts += 1
        if opps >= 2 and sexts >= 2 and is_mixed_pattern(combo, person_map):
            patterns.append(combo)
    return patterns


def detect_double_trine(df, person_map):
    """한 포인트가 두 개의 Trine을 맺는 간단 패턴"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Trine"])
            and aspect_exists(df, p1, p3, ["Trine"])
            and is_mixed_pattern(combo, person_map)
        ):
            patterns.append(combo)
    return patterns


def detect_golden_yod(df, person_map):
    """Quintile 기반 Yod"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Bi-quintile", "Quintile"])
            and aspect_exists(df, p1, p3, ["Quincunx"])
            and aspect_exists(df, p2, p3, ["Quincunx"])
            and is_mixed_pattern(combo, person_map)
        ):
            patterns.append(combo)
    return patterns


def detect_finger_of_fate(df, person_map):
    """Minor: 두 개의 Semisextile + Quincunx"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Semi-sextile"])
            and aspect_exists(df, p1, p3, ["Semi-sextile"])
            and aspect_exists(df, p2, p3, ["Quincunx"])
            and is_mixed_pattern(combo, person_map)
        ):
            patterns.append(combo)
    return patterns


# 🔮 메인 호출 --------------------------------------------------------

def detect_patterns(df):
    """Synastry 전용 도형 감지"""
    if df.empty:
        return {}

    person_map = build_person_map(df)

    return {
        "Grand Trine": detect_grand_trine(df, person_map),
        "Kite": detect_kite(df, person_map),
        "Yod": detect_yod(df, person_map),
        "Thor’s Hammer": detect_thors_hammer(df, person_map),
        "T-Square": detect_tsquare(df, person_map),
        "Mystic Rectangle": detect_mystic_rectangle(df, person_map),
        "Double Trine": detect_double_trine(df, person_map),
        "Golden Yod": detect_golden_yod(df, person_map),
        "Finger of Fate": detect_finger_of_fate(df, person_map),
    }
