# -*- coding: utf-8 -*-
"""Amazon_Product_Analysis_and_Recommendation_System.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jo4tPM0F15XNkqrga91121mEAvmZ9pfX
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""**Data Extraction**"""

data = pd.read_csv('amazon.csv', error_bad_lines=False)

data.head()

"""**Data Preparation**"""

data.shape

def check_missing_values(data):
  return data.isnull().sum()

print(check_missing_values(data))
data[data.rating_count.isnull()]

data.dropna(subset=['rating_count'],inplace=True)

print(check_missing_values(data))

def check_duplicates(data):
  return data.duplicated().sum()

print(check_duplicates(data))

def check_data_types(data):
  return data.dtypes

print(check_data_types(data))

data['discounted_price'] = data['discounted_price'].astype(str).str.replace('₹','').str.replace(',','').astype(float)
data['actual_price'] = data['actual_price'].astype(str).str.replace('₹','').str.replace(',','').astype(float)
data['discount_percentage'] = data['discount_percentage'].astype(str).str.replace('%','').astype(float)

data = data[data['rating'].apply(lambda x: '|' not in str(x))]

data['rating'] = data['rating'].astype(str).str.replace(',','').astype(float)
data['rating_count'] = data['rating_count'].astype(str).str.replace(',','').astype(float)

print(check_data_types(data))

"""We create a column **rating_weighted** as a way of considering not only the average rating, but also the number of people who rated the product. This column weighs the average rating by the number of ratings, giving more weight to ratings with a large number of raters. This can help identify products with high customer satisfaction and many positive ratings compared to products with high average ratings but few raters."""

data['rating_weighted'] = data['rating']*data['rating_count']

"""We Extract both the **main and final categories** from the category column as it provides us with a clearer picture of how our products are distributed across different categories."""

data['sub_category'] = data['category'].astype(str).str.split('|').str[-1]
data['main_category'] = data['category'].astype(str).str.split('|').str[0]

data.columns

"""**Exploratory Data Analysis**

Analysis of distribution of products by category using a bar plot.
"""

main_category_counts = data['main_category'].value_counts()[:30]

plt.bar(range(len(main_category_counts)),main_category_counts.values)
plt.ylabel('Number of Products')
plt.title('Distribution of Products by Main Categories (Top 30)')
plt.xticks(range(len(main_category_counts)),'')
plt.show()

top_main_categories = pd.DataFrame({'Main Category':main_category_counts.index,'Number of Products':main_category_counts.values})
print('Top main Categories')
print(top_main_categories.to_string(index=False))

sub_category_counts = data['sub_category'].value_counts()[:30]

plt.bar(range(len(sub_category_counts)),sub_category_counts.values)
plt.ylabel('Number of Products')
plt.title('Distribution of Products by Sub Categories (Top 30)')
plt.xticks(range(len(sub_category_counts)),'')
plt.show()

top_sub_categories = pd.DataFrame({'Main Category':sub_category_counts.index,'Number of Products':sub_category_counts.values})
print('Top sub Categories')
print(top_sub_categories.to_string(index=False))

"""Analysis of distribution of customer ratings using a histogram."""

plt.hist(data['rating'])
plt.xlabel('Rating')
plt.ylabel('Number of Reviews')
plt.title('Distribution of Customer Ratings')
plt.show()

bins = [0,1,2,3,4,5]
data['cluster'] = pd.cut(data['rating'],bins=bins,include_lowest = True,labels=['0-1','1-2','2-3','3-4','4-5'])
table = data['cluster'].value_counts().reset_index().sort_values('index').rename(columns={'index':'Cluster','cluster':'Number of Reviews'})
print(table)

top = data.groupby(['main_category'])['rating'].mean().sort_values(ascending=False).head(10).reset_index()
plt.bar(top['main_category'],top['rating'])
plt.xlabel('main category')
plt.ylabel('Rating')
plt.title('Top Categories by Rating')
plt.xticks(rotation=90)
plt.show()

ranking = data.groupby(['main_category'])['rating'].mean().sort_values(ascending=False).reset_index()
print(ranking)

top = data.groupby(['sub_category'])['rating'].mean().sort_values(ascending=False).head(10).reset_index()
plt.bar(top['sub_category'],top['rating'])
plt.xlabel('sub category')
plt.ylabel('Rating')
plt.title('Top Categories by Rating')
plt.xticks(rotation=90)
plt.show()

