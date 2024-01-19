import scrapy, pandas as pd

class PdbSpider(scrapy.Spider):
  name = 'PdbSpider'

  def start_requests(self):
    pdb_code = self.get_pdb_code('code.csv')
    for code in pdb_code:
      yield scrapy.Request(
        url=f'https://www.rcsb.org/structure/{code}',
        callback=self.parse
      )

  def parse(self, response):
    code = response.xpath('//span[@id="structureID"]/text()').get()[1:]
    organism = response.xpath('//li[@id="header_organism"]/a/text()').get()
    method = response.xpath('//li[@id="exp_header_0_method"]/text()').get()
    resolution = response.xpath('//li[@id="exp_header_0_diffraction_resolution"]/text()').get()
    uniprot = ''

    try:
      uniprot = response.xpath('//div[@class="table-responsive"]')[0].xpath('./table/tbody/tr')[4].xpath('./td/div')[0].xpath('./a/text()').get()
    except IndexError:
      uniprot = 'NoUniprot'

    if (resolution != None):
      resolution = float(resolution[:4])

    yield {
      'Code': code,
      'Organism': organism,
      'Method': method,
      'Resolution': resolution,
      'Uniprot': uniprot
    }

  def get_pdb_code(self, file_name):
    code = pd.read_csv(file_name)
    # return list(filter(lambda code: len(code) == 4, list(code.loc[:, 'code'])))
    return ['1F2S', '1LU0', '2C4B', '2IT8', '2LET', '2LJS', '2PO8', '4GUX', '5WOV', '6CDX', '6MSL']