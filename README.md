# 📉 Pricely

Запрос в API — FastAPI принимает ProductCreateDTO, PriceCreateDTO, UserCreateDTO.

DTO → Entity — маппер конвертирует Pydantic DTO в чистые доменные объекты.

UseCase — CreateProductUseCase получает доменные объекты и управляет бизнес-логикой.

Repository — инфраструктурная реализация сохраняет объекты через ORM.

ORM ↔ Entity — мапперы конвертируют между слоями.