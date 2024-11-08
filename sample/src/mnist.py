import keras
from sklearn.model_selection import train_test_split

from core.src.convertor import convert

if __name__ == "__main__":
    (X_train_full, y_train_full), (X_test, y_test) = keras.datasets.mnist.load_data()

    X_train, X_valid, y_train, y_valid = train_test_split(
        X_train_full, y_train_full, test_size=0.1, random_state=1)

    X_train, X_valid, X_test = X_train / 255., X_valid / 255., X_test / 255.

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=[28, 28]),
        keras.layers.Dense(512, activation="softmax"),
    ])

    topology = convert(model)
    print(topology.to_json())

    # model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.05),
    #               loss="sparse_categorical_crossentropy",
    #               metrics=["accuracy"])
    #
    # model.fit(X_train_full, y_train_full, batch_size=32, epochs=1)
    #
    # test_loss, test_accuracy = model.evaluate(X_test, y_test)

    # print(model.layers)
    # print(model.summary())
