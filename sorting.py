"""Merge Sort (stable, O(n log n)) used to prioritise parcels."""


def merge_sort(items, key=lambda x: x):
    """Return a new list sorted ascending by key(item). Does not use sorted()."""
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        # <= keeps the sort stable (equal keys stay in original order)
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def prioritise_parcels(parcels):
    """Earliest deadline first; ties broken by higher priority first."""
    return merge_sort(parcels, key=lambda p: (p["deadline"], -p["priority"]))
