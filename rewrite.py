from typing import Dict, List


def is_creatable_check(wanted: str, initial: str,
                       rules: Dict[str, List[str]]) -> bool:
    if initial == wanted:
        return True

    if initial in rules:
        
        for elem in rules[initial]:
            if is_creatable_check(wanted, elem, rules):
                return True

    return False


def is_creatable(wanted: str, initial: str,
                 rules: Dict[str, List[str]]) -> bool:
    if wanted == initial:
        return True

    if (wanted != initial and rules == {}) or len(wanted) != len(initial):
        return False

    for i in range(len(wanted)):
        if wanted[i] != initial[i] and not is_creatable_check(wanted[i], initial[i], rules):
            return False

    return True


def main() -> None:
    assert is_creatable("abc", "abc", {})
    assert not is_creatable("bc", "abc", {})
    assert is_creatable("abc", "abc", {"a": ["c", "d"]})
    assert not is_creatable("bbc", "abc", {"a": ["c", "d"]})
    assert is_creatable("aec", "abc",
                        {"a": ["e", "f"], "b": ["a", "f"]})
    assert is_creatable("fec", "abc",
                        {"a": ["e", "f"], "b": ["a", "f"]})
    assert is_creatable("bbb", "aaa", {"a": ["c"], "c": ["b"]})
    assert is_creatable("bcb", "aaa", {"a": ["c"], "c": ["b"]})
    assert is_creatable("ccc", "aaa", {"a": ["c"], "c": ["b"]})
    assert is_creatable("abcd", "aaaa",
                        {"a": ["b", "c", "d", "e"], "c": ["b"]})
    assert is_creatable("a", "a", {"a": ["b", "c"]})
    assert not is_creatable("aa", "bb",
                            {"b": ["c", "d", "e", "f"],
                             "c": ["d", "e", "f"],
                             "d": ["e", "f"],
                             "e": ["f"]})
    assert is_creatable("fd", "bc",
                        {"b": ["c", "d", "e"],
                         "c": ["d"],
                         "d": ["f"],
                         "e": ["f"]})


if __name__ == '__main__':
    main()
