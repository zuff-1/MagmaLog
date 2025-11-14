import os

file_counts = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = sum(1 for _ in f)
                    file_counts.append((file_path, lines))
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")

# Sort files by line count descending
file_counts.sort(key=lambda x: x[1], reverse=True)

total_lines = sum(count for _, count in file_counts)

# Print table header
print(f"{'File':<50} {'Lines':>6}")
print("-" * 60)

# Print each file
for file_path, count in file_counts:
    print(f"{file_path:<50} {count:>6}")

print("-" * 60)
print(f"{'Total':<50} {total_lines:>6}")