ranking = data.groupby(['sub_category'])['rating'].mean().sort_values(ascending=False).reset_index()
print(ranking)

mean_discount_by_category = data.groupby('main_category')['discount_percentage'].mean().sort_values(ascending=True)

plt.barh(mean_discount_by_category.index,mean_discount_by_category.values)
plt.title('Discount Percentage by Main Category')
plt.xlabel('Discount Percentage')
plt.ylabel('Main Category')
plt.show()

table = pd.DataFrame({'Main Category':mean_discount_by_category.index,'Mean Discount Percentage':mean_discount_by_category.values})
print(table)

mean_discount_by_sub_category = data.groupby('sub_category')['discount_percentage'].mean().head(15)
mean_discount_by_sub_category = mean_discount_by_sub_category.sort_values(ascending=True)

plt.barh(mean_discount_by_sub_category.index, mean_discount_by_sub_category.values)
plt.title('Discount Percentage by Sub Category')
plt.xlabel('Discount Percentage')
plt.ylabel('Sub Category')
plt.show()

table = pd.DataFrame({'Sub Category': mean_discount_by_sub_category.index, 'Mean Discount Percentage': mean_discount_by_sub_category.values})
print(table)

"""Analysis of reviews by creating word clouds or frequency tables of the most common words used in the reviews."""

from wordcloud import WordCloud

reviews_text = ' '.join(data['review_content'].dropna().values)
wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(reviews_text)
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

high_rating_data = data[data['rating'] > 4.0]
reviews_text = ' '.join(high_rating_data['review_content'].dropna().values)
wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(reviews_text)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

low_rating_data = data[data['rating'] < 3.0]
reviews_text = ' '.join(low_rating_data['review_content'].dropna().values)
wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(reviews_text)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

"""Statistical analysis to identify any correlations between different features."""

numeric_cols = data.select_dtypes(include=['float64','int64'])
correlation_matrix = numeric_cols.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

"""**Product Recommendation System**"""

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
data['user_id_encoded'] = le.fit_transform(data['user_id'])

freq_table = pd.DataFrame({'User ID':data['user_id_encoded'].value_counts().index,'Frequency':data['user_id_encoded'].value_counts().values})
print(freq_table)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_products(df, user_id_encoded):
    tfidf = TfidfVectorizer(stop_words='english')
    df['about_product'] = df['about_product'].fillna('')  # fill NaN values with empty string
    tfidf_matrix = tfidf.fit_transform(df['about_product'])

    user_history = df[df['user_id_encoded'] == user_id_encoded]
    indices = user_history.index.tolist()

    if indices:
        cosine_sim_user = cosine_similarity(tfidf_matrix[indices], tfidf_matrix)
        products = df.iloc[indices]['product_name']
        indices = pd.Series(products.index, index=products)

        similarity_scores = list(enumerate(cosine_sim_user[-1]))
        similarity_scores = [(i, score) for (i, score) in similarity_scores if i not in indices]
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        top_products = [i[0] for i in similarity_scores[1:6]]

        recommended_products = df.iloc[top_products]['product_name'].tolist()

        score = [similarity_scores[i][1] for i in range(5)]

        results_df = pd.DataFrame({'Id Encoded': [user_id_encoded] * 5,
                                   'recommended product': recommended_products,
                                   'score recommendation': score})

        return results_df

    else:
        print("No purchase history found.")
        return None

recommend_products(data,17)

"""**Insights**

**Main Categories and Subcategories:**


*   **Popularity**: Electronics, Computers & Accessories, and Home & Kitchen are the most popular main categories.
*   **Customer Satisfaction**: Office Products and Home Improvement receive high ratings, while Car & Motorbike and Health & Personal Care have lower ratings.
*   **Product Focus**: Businesses can consider focusing on Computers & Accessories and Electronics due to their popularity and high ratings.


**Customer Ratings and Discounts:**

* **Rating Distribution**: Most customer ratings fall within the 3-4 and 4-5 ranges.
* **Room for Improvement**: There is room for improvement in the 0-1 and 1-2 rating ranges.
*   **Discount Strategies**: Discounts can influence customer ratings, especially in price-sensitive categories.
* Diverse Discounts: Discount percentages vary across categories and subcategories, impacting pricing strategies.

**Correlations:**

* **Rating Factors**: Ratings are weakly correlated with the number of reviews and product discounts.

* **Customer Feedback**: Enhancing product quality and customer satisfaction can lead to higher positive ratings and customer loyalty.
"""

