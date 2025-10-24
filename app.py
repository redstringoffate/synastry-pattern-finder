import itertools
import pandas as pd

# ======================
# 🔮 유틸리티
# ======================

def is_mixed_pattern(combo, person_map):
    """도형 내에 B가 하나라도 포함되어 있으면 인정"""
    owners = {person_map.get(p, None) for p in combo}
    return "B" in owners


def aspect_exists(df, p1, p2, aspects):
    """두 포인트 간 특정 Aspect가 존재하는지 확인"""
    subset = df[
        ((df["From"] == p1) & (df["To"] == p2))
        | ((df["From"] == p2) & (df["To"] == p1))
    ]
    return any(subset["Aspect"].isin(aspects))


# ======================
# 🔷 개별 도형 감지 함수
# ======================

def detect_grand_trine(df, person_map):
    """3개의 Trine으로 이루어진 Grand Trine"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        p1, p2, p3 = combo
        if (
            aspect_exists(df, p1, p2, ["Trine"])
            and aspect_exists(df, p2, p3, ["Trine"])
            and aspect_exists(df, p1, p3, ["Trine"])
            and is_mixed_pattern(combo, person_map)
        ):
            patterns.append(combo)
    return patterns


def detect_t_square(df, person_map):
    """Opposition + 두 개의 Square"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        p1, p2, p3 = combo
        has_oppo = aspect_exists(df, p1, p2, ["Opposition"])
        has_square_1 = aspect_exists(df, p1, p3, ["Square"])
        has_square_2 = aspect_exists(df, p2, p3, ["Square"])
        if has_oppo and has_square_1 and has_square_2 and is_mixed_pattern(combo, person_map):
            patterns.append(combo)
    return patterns


def detect_yod(df, person_map):
    """두 개의 Quincunx + Sextile"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 3):
        p1, p2, p3 = combo
        q1 = aspect_exists(df, p1, p2, ["Quincunx"])
        q2 = aspect_exists(df, p1, p3, ["Quincunx"])
        s1 = aspect_exists(df, p2, p3, ["Sextile"])
        if q1 and q2 and s1 and is_mixed_pattern(combo, person_map):
            patterns.append(combo)
    return patterns


def detect_grand_cross(df, person_map):
    """4개의 Square + 2개의 Opposition (Grand Cross)"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 4):
        pairs = list(itertools.combinations(combo, 2))
        oppositions = [p for p in pairs if aspect_exists(df, p[0], p[1], ["Opposition"])]
        squares = [p for p in pairs if aspect_exists(df, p[0], p[1], ["Square"])]
        if len(oppositions) >= 2 and len(squares) >= 4 and is_mixed_pattern(combo, person_map):
            patterns.append(combo)
    return patterns


def detect_kite(df, person_map):
    """Grand Trine + Opposition (Kite)"""
    trines = detect_grand_trine(df, person_map)
    patterns = []
    for tri in trines:
        extra_points = list(set(df["From"]).union(df["To"]) - set(tri))
        for p in extra_points:
            if any(aspect_exists(df, p, t, ["Opposition"]) for t in tri):
                full_combo = tuple(sorted(list(tri) + [p]))
                if is_mixed_pattern(full_combo, person_map):
                    patterns.append(full_combo)
    return patterns


def detect_mystic_rectangle(df, person_map):
    """2 Oppositions + 2 Sextiles + 2 Trines"""
    patterns = []
    labels = list(set(df["From"]).union(df["To"]))
    for combo in itertools.combinations(labels, 4):
        pairs = list(itertools.combinations(combo, 2))
        oppositions = [p for p in pairs if aspect_exists(df, p[0], p[1], ["Opposition"])]
        trines = [p for p in pairs if aspect_exists(df, p[0], p[1], ["Trine"])]
        sextiles = [p for p in pairs if aspect_exists(df, p[0], p[1], ["Sextile"])]
        if len(oppositions) >= 2 and len(trines) >= 2 and len(sextiles) >= 2 and is_mixed_pattern(combo, person_map):
            patterns.append(combo)
    return patterns


# ======================
# 🧭 메인 감지기
# ======================

def detect_patterns(df):
    """Synastry용 Aspect Pattern 탐지"""
    labels = list(set(df["From"]).union(df["To"]))

    # 🪞 A_/B_ prefix 기반 person mapping
    person_map = {}
    for p in labels:
        if p.startswith("A_"):
            person_map[p] = "A"
        elif p.startswith("B_"):
            person_map[p] = "B"

    return {
        "Grand Trine": detect_grand_trine(df, person_map),
        "T-Square": detect_t_square(df, person_map),
        "Yod": detect_yod(df, person_map),
        "Grand Cross": detect_grand_cross(df, person_map),
        "Kite": detect_kite(df, person_map),
        "Mystic Rectangle": detect_mystic_rectangle(df, person_map),
    }
