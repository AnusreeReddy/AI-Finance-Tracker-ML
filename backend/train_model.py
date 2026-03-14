import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob # Keep import, but .correct() is removed from functions

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Lemmatize function (TextBlob.correct() removed)
def lemmatize_text(text):
    # Only lowercase and lemmatize, no spelling correction
    return ' '.join([lemmatizer.lemmatize(word) for word in text.lower().split()])

# VERIFIED AND FURTHER EXPANDED DATASET (Shopping and Income especially)
data = {
    'description': [
        # Food (26 items)
        'Dinner at restaurant', 'Lunch at cafe', 'Grocery shopping at mall',
        'Breakfast at hotel', 'Snacks at coffee shop', 'Tea at roadside stall', 'Lunch with colleagues',
        'Pizza order online', 'Dinner buffet at restaurant', 'Coffee at Starbucks',
        'Ordered food on Swiggy', 'Ice cream from Baskin Robbins', 'bought groceries', 'cafe bill',
        'bought a large pizza', 'ordered pizza delivery', 'ate pizza for dinner', 'pizza from dominos',
        'fine dining experience', 'fast food purchase', 'supermarket shopping for food',
        'vegetable purchase', 'fruit stand', 'bakery items', 'restaurant bill', 'drink purchase',

        # Travel (23 items)
        'Uber ride', 'Flight to Mumbai', 'Train ticket booking', 'Bus fare payment',
        'Taxi fare to airport', 'Metro card recharge', 'Rental car booking', 'Boat ride tickets',
        'Cab ride to office', 'Petrol for car', 'Highway toll payment', 'Train pass renewal',
        'flight tickets', 'bus travel', 'airport taxi', 'hotel booking', 'vacation package',
        'local transport', 'fuel expense', 'train journey', 'toll gate', 'car rental',

        # Entertainment (20 items)
        'Netflix subscription', 'Movie at PVR', 'Concert ticket', 'Amusement park entry',
        'Museum ticket', 'Live sports match ticket', 'Stand-up comedy show',
        'Amazon Prime renewal', 'Spotify subscription', 'Game download Steam',
        'cinema tickets', 'video game purchase', 'attraction entry fee', 'music concert',
        'theatre show', 'online streaming service', 'app game purchase', 'arcade games',
        'event ticket', 'party expense',

        # Shopping (30 items) - Significantly Expanded
        'New shoes from store', 'Bought jeans online', 'Grocery shopping at Walmart',
        'Bought vegetables from local market', 'Purchased books', 'Bought cosmetics',
        'Purchased gifts for birthday', 'Bought a mobile phone', 'Shopping at mall',
        'new clothes', 'online shopping', 'electronics purchase', 'vegetable market',
        'fashion items', 'home decor', 'jewelry purchase', 'childrens toys', 'sports equipment',
        'bought new running shoes', 'purchased a pair of shoes', 'shoe store visit',
        'footwear shopping', 'dress purchase', 'shirt bought', 'new gadget',
        'books from amazon', 'stationery items', 'kitchen appliances', 'home furnishings',
        'birthday present',

        # Health (18 items)
        'Doctor appointment', 'Buy medicines', 'Health insurance premium',
        'Dental cleaning appointment', 'Gym membership', 'Yoga class payment',
        'Dental appointment', 'General checkup', 'Eye test and glasses', 'Hospital emergency visit',
        'pharmacy bill', 'medical checkup', 'physiotherapy session', 'medicine purchase',
        'health checkup', 'prescription refill', 'clinic visit', 'vaccination cost',

        # Utilities (16 items)
        'Electricity bill', 'Phone recharge', 'Water bill payment', 'Internet broadband bill',
        'DTH recharge', 'Gas bill', 'Mobile data top-up', 'Landline bill payment',
        'home electricity bill', 'wifi bill', 'phone top up', 'cooking gas payment',
        'utility bill payment', 'broadband service', 'water supply bill', 'sewage charges',

        # Education (14 items)
        'Online course payment', 'Tuition fee payment', 'Book purchase for studies',
        'Exam fee', 'Enrolled in Udemy course', 'School uniform purchase',
        'college fees', 'textbook purchase', 'course subscription', 'exam registration',
        'educational software', 'school supplies', 'university tuition', 'workshop fee',

        # Income (25 items) - Expanded slightly
        'Salary for the month', 'Freelance project payment', 'Bonus from office',
        'Dividend from investment', 'Interest from savings', 'Sold old laptop',
        'Monthly paycheck received', 'Payment for consulting', 'Annual bonus',
        'Bank interest credited', 'Stock dividends', 'Sold old phone',
        'Revenue from project', 'Client payment', 'Rental income',
        'Refund received', 'Tax refund', 'Received payment', 'Paycheck deposit',
        'investment returns', 'royalty payment', 'gift money received',
        'consulting fee', 'commission earned', 'investment profit',

        # Rent / Housing (14 items)
        'House rent payment', 'Monthly apartment rent', 'Paying rent to landlord',
        'Security deposit for apartment', 'EMI for home loan', 'Apartment maintenance charges',
        'rent payment', 'home loan installment', 'building maintenance', 'property tax',
        'mortgage payment', 'home renovation', 'furnace repair', 'plumbing service',

        # Insurance (9 items)
        'Car insurance premium', 'Life insurance payment', 'Health policy renewal',
        'auto insurance', 'home insurance', 'travel insurance premium',
        'insurance policy payment', 'premium payment', 'health insurance plan'
    ],
    'category': [
        # Food (26 items)
        'Food', 'Food', 'Shopping', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food',
        'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food', 'Food',

        # Travel (23 items)
        'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel',
        'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel', 'Travel',

        # Entertainment (20 items)
        'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment',
        'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment',
        'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment',

        # Shopping (30 items)
        'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping',
        'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping',
        'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping', 'Shopping',
        'Shopping', 'Shopping', 

        # Health (18 items)
        'Health', 'Health', 'Health', 'Health', 'Health', 'Health', 'Health', 'Health', 'Health', 'Health',
        'Health', 'Health', 'Health', 'Health', 'Health', 'Health', 'Health', 'Health',

        # Utilities (16 items)
        'Utilities', 'Utilities', 'Utilities', 'Utilities', 'Utilities', 'Utilities', 'Utilities', 'Utilities',
        'Utilities', 'Utilities', 'Utilities', 'Utilities', 'Utilities', 'Utilities', 'Utilities', 'Utilities',

        # Education (14 items)
        'Education', 'Education', 'Education', 'Education', 'Education', 'Education',
        'Education', 'Education', 'Education', 'Education', 'Education', 'Education', 'Education', 'Education',

        # Income (25 items)
        'Income', 'Income', 'Income', 'Income', 'Income', 'Income',
        'Income', 'Income', 'Income', 'Income', 'Income', 'Income',
        'Income', 'Income', 'Income', 'Income', 'Income', 'Income', 'Income', 'Income', 'Income', 'Income',
        'Income', 'Income', 'Income',

        # Housing (14 items)
        'Housing', 'Housing', 'Housing', 'Housing', 'Housing', 'Housing',
        'Housing', 'Housing', 'Housing', 'Housing', 'Housing', 'Housing', 'Housing', 'Housing',

        # Insurance (9 items)
        'Insurance', 'Insurance', 'Insurance', 'Insurance', 'Insurance', 'Insurance',
        'Insurance', 'Insurance', 'Insurance'
    ]
}

