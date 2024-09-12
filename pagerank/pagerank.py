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
    franks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(franks):
        print(f"  {page}: {franks[page]:.4f}")
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
    prob = corpus.copy()
    i = corpus[page]

    for p in prob.keys():
        if len(i) == 0:
            prob[p] = 1 / len(corpus)
        else:
            if p in i:
                prob[p] = (1 - damping_factor) / len(corpus) + damping_factor / len(i)
            else:
                prob[p] = (1 - damping_factor) / len(corpus)

    return prob

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = corpus.copy()
    soma_links = []

    links = list(corpus.keys())
    link = random.choice(links)
    soma_links.append(link)

    for i in range(n - 1):
        prob = transition_model(corpus, link, damping_factor)
        weights = list(prob.values())
        link = random.choices(links, weights=weights, k=1)[0]
        soma_links.append(link)

    for p in links:
        page_rank[p] = soma_links.count(p) / n
    
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    page_rank = {page: 1 / num_pages for page in corpus}
    change = 1
    epsilon = 0.001  # convergence threshold

    while change > epsilon:
        new_rank = {}
        for page in corpus:
            # Calculate the first term of the formula
            rank = (1 - damping_factor) / num_pages
            
            # Calculate the second term of the formula
            total = 0
            for p in corpus:
                if page in corpus[p]:
                    total += page_rank[p] / len(corpus[p])
                if not corpus[p]:
                    total += page_rank[p] / num_pages
            
            rank += damping_factor * total
            new_rank[page] = rank
        
        # Calculate the maximum change in PageRank values
        change = max(abs(new_rank[page] - page_rank[page]) for page in page_rank)
        
        # Update the PageRank values
        page_rank = new_rank
    
    # Normalize the PageRank values to ensure they sum to 1
    total_rank = sum(page_rank.values())
    page_rank = {page: rank / total_rank for page, rank in page_rank.items()}
    
    return page_rank



if __name__ == "__main__":
    main()
