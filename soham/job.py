import scrapy
import pandas as pd

class CrunchbaseSpider(scrapy.Spider):
    name = "crunchbase"
    data = []
    scraped_data = []

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    }

    start_urls = ["https://www.crunchbase.com/discover/organization.companies/fef354e3ca2df434451d7186c0a41d57"]

    def parse(self, response):
        identifier_formatters = response.css('identifier-formatter')
        for identifier_formatter in identifier_formatters:
            href_value = identifier_formatter.css('::attr(href)').get()
            if href_value:
                self.data.append(href_value)
                full_url = f"https://www.crunchbase.com{href_value}"
                yield scrapy.Request(url=full_url, callback=self.parse_company)

    def parse_company(self, response):
        company_data = {}
        
        company_data['company_title'] = response.css('.profile-name::text').get()
        company_data['description'] = response.css('span.description.ng-star-inserted::text').get()
        location_elements = response.css('.field-type-identifier-multi a')
        company_data['headquarters_location'] = ', '.join(location_elements.css('::text').getall()[:3])
        company_data['company_website'] = response.css('link-formatter a::attr(href)').get()
        company_data['total_funding'] = response.css('span.component--field-formatter.field-type-money::text').get()
        company_data['founded_date'] = response.css('span.component--field-formatter.field-type-date_precision.ng-star-inserted::attr(title)').get()
        company_data['founders'] = response.css('span.component--field-formatter.field-type-identifier-multi a::text').getall()
        company_data['number_of_lead_investments'] = response.css('a.component--field-formatter.field-type-integer.accent.highlight-color-contrast-light.ng-star-inserted::text').get()
        company_data['diversify_investments'] = response.css('div.identifier-label::text').get()
        company_data['contact_email'] = response.css('.ng-star-inserted::text').get()
        company_data['number_of_employee_profiles'] = response.xpath('/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/mat-tab-nav-panel/div/page-centered-layout/div/div/div[1]/row-card[2]/profile-section/section-card/mat-card/div[2]/big-values-card/div/big-values-card-item/obfuscation/field-formatter/a').get()
        company_data['Total_Products_Active'] = response.css('span.component--field-formatter.field-type-integer.ng-star-inserted::text').getall()
        company_data['active_tech_count'] = response.css('span.component--field-formatter::text').getall()
        company_data['monthly_visits'] = response.css('span.component--field-formatter.field-type-integer.ng-star-inserted::attr(title)').get()

        self.scraped_data.append(company_data)

    def closed(self, reason):
        df = pd.DataFrame(self.scraped_data)
        df.to_csv('crunchbase_data.csv', index=False)
