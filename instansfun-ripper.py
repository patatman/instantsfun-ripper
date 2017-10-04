from lxml import html
import requests

from tqdm import tqdm

print ('Downloading data from website...')

page = requests.get('http://www.instantsfun.es/')
tree = html.fromstring(page.content)
names = tree.xpath('/html/body/div[3]/div/div/div[1]/div[2]/ul/li/h2/a/text()')
colors = tree.xpath('//*[@id="instant_buttons"]//@class')
categories = tree.xpath('/html/body/div[3]/div/div/div[1]/div[2]/ul/li/div[2]/a/@href')
sound_urls = tree.xpath('/html/body/div[3]/div/div/div[1]/div[2]/ul/li/div/audio/source/source/@src')

print ('\tDownload complete!')

print ('Generating .csv file...')

if len(names) == len(colors) == len(categories) == len(sound_urls):

    f = open('scraped_database.csv', 'w')
    f.write('name,color,category,sound_url\n')

    for element in range(0,len(names)):
        seq = (names[element],colors[element],categories[element].split('/')[3], sound_urls[element])
        f.write(','.join(seq))
        f.write('\n')

    f.close()

    print ('\tFile resourced created!')

    print ('Downloading sound files from website...')

    URL_PREFIX = 'http://www.instantsfun.es'

    for element in range(0, len(sound_urls)):
        filename = sound_urls[element].split('/')[2]
        print ('Downloading ' + filename)
        url = URL_PREFIX + sound_urls[element]
        response = requests.get(url, stream=True)

        with open('./audio/' + filename, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)
