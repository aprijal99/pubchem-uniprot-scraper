import scrapy, pandas as pd, re
from xml.etree import ElementTree as ET

class UniprotSpider(scrapy.Spider):
  name = 'UniprotSpider'

  def start_requests(self):
    uniprot_code = self.get_uniprot_code()
    for code in uniprot_code:
      if (code == 'NoUniprot'):
        continue

      yield scrapy.Request(
        url=f'https://rest.uniprot.org/uniprotkb/{code}.xml',
        callback=self.parse
      )

  def parse(self, response):
    clean_res = re.sub('\n\s*', '', response.text)

    root = ET.fromstring(clean_res)
    accession = root.find('.//{http://uniprot.org/uniprot}accession').text
    prot_name = root.find('.//{http://uniprot.org/uniprot}fullName').text
    scientific_organism = root.find('.//{http://uniprot.org/uniprot}organism')[0].text
    common_organism = root.find('.//{http://uniprot.org/uniprot}organism')[1].text

    yield {
      'Uniprot': accession,
      'Protein Name': prot_name,
      'Organism': f'{scientific_organism} ({common_organism})'
    }

  def get_uniprot_code(self):
    # code_data = pd.read_csv('code.csv')
    # pdb_data = pd.read_csv('pdb.csv')

    # code_uniprot = list(filter(lambda code: len(code) != 4, code_data.loc[:, 'code']))
    # pdb_uniprot = list(pdb_data.loc[:, 'Uniprot'])
    
    # pdb_uniprot.extend(code_uniprot)

    # return pdb_uniprot

    uniprot = pd.read_csv('new_uniprot.csv')
    uniprot_list = list(uniprot.loc[:, 'code'])

    return [u.rstrip('.pdb') for u in uniprot_list]