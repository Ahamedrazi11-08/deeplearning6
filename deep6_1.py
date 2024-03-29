from keras.layers import Input, Dense
from keras.models import Model
from keras.callbacks import TensorBoard
from keras import regularizers

# this is the size of our encoded representations
encoding_dim = 32  # 32 floats

# this is our input placeholder
input_img = Input(shape=(784,))

encoded1 = Dense(128, activation='relu')(input_img)

# encoded representation of the input
encoded2 = Dense(encoding_dim, activation='relu', activity_regularizer=regularizers.l1(1e-7))(encoded1)

# lossy reconstruction of the input
decoded = Dense(128, activation='sigmoid')(encoded2)
decoded2 = Dense(784, activation='sigmoid')(decoded)

# this model maps an input to its reconstruction
autoencoder = Model(input_img, decoded2)

# # this model maps an input to its encoded representation
# encoder = Model(input_img, encoded1)

# # create a placeholder for an encoded (32-dimensional) input
# encoded_input = Input(shape=(encoding_dim,))

# # retrieve the last layer of the autoencoder model
# decoder_layer = autoencoder.layers[-1]

# # create the decoder model
# decoder = Model(encoded_input, decoder_layer(encoded_input))
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy',metrics=['accuracy'])

from keras.datasets import mnist
import matplotlib.pyplot as plt
import numpy as np
(x_train, _), (x_test, _) = mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

tensorboard = TensorBoard(log_dir='1', histogram_freq=0, write_graph=True, write_images=False)
history=autoencoder.fit(x_train, x_train, epochs=22, batch_size=1024, shuffle=True, validation_data=(x_test, x_test),callbacks=[tensorboard])
pred=autoencoder.predict(x_test)
plt.imshow(pred[0].reshape(28,28))
plt.show()
# # encode and decode some digits
# # note that we take them from the test set
# encoded_imgs = encoder.predict(x_test)
# decoded_imgs = decoder.predict(encoded_imgs)


# import matplotlib.pyplot as plt

# n = 10  # how many digits we will display
# plt.figure(figsize=(20, 4))
# for i in range(n):
#     # display original
#     ax = plt.subplot(2, n, i + 1)
#     plt.imshow(x_test[i].reshape(28, 28))
#     plt.gray()
#     ax.get_xaxis().set_visible(False)
#     ax.get_yaxis().set_visible(False)

#     # display reconstruction
#     ax = plt.subplot(2, n, i + 1 + n)
#     plt.imshow(decoded_imgs[i].reshape(28, 28))
#     plt.gray()
#     ax.get_xaxis().set_visible(False)
#     ax.get_yaxis().set_visible(False)
# plt.show()


# # Saving the model
# model_json = autoencoder.to_json()
# with open("model.json", "w") as json_file:
#     json_file.write(model_json)

# # serialize weights to HDF5
# autoencoder.save_weights("model.h5")