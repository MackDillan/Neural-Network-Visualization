import keras
import numpy as np

from core.src.convertor import convert


def create_xor_model():   
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    model = keras.Sequential([
        keras.layers.Input(shape=(2,)),
        keras.layers.Dense(2, activation='sigmoid', kernel_initializer=keras.initializers.Zeros()),
        keras.layers.Dense(1, activation='sigmoid', kernel_initializer=keras.initializers.Ones()),
    ])

    model.compile(loss='mse', optimizer='adam')
    model.fit(X, y, epochs=1, verbose=1)


if __name__ == "__main__":

    model = create_xor_model()
    topology = convert(model)
    print(topology.to_dict())
    # model.fit(X, y, epochs=1_000, verbose=1)

    #topology = convert(model)
    #print(topology.to_json())
    #
    # # model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.05),
    # #               loss="sparse_categorical_crossentropy",
    # #               metrics=["accuracy"])
    # #
    # # model.fit(X_train_full, y_train_full, batch_size=32, epochs=1)
    # #
    # # test_loss, test_accuracy = model.evaluate(X_test, y_test)
    #
    # # print(model.layers)
    # print(model.summary())
