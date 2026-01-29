from dataclasses import dataclass


@dataclass
class ProductFields:
    article: str = '//div[contains(text(),"Артикул")]'
    name: str = '//div[@data-widget="webProductHeading"]//h1'
    price_with_card: int = '//span[@class="tsHeadline600Large"]'
    price_without_card: int = (
        '//span[contains(text(),"₽") and contains(@class,"tsHeadline500Medium")]'
    )
