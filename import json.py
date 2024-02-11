import json
import random
from datetime import datetime, timedelta

# Function to generate random dates within a given range
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Function to generate a dataset for a student's university studies
def generate_student_dataset(start_date, end_date):
    dataset = []

    current_date = start_date
    while current_date <= end_date:
        # Simulate attending lectures
        lectures_attended = random.randint(2, 6)

        # Simulate completing assignments
        assignments_completed = random.randint(0, 3)

        # Simulate reading books
        books_read = random.randint(0, 2)
        books = []
        for _ in range(books_read):
            book = {
                'title': f'Book{_ + 1}',
                'author': f'Author{_ + 1}',
                'pages_read': random.randint(20, 200)
            }
            books.append(book)

        # Simulate grades obtained
        grades = {
            'mathematics': round(random.uniform(60, 100), 2),
            'literature': round(random.uniform(60, 100), 2)
        }

        # Create a record for the current date
        record = {
            'date': current_date.strftime('%Y-%m-%d'),
            'lectures_attended': lectures_attended,
            'assignments_completed': assignments_completed,
            'books_read': books,
            'grades': grades
        }

        dataset.append(record)

        # Move to the next day
        current_date += timedelta(days=1)

    return dataset

# Set the start and end dates for the dataset
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

# Generate the dataset
student_dataset = generate_student_dataset(start_date, end_date)

# Save the dataset to a JSON file
with open('student_dataset.json', 'w') as file:
    json.dump(student_dataset, file, indent=4)

print("Dataset generated and saved successfully!")
