import re
from nltk.corpus import stopwords
import operator
import math
import random
import numpy as np
#Using feature extraction now
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)

from sklearn.feature_extraction.text import TfidfTransformer
tfidf = TfidfTransformer(norm="l2")

from sklearn.metrics.pairwise import cosine_similarity

presidents=[]
presidents.append("Pranab Kumar Mukherjee (born 11 December 1935) is the 13th and current President of India, he has been in office since July 2012. I a political career spanning six decades, Mukherjee was a senior leader of the Indian National Congress and occupied several ministerial portfolios in the Government of India. Prior to his election as President,Mukherjee was Union Finance Minister from 2009 to 2012, and the Congress party\'s top troubleshooter.Mukherjee got his break in politics in 1969 when Prime Minister Indira Gandhi helped him get elected to the Rajya Sabha, the upper house of Parliament, on a Congress ticket. Following a meteoric rise, he became one of Indira Gandhi\'s most trusted lieutenants, and a minister in her cabinet by 1973. During the controversial Internal Emergency of 1975-77, he was accused (like several other Congress leaders) of committing gross excesses. Mukherjee\'s service in a number of ministerial capacities culminated in his first stint as finance minister in 1982-84. Mukherjee was also Leader of the House in the Rajya Sabha from 1980 to 1985.Mukherjee was sidelined from the Congress during the premiership of Rajiv Gandhi, Indira\'s son. Mukherjee had viewed himself, and not the inexperienced Rajiv, as the rightful successor to Indira following her assassination in 1984. Mukherjee lost out in the ensuing power struggle. He formed his own party, the Rashtriya Samajwadi Congress, which merged with the Congress in 1989 after reaching a consensus with Rajiv Gandhi. Mukherjee\'s political career revived when Prime Minister P. V. Narasimha Rao appointed him Planning Commission head in 1991 and foreign minister in 1995. Following this, as elder statesman of the Congress, Mukherjee was the principal and architect of Sonia Gandhi\'s ascension to the party\'s presidency in 1998.When the Congress-led United Progressive Alliance (UPA) came into power in 2004, Mukherjee won a Lok Sabha (the popularly elected lower house of Parliament) seat for the first time. From then until his resignation in 2012, Mukherjee was practically number-two in Prime Minister Manmohan Singh\'s government. He held a number of key cabinet portfoliosDefence (2004-06), External Affairs (2006-09) and Finance (2009-12)apart from heading several Groups of Ministers (GoMs) and being Leader of the House in the Lok Sabha. After securing the UPA\'s nomination for the country\'s presidency in July 2012, Mukherjee comfortably defeated P. A. Sangma in the race to Rashtrapati Bhavan, winning 70 percent of the electoral-college vote. He is the wealthiest president of India to date.Pranab was born in a Bengali Brahmin family in Mirati in the Birbhum district of Bengal province (now in West Bengal). His father was active in the Indian independence movement and was a member of West Bengal Legislative Council between 1952 and 1964 as a representative of the Indian National Congress and was the member of AICC. His mother was Rajlakshmi.He attended the Suri Vidyasagar College in Suri (Birbhum).")

presidents.append("Pratibha Devisingh Patil (born 19 December 1934) is an Indian politician who served as the 12th President of India from 2007 to 2012. A member of the Indian National Congress, Patil is the only woman to hold the office.She previously served as the Governor of Rajasthan from 2004 to 2007.Pratibha Devisingh Patil is the daughter of Narayan Rao Patil.She was born on 19 December 1934 in the village of Nadgaon, in the Jalgaon district of Maharashtra, India. She was educated initially at R. R. Vidyalaya, Jalgaon, and subsequently was awarded a master's degree in Political Science and Economics by Mooljee Jetha College, Jalgaon (then under Pune University), and then a Bachelor of Law degree by Government Law College, Mumbai, affiliated to the University of Mumbai. Patil then began to practice law at the Jalgaon District Court, while also taking interest in social issues such as improving the conditions faced by Indian women.Patil married Devisingh Ransingh Shekhawat on 7 July 1965. The couple have a daughter and a son, Raosaheb Shekhawat, who is also a politician.The BBC has described Patil\'s political career prior to assuming presidential office as long and largely low-key.In 1962, at the age of 27, she was elected to the Maharashtra Legislative Assembly for the Jalgaon constituency.Thereafter she won in the Muktainagar (formerly Edlabad) constituency on four consecutive occasions between 1967 and 1985, before becoming a Member of Parliament in the Rajya Sabha between 1985 and 1990. In the 1991 elections for the 10th Lok Sabha, she was elected as a Member of Parliament representing the Amravati constituency.A period of retirement from politics followed later in that decade.Patil had held various Cabinet portfolios during her period in the Maharashtra Legislative Assembly and she had also held official positions while in both the Rajya Sabha and Lok Sabha. In addition, she had been for some years the president of the Maharashtra Pradesh Congress Committee and also held office as Director of the National Federation of Urban Co- operative Banks and Credit Societies and as a Member of the Governing Council of the National Co-operative Union of India.On 8 November 2004 she was appointed as the 24th Governor of Rajasthan,the first woman to hold that office and according to the BBC was a low-profile")

