import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dict1 = {}
    corp = corpus[page]

    len_corp = len(corp)
    pages = corpus.keys()
    len_pages = len(pages)
    if len_corp==0:
        for i in pages:
            dict1[i] = 1/ len_pages
    else:
        for i in pages:
            if i in corp:
                dict1[i] = damping_factor/len_corp + (1-damping_factor)/len_pages
            else:
                dict1[i] = (1-damping_factor)/len_pages

    return dict1

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dict1 = {}
    trans = [(page, transition_model(corpus, page, damping_factor)) for page in corpus]
    pages= []
    for i in trans:
        pages = []
        probs = []
        (page, transition) = i
        for page1 in transition:
            pages.append(page1)
            probs.append(transition[page1])
        dict1[page] = (pages, probs)



    samples = []
    samples.append(random.choice(pages))

    for i in range(n-1):
        samples.append(random.choices(dict1[samples[-1]][0], weights=dict1[samples[-1]][1], k = 1)[0])
    dict2 = {}
    for i in pages:
        dict2[i] = samples.count(i)/n
    return dict2
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    for i in corpus:#normalizing if a page has no links
        if not corpus[i]:
            corpus[i] = set(corpus.keys())

    def incoming(i):
        num =[]
        for page in corpus:
            if i in corpus[page]:
                num.append(page)
        return num

    pages = corpus.keys()
    len_pages = len(pages)
    dict1 = {}#previous pagerank
    for i in pages:
        dict1[i] = 1/len_pages

    while True:

        val = []
        dict2 = {}#new pagerank
        for page in dict1:
            dict2[page] = (1-damping_factor)/len_pages

            for page1 in incoming(page):
                num_link = len(corpus[page1])
                dict2[page] +=damping_factor*dict1[page1]/num_link

            val.append(abs(dict2[page]-dict1[page]))




        for i in val:#tolerance check
            if i>0.001:
                break
        else:
            return dict2
        dict1 = dict2



if __name__ == "__main__":
    main()
