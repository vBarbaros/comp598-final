import os
import json

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

parentdir = Path(__file__).parents[1]


def read_from_json(input_csv_file):
    in_file = os.path.join(parentdir, input_csv_file)
    json_content = None
    with open(in_file, 'r') as fh:
        json_content = json.load(fh)
    return json_content


def plot_stats_graph(x_values, y_values, x_label, y_label):
    plt.plot(x_values, y_values)
    plt.xlabel(x_label)
    plt.ylabel(y_label)


def plot_stats_bar(data, labels, x_label, y_label, title, xticks):
    fig, ax = plt.subplots()
    x = np.arange(len(xticks))
    rects1 = ax.bar(x + 0.00, data[0], color='b', width=0.25, label=labels[0])
    rects2 = ax.bar(x + 0.25, data[1], color='g', width=0.25, label=labels[1])
    rects3 = ax.bar(x + 0.50, data[2], color='r', width=0.25, label=labels[2])

    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(x, xticks)
    ax.legend()

    ax.bar_label(rects1, padding=2)
    ax.bar_label(rects2, padding=2)
    ax.bar_label(rects3, padding=2)

    fig.savefig('plots/' + title + '.png')


def generate_simple_pie_plot(labels, sizes, explode, title):
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.2f%%',
           shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set(aspect="equal", title=title)
    fig.savefig('plots/PIE_PLOT_' + title + '.png')


def generate_tfidf_bar_plot(tfidf_vals, words, label_name):
    plt.rc('ytick', labelsize=11)  # fontsize of the tick labels
    fig, ax = plt.subplots()

    y_pos = np.arange(len(tfidf_vals))
    title = 'Top ' + str(len(words)) + ' words for the label - [' + label_name + ']'
    rect = ax.barh(y_pos, tfidf_vals, align='center')
    ax.set_yticks(y_pos, words)
    ax.invert_yaxis()
    ax.set_xlabel('TF-IDF Values')
    ax.set_title(title)
    ax.bar_label(rect, padding=2)
    plt.xlim((-1, max(tfidf_vals) + 5))
    plt.show()
    fig.savefig('plots/TFIDF_PLOT_' + title + '.png')


if __name__ == '__main__':
    pass