presidents.append("Avul Pakir Jainulabdeen Abdul Kalam better known as A.P.J. Abdul Kalam (15 October 1931 - 27 July 2015) was the 11th President of India from 2002 to 2007. A career scientist turned statesman, Kalam was born and raised in Rameswaram, Tamil Nadu, and studied physics and aerospace engineering. He spent the next four decades as a scientist and science administrator, mainly at the Defence Research and Development Organisation (DRDO) and Indian Space Research Organisation (ISRO) and was intimately involved in India\'s civilian space programme and military missile development efforts.He thus came to be known as the Missile Man of India for his work on the development of ballistic missile and launch vehicle technology.He also played a pivotal organisational, technical, and political role in India's Pokhran-II nuclear tests in 1998, the first since the original nuclear test by India in 1974.Kalam was elected as the 11th President of India in 2002 with the support of both the ruling Bharatiya Janata Party and the then-opposition Indian National Congress. Widely referred to as the People\'s President, he returned to his civilian life of education, writing and public service after a single term. He was a recipient of several prestigious awards, including the Bharat Ratna, India\'s highest civilian honour.While delivering a lecture at the Indian Institute of Management Shillong, Kalam collapsed and died from an apparent cardiac arrest on 27 July 2015, aged 83.Thousands including national-level dignitaries attended the funeral ceremony held in his hometown of Rameshwaram, where he was buried with full state honours.")

def review_to_words( raw_review ):
    # 2. Remove non-letters
    letters_only = re.sub("[^a-zA-Z]", " ", raw_review)
    #
    # 3. Convert to lower case and split into individual words
    words = letters_only.lower().split()
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))
    #
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]
    #
    # 6. Join the words back into one string separated by space,
    # and return the result.
    return( " ".join( meaningful_words ))

clean_reviews = []

num_size=len(presidents)
for i in xrange(0,num_size):
	clean_reviews.append(review_to_words(presidents[i]))

#print clean_reviews

#feature_extraction-----------------------> term frequency
train_data_features=vectorizer.fit_transform(clean_reviews)

#take a look now on the vocabulary
vocab=vectorizer.get_feature_names()
print vocab

dist=np.sum(train_data_features.toarray(),axis=0)

for tag, count in zip(vocab, dist):
    print count, tag

#idf evaluated------------------>
tfidf.fit(train_data_features.toarray())

tf_idf_matrix = tfidf.transform(train_data_features.toarray())
print tf_idf_matrix.todense()

print tf_idf_matrix.shape

questions=[] 
questions.append("Who is Union Finance Minister?")
#questions.append("Who is the best actor in whole universe according to data?")

clean_questions=[]

num_sizes=len(questions)
for i in xrange(0,num_sizes):
    clean_questions.append(review_to_words(questions[i]))
#print clean_questions

train_question_features=vectorizer.transform(clean_questions)

print train_question_features.shape

#----------------------------------------------------------->>>>>
tfidf.fit(train_question_features.toarray())
tf_idf_matrix_question=tfidf.transform(train_question_features.toarray())
print tf_idf_matrix_question.shape

dist=np.sum(train_question_features.toarray(),axis=0)

for tag, count in zip(vocab, dist):
    print count, tag

cosine_value=[]
for i in xrange(0,num_size):
    cosine_value.append(cosine_similarity(tf_idf_matrix[i],train_question_features[0]))

#print cosine_value

z=tf_idf_matrix.dot(tf_idf_matrix_question.T)
print z.shape

index, value = max(enumerate(z), key=operator.itemgetter(1))
print presidents[index]