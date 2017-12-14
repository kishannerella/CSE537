import pickle as pkl
import numpy as np
import scipy as sp
from scipy import stats
from itertools import izip
from copy import deepcopy

#   scipy.stats.chisquare(f_obs, f_exp)
#
#   Args:
#       f_obs = [positive labels in v_1 of attribute, ..., positive labels in v_m of attribute,
#                  negative labels in v_1 of attribute, ..., negative labels in v_m of attribute]
#       f_exp = [positive label count / count of dataset * count of sub dataset, ...(m times), 
#                  negative label count / count of dataset * count of sub dataset, ...(m times)]
#       ddof = m - 1
#
#   Returns: (chisq, p)
#       chisq: The chi-squared test statistic.
#       p: The p-value of the test. -> compare this with the input p-value
#
#   ----------------------------------------------
#
#   scipy.stats.entropy(pk)
#   Args:
#       pk = [count of positive label, count of negative label]
#   Returns: entropy value
#   
class TreeNode():
    def __init__(self, data='T',children=[-1]*5):
        self.nodes = list(children)
        self.data = data


    def save_tree(self,filename):
        obj = open(filename,'w')
        pkl.dump(self,obj)
        
class ID3Node:
    
    def __init__(self):
        self.nodes = [-1]*5
        #self.nodes = {}
        self.attr_id = -1
        
        self.Leaf = False
        self.Label = None
        
    def set_attr(self, attr_id, vals):
        
        self.attr_id = attr_id
        for val in vals:
            self.nodes[val] = ID3Node()

class ID3Builder:

    def __init__(self, p_val, attr_vals):
        
        self.attributes_values = attr_vals
        self.confidence_level = p_val
        #return root
        
    def _get_best_attr(self, data, split_features):
        #print data
        """Find best attribute to split on"""
        best_attribute = -1
        max_information_gain = float("-inf")
        best_feature_info = []
        
        feature_max_val = 5
        features, label = data[0]
        sample_count = len(data)
        
        
        """
        If there is only one/no feature left to split, return None
        Returning None should take care of assigning the major label
        as leaf
        """
        if (len(split_features) >= len(features)-1):
            return None
        
        total_pos = 0
        total_neg = 0
        for f, l in data:
            if (l == 1):
                total_pos += 1
            else:
                total_neg += 1
        """
        If all the data has already been classified to the same value
        """
        if total_pos == 0 or total_neg == 0 :
            return None
        
        cur_inf = sp.stats.entropy([total_pos, total_neg])
        
        f,l = data[0]
        feat_count = []
        for i in range(len(f)):
            per_feat = []
            for j in range(0, feature_max_val):
                per_feat.append([0,0])
            feat_count.append(per_feat)
                
        for f,l in data:
            for i in range(len(f)):
                feat_count[i][f[i]-1][l] += 1
        
        for i in range(len(features)):
            if (i in split_features):
                continue
            #   TODO: compute information gain for this attribute
            """
            feature_tcount = []
            for j in range(0, feature_max_val):
                feature_tcount.append([0,0])

            for f, l in data:
                #print "f - " + str(f) + " f(i) - " + str(f[i]) + " l - " + str(l)
                feature_tcount[f[i]-1][l] += 1
            """
            feature_tcount = feat_count[i]
            future_inf = 0.0
            
            for j in range(0, feature_max_val):
                if (feature_tcount[j][0] + feature_tcount[j][1] > 0):
                    future_inf += ((feature_tcount[j][0] + feature_tcount[j][1])/(sample_count*1.0)) \
                                     * sp.stats.entropy([feature_tcount[j][1], feature_tcount[j][0]])
            information_gain = cur_inf - future_inf

            if max_information_gain < information_gain:
                max_information_gain = information_gain
                best_attribute = i
                best_feature_info = deepcopy(feature_tcount)
        
        if np.isclose(max_information_gain, 0.0):
            return None
        #print "max_information_gain - " + str(max_information_gain)
        #print "best_attribute - " + str(best_attribute)
        #   return None if attribute with max gain does not pass chi square test
        if not self._chi_square(best_attribute, data, best_feature_info, total_pos, total_neg):
            return None
            
        return best_attribute
        
    def build_tree_rec(self, root, data, split_features):
        """Build ID3 tree on root to classify data.
        
        Args:
            root (ID3Node): the root to build on.
            data (List): Training dataset,
                a list of tuples ( feature_values, label ).
        Returns:
            root (ID3Node): the root of built tree.
        """
        
        #if not self._stop():
        if (len(data) > 0):
            best_attr_id = self._get_best_attr(data, split_features)
            if best_attr_id:
                split_features.add(best_attr_id)            
                #attr_vals = self.attributes_values[ best_attr_id ]
                split_data = self._split_data_with_attr(best_attr_id, data)
                root.attr_id = best_attr_id
                #print split_data
                for i in range(5):
                    c_data = split_data[i]
                    #TODO : Change this to make some sense
                    if (len(c_data) == 0):
                        root.nodes[i] = ID3Node()
                        root.nodes[i].Leaf = True
                        root.nodes[i].Label = 1
                    else:
                        root.nodes[i] = ID3Node()
                        self.build_tree_rec(root.nodes[i], c_data, deepcopy(split_features))
            #   don't need to split, this is a leaf node
            else:
                #   TODO: find the majority label and put it to root
                pcount = 0
                ncount = 0
                for f,l in data:
                    if l == 1:
                        pcount+=1
                    else:
                        ncount+=1

                if (pcount > ncount):
                    major_label = 1
                else:
                    major_label = 0
                
                root.Leaf = True
                root.Label = major_label
                
        return root

    def _split_data_with_attr(self, attr, data):
        """Split data and remove according attribute"""
        
        split_data = [[],[],[],[],[]]
        
        for d in data:
            f,l = d
            
            split_data[f[attr]-1].append(d)
            
        return split_data
    
    def _chi_square(self, attr, data, feature_info, total_pos, total_neg):

        """Perform chi-square tests on every attribute"""
        if len(data) == 1:
            return False
        
        if np.isclose(self.confidence_level, 1.0):
            return True
        
        p_ratio = (total_pos*1.0)/(total_pos+total_neg)
        n_ratio = (total_neg*1.0)/(total_pos+total_neg)
        
        f_obs = []
        
        for i in range(5):
            f_obs.append(feature_info[i][1])
            
        for i in range(5):
            f_obs.append(feature_info[i][0])
        
        f_exp = []
        for i in range(5):
            f_exp.append(p_ratio*(feature_info[i][1]+feature_info[i][0]))
        
        for i in range(5):
            f_exp.append(n_ratio*(feature_info[i][1]+feature_info[i][0]))
                
        chisq, p_val = sp.stats.chisquare(f_obs, f_exp, 5-1)
        print f_obs
        print f_exp
        print chisq, p_val
        return p_val < self.confidence_level


