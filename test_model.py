#! /usr/bin/env python

"""
Created on Sun May  1 08:22:04 2016

@author: rahulkumar
"""

import tensorflow as tf
import numpy as np
import corpus_handel

#Corpus builder
#=====================================================
new_question = "What is the date of Boxing Day ?"
new_question = new_question.strip()
new_question = corpus_handel.clean_str(new_question)
new_question = new_question.split(" ")


sentences, dump = corpus_handel.load_data_and_labels()
sequence_length = max(len(x) for x in sentences)
sentences_padded = corpus_handel.pad_sentences(sentences)
vocabulary, vocabulary_inv = corpus_handel.build_vocab(sentences_padded)

num_padding = sequence_length - len(new_question)
new_sentence = new_question + ["<PAD/>"] * num_padding



x = np.array([vocabulary[word] for word in new_sentence])
x_test = np.array([x])


# Evaluation
# ==================================================
checkpoint_file = tf.train.latest_checkpoint('/Users/rahulkumar/Desktop/m_classifier/runs/1462124004/checkpoints/')
graph = tf.Graph()
with graph.as_default():
    session_conf = tf.ConfigProto(
      allow_soft_placement=True,
      log_device_placement=False)
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        # Load the saved meta graph and restore variables
        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
        saver.restore(sess, checkpoint_file)

        # Get the placeholders from the graph by name
        input_x = graph.get_operation_by_name("input_x").outputs[0]
        # input_y = graph.get_operation_by_name("input_y").outputs[0]
        dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

        # Tensors we want to evaluate
        predictions = graph.get_operation_by_name("output/predictions").outputs[0]

        # Generate batches for one epoch
        batches = corpus_handel.batch_iter(x_test, 30, 1, shuffle=False)

        # Collect the predictions here
        all_predictions = []

        for x_test_batch in batches:
            batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
            print batch_predictions            
            all_predictions = np.concatenate([all_predictions, batch_predictions])
#            print all_predictions
            
            
if(all_predictions[0] == 0):
    print 'Who'
elif(all_predictions[0] == 1):
    print 'When'
elif(all_predictions[0] == 2):
    print 'What'
else:
    print 'Unknown'
