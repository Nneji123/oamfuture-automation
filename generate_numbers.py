import csv
import random


# Function to generate a random 5-digit number
def generate_random_digits():
    return str(random.randint(0, 99999)).zfill(
        5
    )  # Ensure 5 digits with leading zeros if needed


# Function to create a list of dictionaries with numbers and statuses
def generate_numbers_and_statuses(num_count):
    data = []
    for _ in range(num_count):
        random_digits = generate_random_digits()
        result = "76770" + random_digits
        # status = "Generated"
        data.append({"Numbers": result, "Status": ""})
    return data


# Calculate the maximum possible number of unique numbers
max_possible_numbers = 10**5

# Set num_records to the maximum possible
num_records = max_possible_numbers

# Generate the data
data_to_write = generate_numbers_and_statuses(num_records)

# Specify the CSV file name
csv_file_name = "generated_numbers.csv"

# Write the data to the CSV file
with open(csv_file_name, mode="w", newline="") as file:
    fieldnames = ["Numbers", "Status"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for row in data_to_write:
        writer.writerow(row)

print(
    f"{num_records} numbers with statuses have been generated and saved to {csv_file_name}."
)
