import pickle
import numpy as np
import scipy as sp

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

class ID3Classifier:

    class ID3Node:
        
        def __init__(self):
            
            self.children = {}
            self.attr_id = -1
            
            self.Leaf = False
            self.Label = None
            
        def set_attr(self, attr_id, vals):
            
            self.attr_id = attr_id
            for val in vals:
                self.children[val] = ID3Node()
    
    class ID3Builder:
    
        def __init__(self, p_val, attr_vals):
            
            self.attributes_values = attr_vals
            self.confidence_level = p_val
            
        def build_tree_rec(self, root, data):
            
            if not self._stop():
            
                best_attr_id = _get_best_attr(data)
                if best_attr_id:
                
                    attr_vals = self.attributes_values[ best_attr_id ]
                    split_data = self._split_data_with_attr(self, best_attr_id, attr_vals, data)
                    
                    for i in attr_vals:
                        c_data = split_data[i]
                        root.children[i] = self.build_tree_rec(root.children[i], c_data)
                #   don't need to split, this is a leaf node
                else:
                    #   TODO: find the majority label and put it to root
                    major_label = None
                    
                    root.Leaf = True
                    root.Label = major_label
                    
            return root
            
        def _get_best_attr(self, data):
            """Find best attribute to split on"""
            best_attributes = -1
            max_information_gain = float("-inf")
            
            features, label = data[0]
            
            for i in range(len(features)):
                #   TODO: compute information gain for this attribute
                information_gain = 0.0
                
            
            #   return None if attribute with max gain does not pass chi square test
            if not self._chi_square(best_attributes, data):
                return None
                
            return best_attributes
    
        def _split_data_with_attr(self, attr, vals, data):
            """Split data and remove according attribute"""
            
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
        
        def _chi_square(self, attr, data):
            """Perform chi-square tests on every attribute"""
            if len(data) == 1:
                return True
            
            #   TODO: fill in the implementation with scipy
            feature_vals, label = data[0]
            attr_cnt = len(feature_vals)
            for i in range(attr_cnt):
                
            
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
        
        if len(feature_vals) != self.attributes_count:
            return
        
        self.data.append( (feature_vals, label) )
    
    def build_tree(self, confidence_level):
        
        self.tree = ID3Node()
        self.builder = ID3Builder(confidence_level, self.attributes_values)
        self.tree = self.builder.build_tree_rec(self.tree, self.data)
        
    def test_data(self, feature_vals):
        """traverse the tree on root"""
        #   TODO: implement this function
        
    def save_tree(self, path):
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
		for i in range(0, len(tsplit)-1):
			label_file.append(tsplit[i])
		label_file.append("label")
		label_file.append(tsplit[len(tsplit)-1])
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
        output_file = args["-p"]
    else:
        exit()
    if "-t" in args:
        decision_tree = args["-t"]
    else:
        exit()
    exit()
    id3_classifier = ID3Classifier()
    
    with open(train_file) as train_in:
        for line in train_in:
            pass
            
            
    with open(test_file) as test_in, open(output_file, "w+") as test_out:
        for line in test_in:
            pass
            
    