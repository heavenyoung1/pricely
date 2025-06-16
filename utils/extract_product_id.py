

def parse_ID(url: str) -> str:
    splitedStr = url.split("/")[-2]
    ID = splitedStr[-10:]
    return ID

print(parse_ID("https://www.ozon.ru/product/nabor-kvadratnyh-konteynerov-dlya-edy-i-hraneniya-fusion-6-sht-2082762097/?campaignId=543"))