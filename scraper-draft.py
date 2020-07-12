import scrapy


class VozSpider(scrapy.Spider):
    name = 'DiemBao'
    start_urls = []

    def parse(self, response):
        POST_SELECTOR = '.message--post'
        
        USER_SELECTOR = '::attr(data-author)'
        LINK_SELECTOR = '.message-userContent::attr(data-lb-id)'
        TEXT_SELECTOR = '.bbWrapper::text'
        IGNORE_SELECTOR = '.username::attr(href)'
        
        def create_ignore_url(user_href, username):
            return f'<a href="https://voz.vn{user_href}ignore">Ignore {username}</a>'
        
        
        for post in response.css(POST_SELECTOR): # ignore first post
            yield {
                'user': post.css(USER_SELECTOR).extract_first(),
                'link': f'<a href="{response.urljoin(post.css(LINK_SELECTOR).extract_first())}">Link to post</a>',
                'text': ' '.join(par.strip() for par in post.css(TEXT_SELECTOR).getall()),
                'ignore': create_ignore_url(post.css(IGNORE_SELECTOR).extract_first(),\
                                            post.css(USER_SELECTOR).extract_first()),
            }
        
        NEXT_PAGE_SELECTOR = '.pageNav-jump--next::attr(href)'
        
        href = response.css(NEXT_PAGE_SELECTOR).extract_first()
        url = response.urljoin(href)
        
        yield scrapy.Request(url=url, callback=self.parse)