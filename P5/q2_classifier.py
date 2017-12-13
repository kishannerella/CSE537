import re
import math

class NaiveBayesSpamClassifier:
    """Naive Bayes Spam Classifier with Laplace smoothing.
    
    When training the classifier, call add_train_data
    for multiple times to feed in labels and data, then
    call finish_training to sum training results up into
    a dictionary of Bayesian estimates for each word.
    
    """
    class SpecialRules:
        """A class for remapping words to string with regular expressions.
        
        The matching of rule is done sequentially w.r.t.
        the order in which the rules are added to the class.
            
        ***This does not do better than smoothing***
        
        """
        def __init__(self):
            self.all_res = []
            self.map_to = {}
            
        def add_rule(self, reg, str):
            """Add rule to this handler.
            
            Args:
                reg (str): The rule in regular expression.
                str (str): The string to which matched input should be remapped.
            """
            new_re = re.compile(reg)
            self.all_res.append(new_re)
            self.map_to[new_re] = str
        
        def remap(self, str):
            """Retern remapped string of input string.
                
            Reterns:
                remapped_str (str): remapped string.
            """
            for regexp in self.all_res:
                if regexp.match(str):
                    return self.map_to[regexp]
            return str
            
    def __init__(self):
        """Inits NaiveBayesSpamClassifier, no parameter is needed."""
        self.all_words = {}
        self.spam_dict = {}
        self.ham_dict = {}
        self.log_prob_dict = {}
        
        self.ham_cnt = 0
        self.spam_cnt = 0
        
        self.default_logp_ham = 0.0
        self.default_logp_spam = 0.0
        
        # self.rule_handler.add_rule("^[0-9]{,3}$", "000")
        # self.rule_handler.add_rule("^(0[0-9]|1[0-9]|2[0-3])[0-5][0-9]$", "0000")
        # self.rule_handler.add_rule("^[0-9,]{4,}$", "00000")
        
    def add_train_data(self, is_spam, tokens):
        """Counts the appearance of each word in spam and ham.
        
        This function can be called multiple times, each call
        processes a line of training data with its label.
        The length of tokens must be greater than zero and
        must be an even number. Otherwise this function will
        return with no effect.

        Args:
            is_spam (bool): True if this line of training data should be
                classified as spam, False otherwise.
            tokens (str): A list of features and feature counts.
                Must be in the format:
                [feature_1, feature_count_1, ..., feature_n, feature_count_n]
        """
        token_cnt = len(tokens)
        if token_cnt == 0 or token_cnt % 2 != 0:
            return
            
        if is_spam:
            self.spam_cnt += 1
        else:
            self.ham_cnt += 1
            
        for i in range(0, len(tokens), 2):
            word = tokens[i]
            word_cnt = int(tokens[i+1])
            
            self.all_words[word] = ""
            if is_spam:
                if word in self.spam_dict:
                    self.spam_dict[ word ] += word_cnt
                else:
                    self.spam_dict[ word ] = word_cnt
            else:
                if word in self.ham_dict:
                    self.ham_dict[ word ] += word_cnt
                else:
                    self.ham_dict[ word ] = word_cnt
        
    def finish_training(self, smoothing=1):
        """Sum up the statistics from add_train_data and fill up self.log_prob_dict.
        
        This function should only be called after every line
        of data is processed by add_train_data. It can be called
        multiple times, each call clears self.log_prob_dict and
        again fill it up with Bayesian estimates with Laplace smoothing
        parameter corresponding to the smoothing argument.
        
        Args:
            smoothing (int): The value of Laplace smoothing parameter.
        """
        s = smoothing * 1.0
        all_ham = self.ham_cnt
        all_spam = self.spam_cnt
        vocab_cnt = len(self.all_words)
        
        self.default_logp_ham = math.log(s / (all_ham + s * vocab_cnt + s))
        self.default_logp_spam = math.log(s / (all_spam + s * vocab_cnt + s))
        
        self.log_prob_dict = {}
        for word in self.all_words:
            
            cnt_ham = s
            cnt_spam = s
            if word in self.ham_dict:
                cnt_ham += self.ham_dict[word]
            if word in self.spam_dict:
                cnt_spam += self.spam_dict[word]
            
            p_ham = cnt_ham / (all_ham + s * vocab_cnt + s)
            p_spam = cnt_spam / (all_spam + s * vocab_cnt + s)
            
            self.log_prob_dict[word] = (math.log(p_ham), math.log(p_spam))
    
    def test_spam(self, tokens):
        """Return the classification result of input features.
        
        The length of tokens must be greater than zero and
        must be an even number.
        
        Args:
            tokens (str): A list of features and feature counts.
                Must be in the format:
                [feature_1, feature_count_1, ..., feature_n, feature_count_n]
        Returns:
            None if argument is invalid.
            True if input features are classified as spam.
            False if input features are classified as ham.
        """
        token_cnt = len(tokens)
        if token_cnt == 0 or token_cnt % 2 != 0:
            return None
            
        logp_ham = 0.0
        logp_spam = 0.0
        
        for i in range(0, token_cnt, 2):
            word = tokens[i]
            cnt = int(tokens[i+1])
            
            if word in self.log_prob_dict:
                word_logp_ham, word_logp_spam =  self.log_prob_dict[word]
                
                for j in range(0, cnt):
                    logp_ham +=  word_logp_ham
                    logp_spam += word_logp_spam
            else:
                logp_ham += self.default_logp_ham
                logp_spam += self.default_logp_spam
        
        return logp_spam > logp_ham
    
    def clear(self):
        """Reset all dictionaries used in this class."""
        self.all_words.clear()
        self.ham_dict.clear()
        self.spam_dict.clear()
        self.log_prob_dict.clear()

import sys
#   main function
if __name__ == "__main__":
    
    if len(sys.argv) != 7:
        print("Usage: python q2_classifier.py -f1 <train_dataset> -f2 <test_dataset> -o <output_file>")
        exit()
        
    args = {}
    for i in range(1, 7, 2):
        args[ sys.argv[i] ] = sys.argv[i+1]
    
    train_file = ""
    test_file = ""
    output_file = ""
    if "-f1" in args:
        train_file = args["-f1"]
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

    nbsc = NaiveBayesSpamClassifier()
    
    with open(train_file) as train_in:
        for line in train_in:

            tokens = line.split()
            token_cnt = len(tokens)
            if token_cnt < 2 or token_cnt % 2 != 0:
                continue
            is_spam = (tokens[1] == "spam")
            
            nbsc.add_train_data(is_spam, tokens[2:])

    nbsc.finish_training(80)
        
    with open(test_file) as test_in, open(output_file, "w+") as test_out:

        total_tests = 0
        correct_tests = 0

        for line in test_in:

            tokens = line.split()
            token_cnt = len(tokens)
            if token_cnt < 2 or token_cnt % 2 != 0:
                continue
            
            id = tokens[0]
            is_spam = nbsc.test_spam(tokens[2:])
            
            is_spam_ans = (tokens[1] == "spam")
            
            if is_spam == is_spam_ans:
                correct_tests = correct_tests + 1
            total_tests = total_tests + 1
            
            str = "spam" if is_spam else "ham"
            test_out.write("{0},{1}\n".format(id, str))

        print("accuracy: {0}%".format(correct_tests * 1.0 / total_tests * 100))