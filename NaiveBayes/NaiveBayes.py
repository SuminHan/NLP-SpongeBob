import io
import numpy
import matplotlib as mpl
import nltk

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import re
import math

special_chars_remover = re.compile("[^\w'|_]")
characters = ["Gary", "Mr.Krabs", "Patrick", "Sandy", "SpongeBob", "Squidward"]
stpwd = nltk.corpus.stopwords.words('english')

def remove_special_characters(sentence):
    return special_chars_remover.sub(' ', sentence)


def main():
    training_sentences = read_data()
    # Put the text for the testing_sentence.
    #testing_sentence = "I love my job at the Krusty Krab, I like Jelly-Fishing and Bubble-Blowing. I've never been late for work!"
    testing_sentence = "I hate this job. I want to go home and play clarinet"
    prob_list = naive_bayes(training_sentences, testing_sentence)

    for i in range(len(characters)):
        print (characters[i] + ": " + str(prob_list[i]))

    plot_title = testing_sentence
    if len(plot_title) > 50: plot_title = plot_title[:50] + "..."
    visualize_boxplot(plot_title,
                      prob_list,
                      characters)


def naive_bayes(training_sentences, testing_sentence):
    log_probs = []
    for char in characters:
        log_probs.append(calculate_doc_prob(training_sentences[char], testing_sentence, 0.1) + math.log(0.5))
    prob_pair = normalize_log_prob(log_probs)

    return prob_pair


def read_data():
    training_sentences = {}
    for char in characters:
        mlist = []
        with open(char + ".txt") as f:
            for line in f:
                line = line.strip()
                mlist.append(line)
        training_sentences[char] = ' '.join(mlist)

    return training_sentences


def normalize_log_prob(probs):
    '''
    normalizing the log based probability code
    '''

    maxprob = max(probs)

    probs = [math.exp(p - maxprob) for p in probs]

    normalize_constant = 1.0 / float(sum(probs))
    probs = [p * normalize_constant for p in probs]

    return probs


def calculate_doc_prob(training_sentence, testing_sentence, alpha):
    logprob = 0

    training_model = create_BOW(training_sentence)
    testing_model = create_BOW(testing_sentence)

    '''
    Calculating the probability that training_model may produce testing_model.
    We use math.log, so note the use.
    예) 3 * 5 = 15
        log(3) + log(5) = log(15)

        5 / 2 = 2.5
        log(5) - log(2) = log(2.5)
    '''
    tot = 0
    for word in training_model:
        tot += training_model[word]

    for word in testing_model:
        if word in training_model:
            logprob += math.log(training_model[word])
            logprob -= math.log(tot)
        else:
            logprob += math.log(alpha)
            logprob -= math.log(tot)
    # log_prob = math.log(prob)
    return logprob


def create_BOW(sentence):
    bow = {}
    sentence = remove_special_characters(sentence)
    sentence = sentence.lower()
    tokens = nltk.word_tokenize(sentence)

    for word in tokens:
        if len(word) < 1 or word in stpwd: continue
        word = word.lower()
        bow.setdefault(word, 0)
        bow[word] += 1
    return bow

def remove_special_characters(sentence):
    return special_chars_remover.sub(' ', sentence)

'''
Code below is for visualization
'''

def visualize_boxplot(title, values, labels):
    width = .35

    print(title)

    fig, ax = plt.subplots()
    ind = numpy.arange(len(values))
    rects = ax.bar(ind, values, width)
    ax.bar(ind, values, width=width)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(labels)

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., height + 0.01, '%.2lf%%' % (height * 100), ha='center',
                    va='bottom')

    autolabel(rects)

    plt.savefig("image.svg", format="svg")


if __name__ == "__main__":
    # elice_utils.send_file("./ratings.txt")
    main()
