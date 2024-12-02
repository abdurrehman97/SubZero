import scrapy
import re


class Brands(scrapy.Spider):
    name = "Test_Project_Spider"

    start_urls = [
        "https://www.subzero-wolf.com/"
    ]

    def parse(self, response, **kwargs):
        return self.make_shelf_api_request()

    def product_shelve(self, response):
        product_shelves = response.css(".coveo-result-image a::attr(href)").getall()

        if product_shelves:
            yield from response.follow_all(product_shelves, callback=self.extract_products_fields)

    def extract_products_fields(self, response):

        model = response.css("#productNoValue::text").get()
        product = response.css(".product-title-heading::text").get()
        thumb = response.css("#productHeaderImg img::attr(src)").get()
        file_urls = response.xpath('.//a[contains(text(), "Use and Care Guide")]/@href').get()
        type_ = response.xpath('.//div[contains(@class, "tab-pane")]//li/a[contains(text(), "Use and Care Guide")]/text()').get()
        type_ = re.search(r"(Use and Care Guide)", type_)
        type_ = type_.group(0) if type_ else None
        brand = response.css('span[itemprop="name"]::text').get()
        language = response.css('html.non-touch::attr(lang)').get()
        if thumb:
            thumb = f"https://www.subzero-wolf.com/trade-resources/product-specifications/product-specifications-detail{thumb}"
        if file_urls:
            file_urls = f'https://www.subzero-wolf.com/{file_urls}'

        yield {
            "model": model if model else None,
            "model_2": '',
            "brand": brand if brand else None,
            "product": product if product else None,
            "product_parent": '',
            "product_lang": language.split('-')[0],
            "file_urls": file_urls,
            "type": type_,
            "url": response.url,
            "thumb": thumb,
            "source": "Sub-Zero, Wolf, and Cove | Kitchen Appliances that Inspire"
        }

    def parse_shelf_api(self, response):

        data = response.json()
        results = data.get("results", [])

        for item in results:
            yield scrapy.Request(
                url=item["printableUri"],
                callback=self.extract_products_fields,
                cookies={"CheckCountry": "False"},
            )

    def make_shelf_api_request(self):
        url = "https://www.subzero-wolf.com/coveo/rest/search/v2?sitecoreItemUri=sitecore%3A%2F%2Fweb%2F%7B81EA8ECE-4FEC-4AC0-8A7E-F480D6694A6D%7D%3Flang%3Den-US%26amp%3Bver%3D1&siteName=UnitedStates"
        body = 'actionsHistory=%5B%5D&referrer=&analytics=%7B%22clientId%22%3A%22%22%2C%22documentLocation%22%3A%22https%3A%2F%2Fwww.subzero-wolf.com%2Fsub-zero%2Fconfigurator%23sort%3D%2540displayorder%2520descending%26numberOfResults%3D100%26f%3AConfiguration%3D%5BUndercounter%2CDrawer%5D%22%2C%22documentReferrer%22%3A%22%22%2C%22pageId%22%3A%22%22%7D&isGuestUser=false&aq=(NOT%20%40z95xtemplate%3D%3D(ADB6CA4F03EF4F47B9AC9CE2BA53FF97%2CFE5DD82648C6436DB87A7C4210C7413B))%20((%40issearchable%3D%3Dtrue)%20(%40brand%3D%3D%22sub-zero%22)%20(%40productstatus%3D%3Dactive))%20(%40productconfiguration%3D%3D(%22Undercounter%22%2C%22Drawer%22))&cq=(%40z95xlanguage%3D%3D%22en-US%22)%20(%40z95xlatestversion%3D%3D1)%20(%40source%3D%3D%22Coveo_web_index%20-%20s10.subzero.com%22)&searchHub=configurator&locale=en&maximumAge=900000&firstResult=0&numberOfResults=100&excerptLength=200&enableDidYouMean=false&sortCriteria=%40displayorder%20descending&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&groupBy=%5B%7B%22field%22%3A%22%40producttype%22%2C%22maximumNumberOfValues%22%3A101%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40productwidth%22%2C%22maximumNumberOfValues%22%3A101%2C%22sortCriteria%22%3A%22alphaascending%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40productconfiguration%22%2C%22maximumNumberOfValues%22%3A101%2C%22sortCriteria%22%3A%22nosort%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%22Column%22%2C%22French%20Door%22%2C%22Over%20%26%20Under%22%2C%22Side-by-Side%22%2C%22Undercounter%22%2C%22Drawer%22%2C%22Compact%20Refrigeration%22%2C%22Double%22%2C%22Drop-Down%20Door%22%2C%22Island%20Hoods%22%2C%22Pro%20Wall%20Hoods%22%2C%22Side-Swing%20Door%22%2C%22Single%22%2C%22Tall%22%2C%22Wall%20Hoods%22%2C%22Wall%20Chimney%20Hoods%22%2C%2215%5C%22%20Module%20Cooktop%22%5D%2C%22advancedQueryOverride%22%3A%22(NOT%20%40z95xtemplate%3D%3D(ADB6CA4F03EF4F47B9AC9CE2BA53FF97%2CFE5DD82648C6436DB87A7C4210C7413B))%20((%40issearchable%3D%3Dtrue)%20(%40brand%3D%3D%5C%22sub-zero%5C%22)%20(%40productstatus%3D%3Dactive))%22%2C%22constantQueryOverride%22%3A%22(%40z95xlanguage%3D%3D%5C%22en-US%5C%22)%20(%40z95xlatestversion%3D%3D1)%20(%40source%3D%3D%5C%22Coveo_web_index%20-%20s10.subzero.com%5C%22)%22%7D%2C%7B%22field%22%3A%22%40productfeatures%22%2C%22maximumNumberOfValues%22%3A101%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40productstyle%22%2C%22maximumNumberOfValues%22%3A101%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40productfinish%22%2C%22maximumNumberOfValues%22%3A101%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40wolfline%22%2C%22maximumNumberOfValues%22%3A101%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%5D&facetOptions=%7B%7D&categoryFacets=%5B%5D&retrieveFirstSentences=true&timezone=Asia%2FKarachi&enableQuerySyntax=false&enableDuplicateFiltering=false&enableCollaborativeRating=false&debug=false&allowQueriesWithoutKeywords=true'
        headers = {
            "Accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        r = scrapy.Request(
            url=url,
            headers=headers,
            body=body.encode("UTF-8"),
            method='POST',
            callback=self.parse_shelf_api
        )
        return r