class ID3Classifier:
    def __init__(self):
        self.tree = None
        self.builder = None
        self.data = []
        self.attributes_count = 0
        self.attributes_name_book = {}
        self.attributes_values = {}
    
    def add_attr_name(self, name):
        
        self.attributes_name_book[ self.attributes_count ] = name
        self.attributes_values[ self.attributes_count ] = [0, 1, 2, 3, 4]
        self.attributes_count += 1
    
    def add_data(self, label, feature_vals):
        
        """if len(feature_vals) != self.attributes_count:
            return
        """
        self.data.append( (feature_vals, label) )
    
    def build_tree(self, confidence_level):
        #print self.data
        #exit()
        self.tree = ID3Node()
        self.builder = ID3Builder(confidence_level, self.attributes_values)
        self.builder.build_tree_rec(self.tree, self.data, set([]))
        
    def test_data(self, feature_vals):
        """Traverse the tree on root.
        
        Args:
            feature_vals(List): the list of feature values in integer.
        
        Returns:
            label(str): the label to which this set of features are classified.
        """
        #   TODO: implement this function
        root = self.tree
        #print root
        while True:
            if root.Leaf:
                return root.Label
            else:
                root = root.nodes[feature_vals[root.attr_id]-1]
        
    def save_tree(self, filename):
        obj = open(filename,'w')
        pkl.dump(self.tree,obj)
        """save tree to file with pickle library"""
        #   TODO: implement this function,
        #       cast th tree to TA's format if needed
        
        
        
import sys
#   main function
if __name__ == "__main__":
        
    if len(sys.argv) != 11:
        print("Usage: python q1_classifier.py -p <pvalue> -f1 <train_dataset> -f2 <test_dataset> -o <output_file> -t <decision_tree>")
        exit()
        
    args = {}
    for i in range(1, 11, 2):
        args[ sys.argv[i] ] = sys.argv[i+1]
    
    train_file = ""
    label_file = ""
    test_file = ""
    output_file = ""
    decision_tree = ""
    p_val = 0.0
    if "-f1" in args:
        train_file = args["-f1"]
        tsplit = train_file.split('.')
        label_file = tsplit[0]
        for i in range(1, len(tsplit)-1):
	        label_file += "." + tsplit[i]
        label_file += "_label"
        label_file += "." + tsplit[len(tsplit)-1]
        #print label_file
    else:
        exit()
    if "-f2" in args:
        test_file = args["-f2"]
    else:
        exit()
    if "-o" in args:
        output_file = args["-o"]
    else:
        exit()
    if "-p" in args:
        p_val = float(args["-p"])
    else:
        exit()
    if "-t" in args:
        decision_tree = args["-t"]
    else:
        exit()

    id3_classifier = ID3Classifier()
    
    with open(train_file) as train_in, open(label_file) as label_in:
        for train_line, label_line in izip(train_in, label_in):
            tokens = [int(i) for i in train_line.split()]
            id3_classifier.add_data(int(label_line), tokens)
    
    id3_classifier.build_tree(p_val)	
    id3_classifier.save_tree(decision_tree)
    
    #TODO remove test_label
    with open(test_file) as test_in, open(output_file, "w+") as test_out, open("test_label.csv") as test_label_in:
        total_tests = 0
        correct_tests = 0
        for test_line, test_label_line in izip(test_in, test_label_in):
            tokens = [int(i) for i in test_line.split()]
            correct_label = int(test_label_line)
            decision_label = id3_classifier.test_data(tokens)
            
            total_tests += 1
            if correct_label == decision_label:
                correct_tests +=1
            test_out.write("{0}\n".format(decision_label))
        print correct_tests
        print("accuracy: {0}%".format(correct_tests * 1.0 / total_tests * 100))
            
            
    
