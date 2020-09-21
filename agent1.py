import tensorflow as tf
import numpy as np
import random

size_x = [840, 128, 3]

data_location = './match.npy'

class agent1:
    def BuildNetwork(self):
        self.n = len(size_x)
        
        self.x = [ tf.placeholder(tf.float32, [None, size_x[0]]) ]
        self.w = [ ]
        self.b = [ ]
        self.z = [ ]
        for i in range(1, self.n):
            n0, n1 = size_x[i-1], size_x[i]
            self.w.append( tf.Variable( tf.random_normal([n0, n1]) / np.sqrt(n0) ) )
            self.b.append( tf.Variable( tf.random_normal([n1]) ) )
            self.z.append( tf.matmul(self.x[i-1], self.w[i-1]) + self.b[i-1] )
            if i == self.n-1:
                self.x.append( tf.nn.softmax(self.z[i-1]) )
            else:
                self.x.append( tf.sigmoid(self.z[i-1]) )
        
        self.y = tf.placeholder(tf.float32, [None, size_x[self.n-1]])
        
        self.cross_entropy_loss = tf.nn.softmax_cross_entropy_with_logits_v2(labels = self.y, logits = self.z[self.n-2])
        self.l2_reg_loss = tf.nn.l2_loss(self.w[0]) + tf.nn.l2_loss(self.w[1])
        
        self.loss = self.cross_entropy_loss + (0.001 * self.l2_reg_loss)
        
        self.saver = tf.train.Saver()
        self.train = tf.train.GradientDescentOptimizer(0.005).minimize(self.loss)
        
        self.accuracy = tf.reduce_mean(tf.abs(self.y - self.x[self.n-1]))
    
    def ExecPosition(self, input_pos, save_loc):
        input_pos = [ input_pos ]
        with tf.Session() as sess:
            self.saver.restore(sess, save_loc)
            output = sess.run(self.x[self.n-1], feed_dict = {self.x[0] : input_pos })
        return output[0]
    
    def InitializeAndSave(self, save_loc):
        with tf.Session() as sess:
            tf.global_variables_initializer().run()
            self.saver.save(sess, save_loc)
    
    def TrainNetwork(self, save_loc):
        data = np.load(data_location)
        
        state = np.asarray([ x for x, y in data])
        sol = np.asarray([ y for x, y in data])
        
        with tf.Session() as sess:
            self.saver.restore(sess, save_loc)
            for i in range(1000):
                print "Epoch: ", i+1
                
                data = zip(state,sol)
                random.shuffle(data)
                
                state = np.asarray([ x for x, y in data])
                sol = np.asarray([ y for x, y in data])
                
                batch_size = 10
                for k in range(0, len(data), batch_size):
                    start = k*batch_size
                    finish = min((k+1)*batch_size, len(data))
                    sess.run(self.train, feed_dict = {self.x[0] : state[start:finish], self.y : sol[start:finish]})
                
                acc_val = 100.0*(1.0-sess.run(self.accuracy, feed_dict = {self.x[0] : state, self.y : sol}))
                l = tf.reduce_mean(self.cross_entropy_loss)
                l_val = sess.run(l, feed_dict = {self.x[0] : state, self.y : sol})
                print "Loss: ", l_val
                print "Accuracy: ", acc_val
                
                if acc_val > 90.0:
                    self.saver.save(sess, save_loc)
                    break
            