# --- TEMPORARY CHECK (Can remove this block after successful run, but it's good for verification) ---
if len(data['description']) != len(data['category']):
    print(f"ERROR: Description list length ({len(data['description'])}) does not match category list length ({len(data['category'])}).")
    exit() # Stop the script if there's a mismatch
else:
    print(f"Lengths match: {len(data['description'])} items.")
# --- END TEMPORARY CHECK ---

# Convert to DataFrame and lemmatize
df = pd.DataFrame(data)
df['description'] = df['description'].apply(lemmatize_text)

# Features and Labels
X = df['description']
y = df['category']

# Vectorize
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Save model and vectorizer
joblib.dump(model, 'expense_categorization_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
print("✅ Model and vectorizer saved!")

# Evaluate model
y_pred = model.predict(X_test)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# Define the category to type mapping (same as in app.py)
category_to_type = {
    'Food': 'Expense',
    'Shopping': 'Expense',
    'Travel': 'Expense',
    'Entertainment': 'Expense',
    'Health': 'Expense',
    'Utilities': 'Expense',
    'Education': 'Expense',
    'Housing': 'Expense',
    'Insurance': 'Expense',
    'Income': 'Savings'
}

# Example prediction with type (TextBlob.correct() removed)
new_description = "bonus" # Testing "shoes" directly
lemmatized = lemmatize_text(new_description)
new_tfidf = vectorizer.transform([lemmatized])
prediction_category = model.predict(new_tfidf)[0]
prediction_type = category_to_type.get(prediction_category, 'Unknown')

print(f"\n🧾 Original Description: '{new_description}'")
print(f"   Lemmatized (no spelling correction): '{lemmatized}'")
print(f"   Predicted Detailed Category: {prediction_category}")
print(f"   Predicted Type (Expense/Savings): {prediction_type}")

# Also test "salary" again to ensure it's still correct
new_description = "investment"
lemmatized = lemmatize_text(new_description)
new_tfidf = vectorizer.transform([lemmatized])
prediction_category = model.predict(new_tfidf)[0]
prediction_type = category_to_type.get(prediction_category, 'Unknown')

print(f"\n🧾 Original Description: '{new_description}'")
print(f"   Lemmatized (no spelling correction): '{lemmatized}'")
print(f"   Predicted Detailed Category: {prediction_category}")
print(f"   Predicted Type (Expense/Savings): {prediction_type}")