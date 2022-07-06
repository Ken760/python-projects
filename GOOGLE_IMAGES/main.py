from icrawler.builtin import GoogleImageCrawler


def google_img_downloader():
    filters = dict(
        type='',  # “photo”, “face”, “clipart”, “linedrawing”, “animated”.
        color='',  # color”, “blackandwhite”, “transparent”, “red”, “orange”, “yellow”,
        # “green”, “teal”, “blue”, “purple”, “pink”, “white”, “gray”, “black”, “brown”.
        size='',  # “large”, “medium”, “icon”, or larger than a given size (e.g. “>640x480”),
        # or exactly is a given size (“=1024x768”).
        license='',  # noncommercial”(labeled for noncommercial reuse), “commercial”(labeled for reuse)
        date='',  # “pastday”, “pastweek” or a tuple of dates, e.g.
        # ((2016, 1, 1), (2017, 1, 1)) or ((2016, 1, 1), None).
    )
    crawler = GoogleImageCrawler(storage={'root_dir': './img'})
    crawler.crawl(
        keyword='',  # image name
        max_num=5,  # number of images
        max_size=(1000, 1000),
        overwrite=True,
        filters=filters,
        file_idx_offset='auto'
    )


def main():
    google_img_downloader()


if __name__ == '__main__':
    main()
