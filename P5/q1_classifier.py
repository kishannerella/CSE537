import pickle as pkl
import numpy as np
import scipy as sp
from scipy import stats
from itertools import izip
from copy import deepcopy

#
#   scipy.stats.entropy(pk)
#   Args:
#       pk = [count of positive label, count of negative label]
#   Returns: entropy value
#   
total_node_count = 0
class TreeNode():
    def __init__(self, data='T',children=[-1]*5):
        self.nodes = list(children)
        self.data = data


    def save_tree(self,filename):
        obj = open(filename,'w')
        pkl.dump(self,obj)

class ID3Builder:

    def __init__(self, p_val):
        self.confidence_level = p_val
        
    def _get_best_attr(self, data, split_features):
        """Find best attribute to split on
        
        Args:
            data (List): dataset at this current node,
                a list of tuples ( feature_values, label ).
            split_features : features on which the data is already split
        Returns:
            best_attr (int): the best attribute to split on
        """
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
        
        """
        Store all the feature counts in a 3D array
        """
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
            """ If we had already split this feature, skip it"""
            if (i in split_features):
                continue
            
            """Get the feature counts of the current feature"""
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

        if not self._chi_square(best_feature_info, total_pos, total_neg):
            return None
            
        return best_attribute
        
    def build_tree_rec(self, root, data, split_features):
        global total_node_count
        """Build ID3 tree on root to classify data.
        
        Args:
            root (ID3Node): the root to build on.
            data (List): Training dataset,
                a list of tuples ( feature_values, label ).
        Returns:
            root (ID3Node): the root of built tree.
        """
        
        if (len(data) > 0):
            best_attr_id = self._get_best_attr(data, split_features)
            if best_attr_id:
                split_features.add(best_attr_id)
                split_data = self._split_data_with_attr(best_attr_id, data)
                root.data = best_attr_id+1

                for i in range(5):
                    c_data = split_data[i]
                    if (len(c_data) == 0):
                        total_node_count+=1
                        root.nodes[i] = TreeNode()
                        root.nodes[i].data = 'F'
                    else:
                        total_node_count+=1
                        root.nodes[i] = TreeNode()
                        self.build_tree_rec(root.nodes[i], c_data, deepcopy(split_features))
            #   don't need to split, this is a leaf node
            else:
                pcount = 0
                ncount = 0
                for f,l in data:
                    if l == 1:
                        pcount+=1
                    else:
                        ncount+=1

                if (pcount > ncount):
                    major_label = 'T'
                else:
                    major_label = 'F'
                
                root.data = major_label
                
        return root

    def _split_data_with_attr(self, attr, data):
        """Split data and remove according attribute
        
        Args:
            attr (int): the feature to split on
            data (List): dataset at this current node,
                a list of tuples ( feature_values, label ).
        Returns:
            split_data (List): a list of data sets split on attr.
        """
        split_data = [[],[],[],[],[]]
        
        for d in data:
            f,l = d
            split_data[f[attr]-1].append(d)
            
        return split_data
    
    def _chi_square(self, feature_info, total_pos, total_neg):

        """Perform chi-square tests on every attribute
        
        Args:
            feature_info (List): count of positive and negative labels
                           indexed on feature value
            total_pos (int): total positive labels in the current dataset
            total_neg (int): total negative labels in the current dataset
                
        Returns:
            T/F (Boolean): return whether chisquare test is passed or not
        """
        if total_pos + total_neg == 1:
            return False
        
        if np.isclose(self.confidence_level, 1.0):
            return True
        
        p_ratio = (total_pos*1.0)/(total_pos+total_neg)
        n_ratio = (total_neg*1.0)/(total_pos+total_neg)
        
        """
        Calculate S value according to the formula
        """
        S_val = 0.0
        ddof = 0
        for i in range(5):
            t_i = feature_info[i][1]+feature_info[i][0]
            exp_p = p_ratio*t_i
            exp_n = n_ratio*t_i
            obs_p = feature_info[i][1]
            obs_n = feature_info[i][0]
            
            if t_i > 0:
                ddof += 1
                
            if exp_p > 0:
                S_val += pow(exp_p-obs_p, 2)/(exp_p*1.0)
            if exp_n > 0:
                S_val += pow(exp_n-obs_n, 2)/(exp_n*1.0)
        
        p_val = 1 - sp.stats.chi2.cdf(S_val, ddof)
        return p_val < self.confidence_level


class ID3Classifier:
    def __init__(self):
        self.tree = None
        self.builder = None
        self.data = []
    
    def add_data(self, label, feature_vals):
        self.data.append( (feature_vals, label) )
    
    def build_tree(self, confidence_level):
        global total_node_count
        total_node_count+=1
        self.tree = TreeNode()
        self.builder = ID3Builder(confidence_level)
        self.builder.build_tree_rec(self.tree, self.data, set([]))
        
        
    def test_data(self, feature_vals):
        """Traverse the tree on root.
        
        Args:
            feature_vals(List): the list of feature values in integer.
        
        Returns:
            label(str): the label to which this set of features are classified.
        """
        
        root = self.tree
        while True:
            if root.data == 'T':
                return 1
            elif root.data == 'F':
                return 0
            else:
                root = root.nodes[feature_vals[root.data-1]-1]
        
    def save_tree(self, filename):
        self.tree.save_tree(filename)
        
        
        
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
    p_val = 1.0
    if "-f1" in args:
        train_file = args["-f1"]
        tsplit = train_file.split('.')
        label_file = tsplit[0]
        for i in range(1, len(tsplit)-1):
	        label_file += "." + tsplit[i]
        label_file += "_label"
        label_file += "." + tsplit[len(tsplit)-1]
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
    
        for test_line in test_in:
            tokens = [int(i) for i in test_line.split()]
            decision_label = id3_classifier.test_data(tokens)

            test_out.write("{0}\n".format(decision_label))
        print "Total Nodes: {0}".format(total_node_count)
    
    
    #TODO remove test_label
    """
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
        print "Total Nodes: {0}".format(total_node_count)
        print("accuracy: {0}%".format(correct_tests * 1.0 / total_tests * 100))
    """
            
            
    
