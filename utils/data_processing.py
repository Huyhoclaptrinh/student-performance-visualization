import pandas as pd

input_path = "data/StudentsPerformance.csv"
output_path = "data/StudentsPerformance_clean.csv"

# Load raw data
df = pd.read_csv(input_path)

# Cleaning and feature engineering
df = df.dropna().drop_duplicates().reset_index(drop=True)

df["total score"] = df['math score'] + df['reading score'] + df['writing score']
df["average score"] = df["total score"] / 3

# Performance category
# I ask GPT for the idea of performance category
# Promt: "Can you suggest a way to categorize students based on their average scores?"
# Response: "You can create bins for average scores. For example:
# - Below Average: 0-60
# - Average: 60-75
# - Above Average: 75-100
# This categorization can help in understanding the performance distribution of students."
bins = [0, 60, 75, 100]
labels = ["Below Average", "Average", "Above Average"]

df["performance category"] = pd.cut(df["average score"], bins=bins, labels=labels)

# Save the cleaned DataFrame
df.to_csv(output_path, index=False)
print(f"Cleaned data saved to: {output_path}")