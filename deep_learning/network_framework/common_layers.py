INITIALIZER_CONV = tf.contrib.layers.xavier_initializer()
INITIALIZER_BIAS = tf.constant_initializer(0.0)

def _leaky_relu(self):
    return lambda x: tf.maximum(0.2 * x, x)

def conv2d(x, kernel_shape, strides=1, activation=lambda x: tf.maximum(0.1 * x, x), padding='SAME', name='conv', reuse=False, wName='weights', bName='bias', batch_norm=False, training=False):
    with tf.variable_scope(name, reuse=reuse):
        W = tf.get_variable(wName, kernel_shape, initializer=INITIALIZER_CONV)
        b = tf.get_variable(bName, kernel_shape[3], initializer=INITIALIZER_BIAS)
        x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding=padding)
        x = tf.nn.bias_add(x, b)
        if batch_norm:
            x = tf.layers.batch_normalization(x,training=training,momentum=0.99)
        x = activation(x)
        return x