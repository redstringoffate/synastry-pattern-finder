# detect_patterns_synastry.py
import pandas as pd

# --------------------------------------------
# 공통 필터: 도형에 A와 B가 모두 포함되어야 함
# --------------------------------------------
def is_mixed_pattern(combo, person_map):
    """도형 구성원에 A와 B 모두 포함돼 있는지 확인"""
    owners = {person_map.get(p, None) for p in combo}
    return len(owners.intersection({"A", "B"})) == 2


# --------------------------------------------
# Grand Trine
# --------------------------------------------
def detect_grand_trine(df, person_map):
    trines = df[df["Aspect"] == "Trine"]
    combos = []
    labels = sorted(set(df["From"]).union(df["To"]))
    for i in range(len(labels)):
        for j in range(i+1, len(labels)):
            for k in range(j+1, len(labels)):
                a, b, c = labels[i], labels[j], labels[k]
                if (
                    any((df["From"] == a) & (df["To"] == b) & (df["Aspect"] == "Trine")) and
                    any((df["From"] == b) & (df["To"] == c) & (df["Aspect"] == "Trine")) and
                    any((df["From"] == a) & (df["To"] == c) & (df["Aspect"] == "Trine"))
                ):
                    if is_mixed_pattern((a, b, c), person_map):
                        combos.append((a, b, c))
    return combos


# --------------------------------------------
# T-Square
# --------------------------------------------
def detect_tsquare(df, person_map):
    combos = []
    oppositions = df[df["Aspect"] == "Opposition"]
    squares = df[df["Aspect"] == "Square"]
    labels = sorted(set(df["From"]).union(df["To"]))
    for i in range(len(labels)):
        for j in range(i+1, len(labels)):
            for k in range(len(labels)):
                if i == k or j == k:
                    continue
                a, b, c = labels[i], labels[j], labels[k]
                if (
                    any((df["From"] == a) & (df["To"] == b) & (df["Aspect"] == "Opposition")) and
                    any((df["From"] == a) & (df["To"] == c) & (df["Aspect"] == "Square")) and
                    any((df["From"] == b) & (df["To"] == c) & (df["Aspect"] == "Square"))
                ):
                    if is_mixed_pattern((a, b, c), person_map):
                        combos.append((a, b, c))
    return combos


# --------------------------------------------
# Yod
# --------------------------------------------
def detect_yod(df, person_map):
    sextiles = df[df["Aspect"] == "Sextile"]
    quincunxes = df[df["Aspect"] == "Quincunx"]
    combos = []
    labels = sorted(set(df["From"]).union(df["To"]))
    for i in range(len(labels)):
        for j in range(i+1, len(labels)):
            for k in range(j+1, len(labels)):
                a, b, c = labels[i], labels[j], labels[k]
                if (
                    any((df["From"] == a) & (df["To"] == b) & (df["Aspect"] == "Sextile")) and
                    any((df["From"] == a) & (df["To"] == c) & (df["Aspect"] == "Quincunx")) and
                    any((df["From"] == b) & (df["To"] == c) & (df["Aspect"] == "Quincunx"))
                ):
                    if is_mixed_pattern((a, b, c), person_map):
                        combos.append((a, b, c))
    return combos


# --------------------------------------------
# Kite
# --------------------------------------------
def detect_kite(df, person_map):
    combos = []
    trines = df[df["Aspect"] == "Trine"]
    sextiles = df[df["Aspect"] == "Sextile"]
    oppositions = df[df["Aspect"] == "Opposition"]
    labels = sorted(set(df["From"]).union(df["To"]))
    for i in range(len(labels)):
        for j in range(i+1, len(labels)):
            for k in range(j+1, len(labels)):
                for l in range(k+1, len(labels)):
                    a, b, c, d = labels[i], labels[j], labels[k], labels[l]
                    if (
                        any((df["From"] == a) & (df["To"] == b) & (df["Aspect"] == "Trine")) and
                        any((df["From"] == b) & (df["To"] == c) & (df["Aspect"] == "Trine")) and
                        any((df["From"] == a) & (df["To"] == c) & (df["Aspect"] == "Trine")) and
                        any((df["From"] == a) & (df["To"] == d) & (df["Aspect"] == "Opposition")) and
                        (
                            any((df["From"] == d) & (df["To"] == b) & (df["Aspect"] == "Sextile")) or
                            any((df["From"] == d) & (df["To"] == c) & (df["Aspect"] == "Sextile"))
                        )
                    ):
                        if is_mixed_pattern((a, b, c, d), person_map):
                            combos.append((a, b, c, d))
    return combos


# --------------------------------------------
# Mystic Rectangle
# --------------------------------------------
def detect_mystic_rectangle(df, person_map):
    combos = []
    oppositions = df[df["Aspect"] == "Opposition"]
    sextiles = df[df["Aspect"] == "Sextile"]
    trines = df[df["Aspect"] == "Trine"]
    labels = sorted(set(df["From"]).union(df["To"]))
    for i in range(len(labels)):
        for j in range(i+1, len(labels)):
            for k in range(j+1, len(labels)):
                for l in range(k+1, len(labels)):
                    a, b, c, d = labels[i], labels[j], labels[k], labels[l]
                    if (
                        any((df["From"] == a) & (df["To"] == c) & (df["Aspect"] == "Opposition")) and
                        any((df["From"] == b) & (df["To"] == d) & (df["Aspect"] == "Opposition")) and
                        any((df["From"] == a) & (df["To"] == b) & (df["Aspect"] == "Sextile")) and
                        any((df["From"] == c) & (df["To"] == d) & (df["Aspect"] == "Sextile"))
                    ):
                        if is_mixed_pattern((a, b, c, d), person_map):
                            combos.append((a, b, c, d))
    return combos


# --------------------------------------------
# 메인 탐지 함수
# --------------------------------------------
def detect_patterns(df):
    # 🩶 A/B 매핑 자동 추출
    person_map = {}
    for i, row in df.iterrows():
        for col in ["From", "To"]:
            if "A" in row[col]:
                person_map[row[col]] = "A"
            elif "B" in row[col]:
                person_map[row[col]] = "B"

    patterns = {
        "Grand Trine": detect_grand_trine(df, person_map),
        "T-Square": detect_tsquare(df, person_map),
        "Yod": detect_yod(df, person_map),
        "Kite": detect_kite(df, person_map),
        "Mystic Rectangle": detect_mystic_rectangle(df, person_map),
    }
    return patterns
