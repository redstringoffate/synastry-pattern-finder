import itertools
import pandas as pd


# ------------------ 기본 유틸 ------------------

def aspect_exists(df, p1, p2, aspects):
    """두 포인트 간 특정 Aspect가 존재하는지 확인"""
    mask1 = (df["From"] == p1) & (df["To"] == p2)
    mask2 = (df["From"] == p2) & (df["To"] == p1)
    return any(df.loc[mask1 | mask2, "Aspect"].isin(aspects))


def valid_combo(combo):
    """A와 B가 동시에 포함된 조합만 허용"""
    joined = " ".join(combo)
    return ("A_" in joined) and ("B_" in joined)


# ------------------ 패턴 감지 ------------------

def detect_grand_trine(df):
    """한 점이 두 개의 Trine을 가지는 구조"""
    results = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        if not valid_combo(combo):
            continue
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Trine"])
            and aspect_exists(df, p1, p3, ["Trine"])
        ):
            results.append(combo)
    return results


def detect_kite(df):
    """Grand Trine + Opposition"""
    results = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 4):
        if not valid_combo(combo):
            continue
        p1, p2, p3, p4 = combo
        trine_count = sum([
            aspect_exists(df, p1, p2, ["Trine"]),
            aspect_exists(df, p1, p3, ["Trine"]),
            aspect_exists(df, p2, p3, ["Trine"]),
        ])
        opp = any(aspect_exists(df, p, p4, ["Opposition"]) for p in [p1, p2, p3])
        if trine_count >= 2 and opp:
            results.append(combo)
    return results


def detect_yod(df):
    """두 개의 Quincunx + Sextile"""
    results = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        if not valid_combo(combo):
            continue
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Quincunx"])
            and aspect_exists(df, p1, p3, ["Quincunx"])
            and aspect_exists(df, p2, p3, ["Sextile"])
        ):
            results.append(combo)
    return results


def detect_thors_hammer(df):
    """두 개의 Sesquiquadrate + Square"""
    results = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        if not valid_combo(combo):
            continue
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Sesquiquadrate"])
            and aspect_exists(df, p1, p3, ["Sesquiquadrate"])
            and aspect_exists(df, p2, p3, ["Square"])
        ):
            results.append(combo)
    return results


def detect_tsquare(df):
    """Opposition + 두 개의 Square"""
    results = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        if not valid_combo(combo):
            continue
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Opposition"])
            and aspect_exists(df, p1, p3, ["Square"])
            and aspect_exists(df, p2, p3, ["Square"])
        ):
            results.append(combo)
    return results


def detect_mystic_rectangle(df):
    """Opposition 2개 + Sextile 2개"""
    results = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 4):
        if not valid_combo(combo):
            continue
        opps = 0
        sexts = 0
        for p1, p2 in itertools.combinations(combo, 2):
            if aspect_exists(df, p1, p2, ["Opposition"]):
                opps += 1
            if aspect_exists(df, p1, p2, ["Sextile"]):
                sexts += 1
        if opps >= 2 and sexts >= 2:
            results.append(combo)
    return results


def detect_double_trine(df):
    """한 포인트가 두 개의 Trine을 맺는 단순 패턴"""
    results = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        if not valid_combo(combo):
            continue
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Trine"])
            and aspect_exists(df, p1, p3, ["Trine"])
        ):
            results.append(combo)
    return results


def detect_golden_yod(df):
    """Quintile 기반의 Yod 변형"""
    results = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        if not valid_combo(combo):
            continue
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Bi-quintile", "Quintile"])
            and aspect_exists(df, p1, p3, ["Quincunx"])
            and aspect_exists(df, p2, p3, ["Quincunx"])
        ):
            results.append(combo)
    return results


def detect_finger_of_fate(df):
    """두 개의 Semi-sextile + Quincunx (Minor)"""
    results = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        if not valid_combo(combo):
            continue
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Semi-sextile"])
            and aspect_exists(df, p1, p3, ["Semi-sextile"])
            and aspect_exists(df, p2, p3, ["Quincunx"])
        ):
            results.append(combo)
    return results


# ------------------ 메인 호출 ------------------

def detect_patterns(df):
    """Synastry 전용 — A/B 구분 유지하되 전체 pool에서 감지"""
    if df.empty:
        return {}

    return {
        "Grand Trine": detect_grand_trine(df),
        "Kite": detect_kite(df),
        "Yod": detect_yod(df),
        "Thor’s Hammer": detect_thors_hammer(df),
        "T-Square": detect_tsquare(df),
        "Mystic Rectangle": detect_mystic_rectangle(df),
        "Double Trine": detect_double_trine(df),
        "Golden Yod": detect_golden_yod(df),
        "Finger of Fate": detect_finger_of_fate(df),
    }
