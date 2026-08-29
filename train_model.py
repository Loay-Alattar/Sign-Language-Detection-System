import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

data_dict = pickle.load(open('./data.pickle', 'rb'))

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

x_train, x_test, y_train, y_test = train_test_split(
    data, labels,
    test_size=0.2,
    shuffle=True,
    stratify=labels,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=500,        # عدد الأشجار (أفضل قيمة)
    max_depth=30,           # يمنع الـ overfitting
    min_samples_split=4,
    min_samples_leaf=2,
    class_weight='balanced',
    bootstrap=True,
    random_state=42,
    n_jobs=-1               # يستخدم كل أنوية المعالج
)

model.fit(x_train, y_train)

y_predict = model.predict(x_test)
score = accuracy_score(y_predict, y_test)

print(f'{score * 100:.2f}% accuracy')

with open('model.p', 'wb') as f:
    pickle.dump({'model': model}, f)