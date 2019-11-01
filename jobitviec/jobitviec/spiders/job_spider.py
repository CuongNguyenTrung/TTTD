import scrapy


class JobSpider(scrapy.Spider):
    name = "jobs"
    # allowed_domains = ['http://quotes.toscrape.com']
    start_urls = ['https://itviec.com/it-jobs']


    def parse(self, response):
        #chuyển đến trang cần crawl dữ liệu cụ thể
        for href in response.css("h2.title a::attr(href)"):
            yield response.follow(href, callback=self.parse_job)


        #chuyển trang, đặt số lượng trang crawl hiện tại là 3
        page = response.css("div#show_more a.more-jobs-link").attrib['href']
        if (page.find("page=51") == -1):
            for href in response.css("div#show_more a.more-jobs-link::attr(href)"):
                yield response.follow(href, callback=self.parse)



    def parse_job(self, response):
        def remove_strip(array_string):
            return [item.strip() for item in array_string]

        job_details = response.css("div.job-detail")
        job_title = job_details.css(".job_title::text").get().strip()
        tags_list = remove_strip(job_details.css(".tag-list span::text").getall())
        address = job_details.css(".address__full-address span::text").get()
        reasons = remove_strip(job_details.css(".top-3-reasons li::text").getall())
        description = remove_strip(job_details.css(".description li::text").getall())
        require = remove_strip(job_details.css(".experience li::text").getall())
        love_working_here = remove_strip(job_details.css(".love_working_here li::text").getall())
        company = response.css("h3.name a::text").get()
        # print(job_title, tags_list, address, reasons,description, require, love_working_here, company)
        yield {
            "job_title" : job_title,
            "tags_list" : tags_list,
            "address" : address,
            "reasons" : reasons,
            "description" : description,
            "require" : require,
            "love_working_here" : love_working_here,
            "company" : company,
        }