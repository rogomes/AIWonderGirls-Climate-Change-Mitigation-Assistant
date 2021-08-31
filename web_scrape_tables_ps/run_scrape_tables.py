import argparse
from scrape_data import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run web scrape tables data...')
    parser.add_argument('--url_links', type=str,
                        help='Url link as strings separated by comma, if more than one link')
    url_tag_help = 'Url tags as strings separated by comma, if more than one link. '
    url_tag_help = url_tag_help + "  Each tag indicates the source i.e. link"
    parser.add_argument('--url_tags', type=str,
                        help=url_tag_help)
    parser.add_argument('--path_to_save', type=str,
                        help='Path for saving the scraped table data')
    parser.add_argument('--file_type', type=str, default='csv',
                        help='File save type')

    args = parser.parse_args()

    # e.g.
    # url_link = "https://drawdown.org/solutions/table-of-solutions"
    # url_tag = "tableofsolutions"
    # path_to_save = "/content/site_tables"

    url_links = args.url_links.split(",")
    url_tags = args.url_tags.split(",")
    path_to_save = args.path_to_save
    file_type = args.file_type
    print(f"url_links, url_tags: {url_links}, {url_tags}")
    extract_site_tables(url_links, url_tags, path_to_save, file_type)
