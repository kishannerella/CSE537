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
        print data
        """Find best attribute to split on"""
        best_attribute = -1
        max_information_gain = float("-inf")
        
        feature_max_val = 5
        features, label = data[0]
        sample_count = len(data)
        
        total_pos = 0
        total_neg = 0
        
        for f, l in data:
            if (l == 1):
                total_pos += 1
            else:
                total_neg += 1
        
        if total_pos == 0 or total_neg == 0 :
            return None
        
        cur_inf = sp.stats.entropy([total_pos, total_neg])
        
        for i in range(len(features)):
            if (i in split_features):
                continue
            #   TODO: compute information gain for this attribute
            feature_tcount = []
            for j in range(0, feature_max_val+1):
                feature_tcount.append([0,0])

            for f, l in data:
                #print "f - " + str(f) + " f(i) - " + str(f[i]) + " l - " + str(l)
                feature_tcount[f[i]][l] += 1
            
            future_inf = 0.0
            #print "feature_count " + str(feature_tcount)
            
            for j in range(1, feature_max_val+1):
                #print "feature_count[j] " + str(feature_tcount[j])
                if (feature_tcount[j][0] + feature_tcount[j][1] > 0):
                    future_inf += ((feature_tcount[j][0] + feature_tcount[j][1])/(sample_count*1.0)) \
                                     * sp.stats.entropy([feature_tcount[j][1], feature_tcount[j][0]])
            information_gain = cur_inf - future_inf
            #print "i1  " +  str(((feature_tcount[j][0] + feature_tcount[j][1])/(sample_count*1.0)))
            #print "i2  " +  str(sp.stats.entropy([feature_tcount[j][1], feature_tcount[j][0]]))
            #print "information gain  - " + str(information_gain)
            if max_information_gain < information_gain:
                max_information_gain = information_gain
                best_attribute = i
        
        print "max_information_gain - " + str(max_information_gain)
        print "best_attribute - " + str(best_attribute)
        #   return None if attribute with max gain does not pass chi square test
        if not self._chi_square(best_attribute, data):
            return None
            
        return best_attribute
        
    def build_tree_rec(self, root, data, split_features):
        
        #if not self._stop():
        if (len(data) > 0):
            best_attr_id = self._get_best_attr(data, split_features)
            if best_attr_id:
                split_features.add(best_attr_id)            
                #attr_vals = self.attributes_values[ best_attr_id ]
                split_data = self._split_data_with_attr(best_attr_id, data)
                print split_data
                for i in range(5):
                    c_data = split_data[i]
                    if (len(c_data) == 0):
                        root.nodes[i] = -1
                    else:
                        root.nodes[i] = ID3Node()
                        self.build_tree_rec(root.nodes[i], c_data, deepcopy(split_features))
            #   don't need to split, this is a leaf node
            else:
                #   TODO: find the majority label and put it to root
                pcount = 0
                ncount = 0
                for d in data:
                    if d[1] == 1:
                        pcount+=1
                    else:
                        ncount+=1

                if (pcount > ncount):
                    major_label = 1
                else:
                    major_label = 0
                
                root.Leaf = True
                root.Label = major_label
                

    def _split_data_with_attr(self, attr, data):
        """Split data and remove according attribute"""
        
        split_data = [[],[],[],[],[]]
        
        for d in data:
            f,l = d
            
            split_data[f[attr]-1].append(d)
            
        return split_data
        """
        feature_vals, label = data[0]
        attr_is_first = attr == 0
        attr_is_last = attr == (len(feature_vals) - 1)
        
        ret_dict = {}
        idx = 0
        #   vals are sorted
        for val in vals:
            ret_dict[val] = []
        
        for feature_vals, label in data:
            val = feature_vals[attr]
            new_feature_vals = []
            if not attr_is_first:
                new_feature_vals.append(feature_vals[:attr-1])
            if not attr_is_last:
                new_feature_vals.append(feature_vals[attr+1:])
            ret_dict[val].append( (new_feature_vals, label) )
            
        return ret_dict
        """
    
    def _chi_square(self, attr, data):
        return True;
        """Perform chi-square tests on every attribute"""
        if len(data) == 1:
            return True
        
        #   TODO: fill in the implementation with scipy
        feature_vals, label = data[0]
        attr_cnt = len(feature_vals)
        for i in range(attr_cnt):
            pass


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
        self.attributes_values[ self.attributes_count ] = [1, 2, 3, 4, 5]
        self.attributes_count += 1
    
    def add_data(self, label, feature_vals):
        
        """if len(feature_vals) != self.attributes_count:
            return
        """
        self.data.append( (feature_vals, label) )
    
    def build_tree(self, confidence_level):
        print self.data
        #exit()
        self.tree = ID3Node()
        self.builder = ID3Builder(confidence_level, self.attributes_values)
        self.tree = self.builder.build_tree_rec(self.tree, self.data, set([]))
        
    def test_data(self, feature_vals):
        """traverse the tree on root"""
        #   TODO: implement this function
        
    def save_tree(self, filename):
        obj = open(filename,'w')
        pkl.dump(self,obj)
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
        print label_file
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
    with open(test_file) as test_in, open(output_file, "w+") as test_out:
        for line in test_in:
            pass
            
    
