def calculate_statistics(data):
    if not data:
        return None

    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = variance ** 0.5

    return {
        "mean": mean,
        "variance": variance,
        "std_dev": std_dev
    }

def find_outliers(data, threshold=2):
    stats = calculate_statistics(data)
    if stats is None:
        return []

    mean = stats["mean"]
    std_dev = stats["std_dev"]

    outliers = []
    for value in data:
        if abs(value - mean) > threshold * std_dev:
            outliers.append(value)

    return outliers

def main():
    import random
    data = [random.gauss(50, 10) for _ in range(100)]
    data += [5, 150]  # Add some outliers

    print("Original Data Summary:")
    print(calculate_statistics(data))

    outliers = find_outliers(data)
    print(f"Detected Outliers: {outliers}")

if __name__ == "__main__":
    main()
